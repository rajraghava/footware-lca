#!/usr/bin/env python3
"""Build archived-official-spec workflow files and a 100-model expansion scaffold."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
CURRENT_SOURCES = ROOT / "product_source_appendix_40_models.csv"
OUTDIR = ROOT / "archived_specs"
SCAFFOLD_CSV = OUTDIR / "expansion_100_model_scaffold.csv"
TEMPLATE_CSV = OUTDIR / "official_capture_template.csv"
SUMMARY_MD = OUTDIR / "expansion_100_summary.md"


BRAND_SEARCH_PATTERNS = {
    "Nike": "https://www.nike.com/w?q={query}",
    "Jordan": "https://www.nike.com/w?q={query}",
    "Adidas": "https://www.adidas.com/us/search?q={query}",
    "ASICS": "https://www.asics.com/us/en-us/search/?q={query}",
    "Brooks": "https://www.brooksrunning.com/en_us/search/?q={query}",
    "Hoka": "https://www.hoka.com/en/us/search?q={query}",
    "Mizuno": "https://usa.mizuno.com/search?query={query}",
    "New Balance": "https://www.newbalance.com/search/?q={query}",
    "On": "https://www.on.com/en-us/search?q={query}",
    "Puma": "https://us.puma.com/us/en/search?q={query}",
    "Reebok": "https://www.reebok.com/search?q={query}",
    "Saucony": "https://www.saucony.com/en/search?q={query}",
    "Converse": "https://www.converse.com/search?q={query}",
    "Under Armour": "https://www.underarmour.com/en-us/search/?q={query}",
    "Vans": "https://www.vans.com/en-us/search/product?q={query}",
    "Dr. Martens": "https://www.drmartens.com/us/en/search/?text={query}",
}


EXTRA_CANDIDATES = [
    ("Running", "Nike", "Nike Vomero 18"),
    ("Running", "Nike", "Nike Structure 25"),
    ("Running", "Brooks", "Brooks Glycerin 22"),
    ("Running", "Brooks", "Brooks Adrenaline GTS 24"),
    ("Running", "Hoka", "Hoka Bondi 9"),
    ("Running", "Hoka", "Hoka Mach 6"),
    ("Running", "Adidas", "Adidas Supernova Rise"),
    ("Running", "Adidas", "Adidas Adizero Adios Pro 4"),
    ("Running", "ASICS", "ASICS Gel-Nimbus 27"),
    ("Running", "ASICS", "ASICS Novablast 5"),
    ("Running", "New Balance", "New Balance Fresh Foam X 880v15"),
    ("Running", "Saucony", "Saucony Triumph 22"),
    ("Running", "On", "On Cloudsurfer 2"),
    ("Running", "Mizuno", "Mizuno Wave Sky 8"),
    ("Running", "Under Armour", "Under Armour Infinite Elite 2"),
    ("Basketball", "Nike", "Nike Book 1"),
    ("Basketball", "Nike", "Nike Ja 2"),
    ("Basketball", "Nike", "Nike Giannis Freak 6"),
    ("Basketball", "Nike", "Nike G.T. Hustle 3"),
    ("Basketball", "Adidas", "Adidas Dame 9"),
    ("Basketball", "Adidas", "Adidas D.O.N. Issue 6"),
    ("Basketball", "Adidas", "Adidas Crazy IIInfinity"),
    ("Basketball", "Puma", "Puma MB.04"),
    ("Basketball", "Puma", "Puma All-Pro NITRO 2"),
    ("Basketball", "Puma", "Puma Scoot Zeros II"),
    ("Basketball", "Jordan", "Jordan Tatum 3"),
    ("Basketball", "Jordan", "Jordan Luka 3"),
    ("Basketball", "New Balance", "New Balance Fresh Foam BB v3"),
    ("Basketball", "New Balance", "New Balance Hesi Low v2"),
    ("Basketball", "Under Armour", "Under Armour Curry Fox 1"),
    ("Casual", "Nike", "Nike Dunk Low"),
    ("Casual", "Nike", "Nike Cortez"),
    ("Casual", "Nike", "Nike Blazer Mid '77"),
    ("Casual", "Jordan", "Jordan 1 Low"),
    ("Casual", "Adidas", "Adidas Samba OG"),
    ("Casual", "Adidas", "Adidas Superstar"),
    ("Casual", "Adidas", "Adidas Gazelle"),
    ("Casual", "Adidas", "Adidas Campus 00s"),
    ("Casual", "New Balance", "New Balance 574"),
    ("Casual", "New Balance", "New Balance 9060"),
    ("Casual", "New Balance", "New Balance 327"),
    ("Casual", "Converse", "Converse Chuck 70"),
    ("Casual", "Vans", "Vans Knu Skool"),
    ("Casual", "Reebok", "Reebok Classic Leather"),
    ("Casual", "Puma", "Puma Palermo"),
    ("Soccer", "Nike", "Nike Mercurial Vapor 16 Elite"),
    ("Soccer", "Nike", "Nike Phantom Luna 2 Elite"),
    ("Soccer", "Nike", "Nike Premier 3"),
    ("Soccer", "Nike", "Nike Tiempo Legend 10 Academy"),
    ("Soccer", "Adidas", "Adidas F50 Elite"),
    ("Soccer", "Adidas", "Adidas Predator League"),
    ("Soccer", "Adidas", "Adidas Copa Gloro"),
    ("Soccer", "Puma", "Puma Ultra 5 Ultimate"),
    ("Soccer", "Puma", "Puma Future 8 Match"),
    ("Soccer", "Puma", "Puma King Match"),
    ("Soccer", "Mizuno", "Mizuno Alpha Elite"),
    ("Soccer", "Mizuno", "Mizuno Morelia II Japan"),
    ("Soccer", "Mizuno", "Mizuno Morelia Neo IV Beta"),
    ("Soccer", "New Balance", "New Balance Furon v8+"),
    ("Soccer", "New Balance", "New Balance 442 v2 Team"),
]


def brand_search_url(brand: str, model: str) -> str:
    pattern = BRAND_SEARCH_PATTERNS[brand]
    query = quote_plus(model.replace("+", " plus "))
    return pattern.format(query=query)


def current_rows() -> list[dict]:
    frame = pd.read_csv(CURRENT_SOURCES)
    rows = []
    for _, row in frame.iterrows():
        rows.append(
            {
                "Target_Sample": 100,
                "Category": row["Category"],
                "Brand": row["Brand"],
                "Model": row["Model"],
                "Sample_Status": "current_40_modeled_row",
                "Category_Quota_Target": 25,
                "Official_Source_URL": row["Product_Source_URL"],
                "Source_Entry_Type": row["Source_Type"],
                "Archive_Target_URL": row["Product_Source_URL"],
                "Live_Verification_Status": "already linked in current 40-model appendix",
                "Archive_Capture_Status": "pending archived screenshot/pdf capture",
                "Wayback_URL": "",
                "ArchiveToday_URL": "",
                "SKU_Style_Code": "",
                "MSRP_USD_At_Capture": "",
                "Official_Weight_Text": "",
                "Weight_Size_Basis": "",
                "Official_Materials_Text": "",
                "Visible_Material_Confirmation": "current coded material already present; confirm against archived page",
                "Capture_Priority": "high",
                "Next_Action": "Archive the linked official page, extract SKU/MSRP/materials/weight, and attach capture files.",
                "Notes": row["Traceability_Note"],
            }
        )
    return rows


def candidate_rows() -> list[dict]:
    rows = []
    for category, brand, model in EXTRA_CANDIDATES:
        rows.append(
            {
                "Target_Sample": 100,
                "Category": category,
                "Brand": brand,
                "Model": model,
                "Sample_Status": "expansion_candidate_needs_live_capture",
                "Category_Quota_Target": 25,
                "Official_Source_URL": brand_search_url(brand, model),
                "Source_Entry_Type": "official_search_page",
                "Archive_Target_URL": "",
                "Live_Verification_Status": "needs exact official PDP or collection-page resolution",
                "Archive_Capture_Status": "not started",
                "Wayback_URL": "",
                "ArchiveToday_URL": "",
                "SKU_Style_Code": "",
                "MSRP_USD_At_Capture": "",
                "Official_Weight_Text": "",
                "Weight_Size_Basis": "",
                "Official_Materials_Text": "",
                "Visible_Material_Confirmation": "",
                "Capture_Priority": "medium",
                "Next_Action": "Use the official search entrypoint to resolve an exact product or model-family page, then archive and extract SKU/MSRP/materials/weight.",
                "Notes": "Candidate added to balance the 100-model frame; do not model until an exact official page is captured and coded.",
            }
        )
    return rows


def build_template() -> pd.DataFrame:
    columns = [
        "Category",
        "Brand",
        "Model",
        "Official_Source_URL",
        "Resolved_Official_Page_URL",
        "Wayback_URL",
        "ArchiveToday_URL",
        "Capture_Date",
        "Source_Tier",
        "SKU_Style_Code",
        "MSRP_USD_At_Capture",
        "Official_Weight_Text",
        "Weight_Size_Basis",
        "Official_Materials_Text",
        "Upper_Material_Code",
        "Midsole_Code",
        "Outsole_Code",
        "Pair_Mass_Assumption_kg",
        "Lifespan_Bucket_Years",
        "Capture_Files",
        "Reviewer_Notes",
    ]
    return pd.DataFrame(columns=columns)


def write_summary(frame: pd.DataFrame) -> None:
    category_counts = frame.groupby(["Category", "Sample_Status"]).size().unstack(fill_value=0)
    source_counts = Counter(frame["Source_Entry_Type"])
    total = len(frame)
    lines = [
        "# Expansion 100 Summary",
        "",
        "This scaffold expands the current 40-model line to a balanced 100-model target without pretending the 60 new rows are already modeled.",
        "",
        "## Design",
        "",
        f"- Total rows: `{total}`",
        "- Category target: `25` per category",
        f"- Current modeled rows carried over: `{int((frame['Sample_Status'] == 'current_40_modeled_row').sum())}`",
        f"- New expansion candidates: `{int((frame['Sample_Status'] == 'expansion_candidate_needs_live_capture').sum())}`",
        "",
        "## Category Balance",
        "",
        "| Category | Current 40 | New Candidates | Total |",
        "|----------|------------|----------------|-------|",
    ]
    for category in ["Running", "Basketball", "Casual", "Soccer"]:
        current = int(category_counts.loc[category, "current_40_modeled_row"])
        new = int(category_counts.loc[category, "expansion_candidate_needs_live_capture"])
        lines.append(f"| {category} | {current} | {new} | {current + new} |")
    lines.extend(
        [
            "",
            "## Source Entry Types",
            "",
            f"- Current exact or model-family links carried over from the 40-model appendix: `{total - source_counts['official_search_page']}`",
            f"- New search-entry candidates that still need exact-page resolution: `{source_counts['official_search_page']}`",
            "",
            "## Interpretation",
            "",
            "- The 40 current rows remain the only rows with active modeled impact outputs.",
            "- The 60 new rows are source-capture candidates only. They should not be assigned mass, lifespan, or impact values until an exact official page has been archived and coded.",
            "- This scaffold is designed for archival capture first, modeling second.",
            "",
            "## Recommended Next Steps",
            "",
            "1. Resolve exact official PDPs or official collection pages for the 60 candidate rows.",
            "2. Archive each resolved page to PDF/screenshot and log a Wayback or archive.today URL.",
            "3. Extract SKU, MSRP, official materials text, and weight disclosures where available.",
            "4. Only after source capture, assign mass and lifespan assumptions and decide which rows belong in a modeled 100-product dataset.",
            "",
        ]
    )
    SUMMARY_MD.write_text("\n".join(lines))


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(current_rows() + candidate_rows())
    frame = frame.sort_values(["Category", "Sample_Status", "Brand", "Model"]).reset_index(drop=True)
    frame.to_csv(SCAFFOLD_CSV, index=False)
    build_template().to_csv(TEMPLATE_CSV, index=False)
    write_summary(frame)


if __name__ == "__main__":
    main()
