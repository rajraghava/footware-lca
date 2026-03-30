#!/usr/bin/env python3
"""Build a ranked next-pass queue for expanding the official public-weight validation subset."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
APPENDIX_PATH = ROOT / "product_source_appendix_40_models.csv"
SUBSET_PATH = ROOT / "public_weight_validation_subset.csv"
QUEUE_PATH = ROOT / "public_weight_validation_next_pass.csv"
SUMMARY_PATH = ROOT / "public_weight_validation_next_pass_summary.md"

PERFORMANCE_CATEGORIES = {"Running", "Soccer", "Basketball"}
BRAND_PRIORITY = {"Nike", "Hoka", "ASICS", "Mizuno", "Under Armour", "Brooks", "Saucony", "New Balance", "Puma"}


def extract_pdf_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True, check=True).stdout
    except Exception:
        return ""


def normalize(text: str) -> str:
    return " ".join(text.split())


def analyze_signals(html_text: str, pdf_text: str) -> tuple[str, str, str, str, str]:
    combined = f"{normalize(pdf_text)} {normalize(html_text)}"
    gram_hits = "; ".join(re.findall(r"\b(\d{2,4})\s?g\b", combined, re.I)[:5])
    oz_hits = "; ".join(re.findall(r"\b(\d+(?:\.\d+)?)\s?oz\b", combined, re.I)[:5])
    weight_context = bool(re.search(r"\bweight\b", combined, re.I))
    numeric_context = bool(gram_hits or oz_hits)
    if weight_context and numeric_context:
        confidence = "high"
    elif weight_context:
        confidence = "medium"
    else:
        confidence = "low"
    snippet_match = re.search(r"(.{0,80}\bweight\b.{0,160})", combined, re.I)
    snippet = snippet_match.group(1)[:240] if snippet_match else ""
    signal_source = "pdf_or_html_weight_signal" if weight_context else "no_direct_weight_signal"
    return confidence, signal_source, gram_hits, oz_hits, snippet


def queue_rank(row: pd.Series) -> tuple[int, int, int, str]:
    confidence_order = {"high": 0, "medium": 1, "low": 2}
    category_order = {"Running": 0, "Soccer": 1, "Basketball": 2, "Casual": 3}
    brand_bonus = 0 if row["Brand"] in BRAND_PRIORITY else 1
    return (
        confidence_order.get(str(row["Signal_Confidence"]), 9),
        category_order.get(str(row["Category"]), 9),
        brand_bonus,
        str(row["Model"]),
    )


def recommended_action(row: pd.Series) -> str:
    if row["Signal_Confidence"] == "high":
        return "Re-open the official page, verify the exact weight excerpt, and promote the row into public_weight_validation_subset.csv if the disclosure is unambiguous."
    if row["Signal_Confidence"] == "medium":
        return "Manual check recommended: inspect product details/specifications on the official page for an explicit single-shoe disclosure."
    if row["Category"] in PERFORMANCE_CATEGORIES and row["Brand"] in BRAND_PRIORITY:
        return "Keep in the next-pass set; performance models from this brand/category are still plausible official-weight candidates despite no clean local text hit."
    return "Lower priority unless a new official page or archived excerpt surfaces."


def main() -> None:
    appendix = pd.read_csv(APPENDIX_PATH).fillna("")
    validated_models = set(pd.read_csv(SUBSET_PATH)["Model"])

    rows = []
    for row in appendix.itertuples(index=False):
        if row.Model in validated_models:
            continue
        html_path = ROOT / row.Local_HTML_Artifact if row.Local_HTML_Artifact else None
        pdf_path = ROOT / row.Local_PDF_Artifact if row.Local_PDF_Artifact else None
        html_text = html_path.read_text(errors="ignore") if html_path and html_path.exists() else ""
        pdf_text = extract_pdf_text(pdf_path) if pdf_path else ""
        confidence, signal_source, gram_hits, oz_hits, snippet = analyze_signals(html_text, pdf_text)
        rows.append(
            {
                "Model": row.Model,
                "Brand": row.Brand,
                "Category": row.Category,
                "Source_Type": row.Source_Type,
                "Product_Source_URL": row.Product_Source_URL,
                "Local_HTML_Artifact": row.Local_HTML_Artifact,
                "Local_PDF_Artifact": row.Local_PDF_Artifact,
                "Signal_Confidence": confidence,
                "Signal_Source": signal_source,
                "Gram_Hits": gram_hits,
                "Oz_Hits": oz_hits,
                "Evidence_Snippet": snippet,
                "Recommended_Action": "",
            }
        )

    queue = pd.DataFrame(rows)
    queue["Recommended_Action"] = queue.apply(recommended_action, axis=1)
    queue = queue.sort_values(by=list(range(4)), key=None) if False else queue.iloc[
        sorted(range(len(queue)), key=lambda idx: queue_rank(queue.iloc[idx]))
    ].reset_index(drop=True)
    queue.insert(0, "Queue_Rank", range(1, len(queue) + 1))
    queue.to_csv(QUEUE_PATH, index=False)

    counts = queue["Signal_Confidence"].value_counts().to_dict()
    top_rows = queue.head(10)
    lines = [
        "# Public Weight Validation Next-Pass Summary",
        "",
        "Date: 2026-03-30",
        "",
        f"- Remaining unvalidated canonical rows: `{len(queue)}`",
        f"- High-confidence local signal rows: `{counts.get('high', 0)}`",
        f"- Medium-confidence local signal rows: `{counts.get('medium', 0)}`",
        f"- Low-confidence rows: `{counts.get('low', 0)}`",
        "",
        "## Top 10 Next-Pass Targets",
        "",
    ]
    for row in top_rows.itertuples(index=False):
        lines.append(
            f"- `{row.Queue_Rank}. {row.Model}` (`{row.Category}`, `{row.Brand}`): `{row.Signal_Confidence}` signal; action: {row.Recommended_Action}"
        )
    lines.extend(
        [
            "",
            "## Files",
            "",
            "- `public_weight_validation_next_pass.csv`",
            "- `public_weight_validation_next_pass_summary.md`",
        ]
    )
    SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
