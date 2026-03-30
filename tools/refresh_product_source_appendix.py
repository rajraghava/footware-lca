#!/usr/bin/env python3
"""Refresh the canonical 40-row product-source appendix from the hardened archive index."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_INDEX = ROOT / "archived_specs" / "canonical_40_archive_index.csv"
SOURCE_APPENDIX = ROOT / "product_source_appendix_40_models.csv"
HARDENED_ACCESS_DATE = "2026-03-30"


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


def build_traceability_note(row: pd.Series) -> str:
    parts: list[str] = []
    base = str(row.get("Traceability_Note", "")).strip()
    note = str(row.get("Notes", "")).strip()

    if base:
        parts.append(base)
    if note and note not in parts:
        parts.append(note)

    artifacts = [
        str(row.get("Existing_HTML_Artifact", "")).strip(),
        str(row.get("Existing_PDF_Artifact", "")).strip(),
        str(row.get("Existing_Screenshot_Artifact", "")).strip(),
    ]
    if all(artifacts):
        parts.append("Local HTML/PDF/screenshot captures are archived in archived_specs for the Phase 1 provenance-hardening pass.")
    elif any(artifacts):
        parts.append("Partial local capture artifacts are archived in archived_specs for the Phase 1 provenance-hardening pass.")

    archive_url = str(row.get("Archive_URL", "")).strip()
    if archive_url:
        parts.append(f"Third-party archive URL: {archive_url}")

    cleaned: list[str] = []
    for part in parts:
        normalized = " ".join(part.split())
        if normalized and normalized not in cleaned:
            cleaned.append(normalized)
    return " ".join(cleaned)


def main() -> None:
    archive = pd.read_csv(ARCHIVE_INDEX, dtype=str).fillna("")
    existing = pd.read_csv(SOURCE_APPENDIX, dtype=str).fillna("")

    merged = existing.merge(
        archive[
            [
                "Model",
                "Brand",
                "Category",
                "Current_Source_Type",
                "Current_Product_URL",
                "Current_Price_URL",
                "Resolved_URL",
                "Evidence_Tier_Final",
                "SKU_or_Style_Code",
                "Existing_HTML_Artifact",
                "Existing_PDF_Artifact",
                "Existing_Screenshot_Artifact",
                "Archive_URL",
                "Capture_Status",
                "Traceability_Note",
                "Notes",
            ]
        ],
        on=["Model", "Brand", "Category"],
        how="left",
        validate="one_to_one",
        suffixes=("", "_archive"),
    )

    refreshed = pd.DataFrame(
        {
            "Model": merged["Model"],
            "Brand": merged["Brand"],
            "Category": merged["Category"],
            "Product_Source_URL": merged["Resolved_URL"].where(merged["Resolved_URL"] != "", merged["Product_Source_URL"]),
            "Price_Source_URL": merged["Resolved_URL"].where(merged["Resolved_URL"] != "", merged["Price_Source_URL"]),
            "Accessed_Date": HARDENED_ACCESS_DATE,
            "Source_Type": merged["Evidence_Tier_Final"].where(merged["Evidence_Tier_Final"] != "", merged["Source_Type"]),
            "Traceability_Note": merged.apply(build_traceability_note, axis=1),
            "Price_Coding_Note": merged["Price_Coding_Note"],
            "Mass_Basis": merged["Mass_Basis"].map(normalize_mass_basis),
            "Lifespan_Basis": merged["Lifespan_Basis"],
            "Original_Source_Type": merged["Current_Source_Type"].where(merged["Current_Source_Type"] != "", merged["Source_Type"]),
            "Original_Product_Source_URL": merged["Current_Product_URL"].where(merged["Current_Product_URL"] != "", merged["Product_Source_URL"]),
            "Original_Price_Source_URL": merged["Current_Price_URL"].where(merged["Current_Price_URL"] != "", merged["Price_Source_URL"]),
            "SKU_or_Style_Code": merged["SKU_or_Style_Code"],
            "Local_HTML_Artifact": merged["Existing_HTML_Artifact"],
            "Local_PDF_Artifact": merged["Existing_PDF_Artifact"],
            "Local_Screenshot_Artifact": merged["Existing_Screenshot_Artifact"],
            "Archive_URL": merged["Archive_URL"],
            "Capture_Status": merged["Capture_Status"],
        }
    )

    refreshed.to_csv(SOURCE_APPENDIX, index=False)


if __name__ == "__main__":
    main()
