#!/usr/bin/env python3
"""Build a Phase 1 provenance-hardening scaffold for the canonical 40-row dataset."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "expanded_dataset_40_models.csv"
APPENDIX_PATH = ROOT / "product_source_appendix_40_models.csv"
ARCHIVE_DIR = ROOT / "archived_specs"
HTML_DIR = ARCHIVE_DIR / "canonical_40_live_html_captures"
PDF_DIR = ARCHIVE_DIR / "canonical_40_live_pdf_captures"
SCREENSHOT_DIR = ARCHIVE_DIR / "canonical_40_screenshots"
OUTPUT_PATH = ARCHIVE_DIR / "canonical_40_archive_index.csv"
HIGH_PRIORITY_QUEUE_PATH = ARCHIVE_DIR / "canonical_40_high_priority_queue.csv"


def normalize_mass_basis(text: str) -> str:
    normalized = " ".join(str(text).split())
    replacements = {
        "Screening pair-mass estimate anchored": "Screening stored reference mass anchored",
        "Pilot pair-mass estimate anchored": "Pilot stored reference mass anchored",
    }
    for old, new in replacements.items():
        if old in normalized:
            normalized = normalized.replace(old, new)
    return normalized


HIGH_PRIORITY_QUEUE = {
    "Nike Pegasus 41": {
        "rank": 1,
        "wave": "wave_1_fastest",
        "tier": "easy",
        "rationale": "Nike collection page with a likely recoverable exact PDP; Nike models have been the most capture-friendly in this workspace.",
    },
    "Hoka Clifton 9": {
        "rank": 2,
        "wave": "wave_1_fastest",
        "tier": "easy",
        "rationale": "Exact regional PDP already identified; HOKA pages have yielded the cleanest local HTML/PDF captures so far.",
    },
    "Nike KD 17": {
        "rank": 3,
        "wave": "wave_1_fastest",
        "tier": "easy",
        "rationale": "Regional Nike PDP already resolved, and Nike basketball rows have generally converted cleanly to exact style-code pages.",
    },
    "Nike Air Force 1 '07 LV8": {
        "rank": 4,
        "wave": "wave_1_fastest",
        "tier": "easy",
        "rationale": "Nike collection page likely maps to an exact product page, though the exact colorway/SKU may need manual disambiguation.",
    },
    "Nike Phantom GX 2 Elite": {
        "rank": 5,
        "wave": "wave_1_fastest",
        "tier": "easy",
        "rationale": "Regional Nike soccer PDP already exists; the main task is finding the equivalent U.S. or stable exact page.",
    },
    "Nike Zoom GT Cut 3": {
        "rank": 6,
        "wave": "wave_2_medium",
        "tier": "medium",
        "rationale": "Only a release page is currently cited, but Nike usually retains a recoverable PDP for newer signature/performance models.",
    },
    "Jordan Luka 2": {
        "rank": 7,
        "wave": "wave_2_medium",
        "tier": "medium",
        "rationale": "Release-page-only row; likely still recoverable through Nike/Jordan style-code search, but older model status makes it less certain.",
    },
    "On Cloudmonster": {
        "rank": 8,
        "wave": "wave_2_medium",
        "tier": "medium",
        "rationale": "On usually resolves cleanly enough for source confirmation, but local captures tend to degrade to a JS shell rather than a full HTML artifact.",
    },
    "Mizuno Wave Rider 27": {
        "rank": 9,
        "wave": "wave_2_medium",
        "tier": "medium",
        "rationale": "Model-family page is already identified and likely close to an exact PDP, but Mizuno page structure is less predictable than Nike or HOKA.",
    },
    "ASICS Gel-Kayano 31": {
        "rank": 10,
        "wave": "wave_2_medium",
        "tier": "medium",
        "rationale": "Exact PDP is likely recoverable, but ASICS has previously returned blocked or degraded automated captures in this workspace.",
    },
    "Adidas Harden Vol. 8": {
        "rank": 11,
        "wave": "wave_3_hardest",
        "tier": "hard",
        "rationale": "adidas exact PDP likely exists, but adidas pages have repeatedly returned 403-style blocks during local capture attempts.",
    },
    "Mizuno Morelia Neo IV": {
        "rank": 12,
        "wave": "wave_3_hardest",
        "tier": "hard",
        "rationale": "Current family page resolves to a neighboring Pro/all-surface variant, so exact variant disambiguation is likely to be manual and slower.",
    },
    "Adidas Stan Smith Primegreen": {
        "rank": 13,
        "wave": "wave_3_hardest",
        "tier": "hard",
        "rationale": "Current evidence is only a newsroom/release page for an older Primegreen concept row; exact PDP recovery may now depend on archives rather than live product pages.",
    },
}


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def relpath(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def first_existing(paths: list[Path]) -> str:
    for path in paths:
        if path.exists():
            return relpath(path)
    return ""


def phase1_action(source_type: str) -> str:
    if source_type == "official_exact_pdp":
        return "Capture the exact PDP locally, record SKU/style code, and add archive URL if available."
    return (
        "Attempt to upgrade to an exact official PDP; if unavailable, capture the current official fallback "
        "locally and retain explicit proxy labeling."
    )


def upgrade_priority(source_type: str) -> str:
    return "high" if source_type != "official_exact_pdp" else "medium"


def capture_status(existing_html: str, existing_pdf: str) -> str:
    return "existing_capture_found" if existing_html or existing_pdf else "pending_capture"


def build_index() -> pd.DataFrame:
    dataset = pd.read_csv(DATASET_PATH)
    appendix = pd.read_csv(APPENDIX_PATH)

    frame = dataset[["Model", "Brand", "Category"]].merge(
        appendix,
        on=["Model", "Brand", "Category"],
        how="left",
        validate="one_to_one",
    )

    rows: list[dict[str, str]] = []
    legacy_html_dirs = [
        ARCHIVE_DIR / "live_html_captures",
        ARCHIVE_DIR / "live_html_captures_round2",
        HTML_DIR,
    ]
    legacy_pdf_dirs = [
        ARCHIVE_DIR / "live_pdf_captures",
        PDF_DIR,
    ]

    for row in frame.to_dict(orient="records"):
        slug = slugify(row["Model"])
        planned_html = HTML_DIR / f"{slug}.html"
        planned_pdf = PDF_DIR / f"{slug}.pdf"
        planned_screenshot = SCREENSHOT_DIR / f"{slug}.png"

        existing_html = first_existing([directory / f"{slug}.html" for directory in legacy_html_dirs])
        existing_pdf = first_existing([directory / f"{slug}.pdf" for directory in legacy_pdf_dirs])
        existing_screenshot = relpath(planned_screenshot) if planned_screenshot.exists() else ""

        rows.append(
            {
                "Model": row["Model"],
                "Brand": row["Brand"],
                "Category": row["Category"],
                "Current_Source_Type": row["Source_Type"],
                "Current_Product_URL": row["Product_Source_URL"],
                "Current_Price_URL": row["Price_Source_URL"],
                "Resolved_URL": row["Product_Source_URL"],
                "Evidence_Tier_Final": row["Source_Type"],
                "SKU_or_Style_Code": "",
                "Accessed_Date": row["Accessed_Date"],
                "Planned_HTML_Path": relpath(planned_html),
                "Planned_PDF_Path": relpath(planned_pdf),
                "Planned_Screenshot_Path": relpath(planned_screenshot),
                "Existing_HTML_Artifact": existing_html,
                "Existing_PDF_Artifact": existing_pdf,
                "Existing_Screenshot_Artifact": existing_screenshot,
                "Archive_URL": "",
                "Capture_Status": capture_status(existing_html, existing_pdf),
                "Upgrade_Priority": upgrade_priority(row["Source_Type"]),
                "Queue_Rank": HIGH_PRIORITY_QUEUE.get(row["Model"], {}).get("rank", ""),
                "Queue_Wave": HIGH_PRIORITY_QUEUE.get(row["Model"], {}).get("wave", ""),
                "Ease_Tier": HIGH_PRIORITY_QUEUE.get(row["Model"], {}).get("tier", ""),
                "Phase1_Action": phase1_action(row["Source_Type"]),
                "Ranking_Rationale": HIGH_PRIORITY_QUEUE.get(row["Model"], {}).get("rationale", ""),
                "Mass_Basis": normalize_mass_basis(row["Mass_Basis"]),
                "Lifespan_Basis": row["Lifespan_Basis"],
                "Traceability_Note": row["Traceability_Note"],
                "Price_Coding_Note": row["Price_Coding_Note"],
                "Notes": "",
            }
        )

    index = pd.DataFrame(rows)

    if OUTPUT_PATH.exists():
        prior = pd.read_csv(OUTPUT_PATH)
        preserved_cols = [
            "Resolved_URL",
            "Evidence_Tier_Final",
            "SKU_or_Style_Code",
            "Archive_URL",
            "Capture_Status",
            "Existing_HTML_Artifact",
            "Existing_PDF_Artifact",
            "Existing_Screenshot_Artifact",
            "Notes",
        ]
        available = [col for col in preserved_cols if col in prior.columns]
        if available:
            prior = prior[["Model"] + available].drop_duplicates(subset=["Model"])
            index = index.merge(prior, on="Model", how="left", suffixes=("", "_prior"))
            for col in available:
                prior_col = f"{col}_prior"
                index[col] = index[prior_col].fillna(index[col])
                index = index.drop(columns=[prior_col])

    return index


def main() -> None:
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    index = build_index()
    index.to_csv(OUTPUT_PATH, index=False)
    high_queue = index.loc[index["Upgrade_Priority"] == "high"].copy()
    high_queue["_queue_rank_sort"] = pd.to_numeric(high_queue["Queue_Rank"], errors="coerce")
    high_queue = high_queue.sort_values(["_queue_rank_sort", "Model"], na_position="last").drop(columns=["_queue_rank_sort"])
    high_queue.to_csv(HIGH_PRIORITY_QUEUE_PATH, index=False)


if __name__ == "__main__":
    main()
