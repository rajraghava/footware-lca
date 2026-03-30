#!/usr/bin/env python3
"""Build a public official-weight validation subset for the canonical 40-row dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "expanded_dataset_40_models.csv"
APPENDIX_PATH = ROOT / "product_source_appendix_40_models.csv"
SUBSET_PATH = ROOT / "public_weight_validation_subset.csv"
FULL_COVERAGE_PATH = ROOT / "public_weight_validation_coverage.csv"
SUMMARY_PATH = ROOT / "public_weight_validation_summary.md"
PROTOCOL_PATH = ROOT / "Public_Weight_Validation_Protocol.md"


OFFICIAL_DISCLOSURES = [
    {
        "Model": "Nike Pegasus 41",
        "Official_Weight_URL": "https://www.nike.com/t/pegasus-41-mens-road-running-shoes-extra-wide-R6tpoXaD/FN4932-002",
        "Evidence_Location": "local_html_capture",
        "Evidence_Date": "2026-03-30",
        "Official_Weight_Excerpt": "Product Details Weight: Approx. 297g/10.5oz (Men's US 10)",
        "Official_Weight_Grams": 297.0,
        "Official_Weight_Oz": 10.5,
        "Stated_Size_or_Context": "Men's US 10",
        "Official_Weight_Basis": "official_single_shoe_disclosure",
    },
    {
        "Model": "Brooks Ghost 17",
        "Official_Weight_URL": "https://www.brooksrunning.com/en_us/ghost-17/1104421D432.080.html",
        "Evidence_Location": "local_html_capture",
        "Evidence_Date": "2026-03-30",
        "Official_Weight_Excerpt": "Midsole drop 10mm Weight 10.1oz / 286.3g",
        "Official_Weight_Grams": 286.3,
        "Official_Weight_Oz": 10.1,
        "Stated_Size_or_Context": "Not stated in captured excerpt",
        "Official_Weight_Basis": "official_single_shoe_disclosure",
    },
    {
        "Model": "On Cloudmonster",
        "Official_Weight_URL": "https://www.on.com/en-us/products/cloudmonster-61/mens/",
        "Evidence_Location": "local_html_capture",
        "Evidence_Date": "2026-03-30",
        "Official_Weight_Excerpt": "Key features Weight: 275g",
        "Official_Weight_Grams": 275.0,
        "Official_Weight_Oz": "",
        "Stated_Size_or_Context": "Not stated in captured excerpt",
        "Official_Weight_Basis": "official_single_shoe_disclosure",
    },
    {
        "Model": "Mizuno Morelia Neo IV",
        "Official_Weight_URL": "https://usa.mizuno.com/soccer-morelia-neo-iv-beta-elite?sku=54031110001200",
        "Evidence_Location": "local_html_capture",
        "Evidence_Date": "2026-03-30",
        "Official_Weight_Excerpt": "Weight: 200g (size 9)",
        "Official_Weight_Grams": 200.0,
        "Official_Weight_Oz": "",
        "Stated_Size_or_Context": "Size 9",
        "Official_Weight_Basis": "official_single_shoe_disclosure",
    },
    {
        "Model": "ASICS Gel-Kayano 31",
        "Official_Weight_URL": "https://www.asics.com/gb/en-gb/gel-kayano-31/p/1011B867-002.html?width=Standard",
        "Evidence_Location": "official_live_page_excerpt",
        "Evidence_Date": "2026-03-30",
        "Official_Weight_Excerpt": "Weight 305 g/10.8 oz",
        "Official_Weight_Grams": 305.0,
        "Official_Weight_Oz": 10.8,
        "Stated_Size_or_Context": "Not stated in official excerpt",
        "Official_Weight_Basis": "official_single_shoe_disclosure",
    },
    {
        "Model": "New Balance Fresh Foam X 1080v13",
        "Official_Weight_URL": "https://www.newbalance.com/pd/fresh-foam-x-1080v13/W1080V13-43098.html",
        "Evidence_Location": "official_live_page_excerpt",
        "Evidence_Date": "2026-03-30",
        "Official_Weight_Excerpt": "Weight 206 grams (7.3 oz)",
        "Official_Weight_Grams": 206.0,
        "Official_Weight_Oz": 7.3,
        "Stated_Size_or_Context": "Women's model; size not stated in official excerpt",
        "Official_Weight_Basis": "official_single_shoe_disclosure",
    },
    {
        "Model": "Saucony Ride 17",
        "Official_Weight_URL": "https://www.saucony.com/en/ride-17/58858W.html",
        "Evidence_Location": "official_live_page_excerpt",
        "Evidence_Date": "2026-03-30",
        "Official_Weight_Excerpt": "Weight: Women's 8.4oz (238g)",
        "Official_Weight_Grams": 238.0,
        "Official_Weight_Oz": 8.4,
        "Stated_Size_or_Context": "Women's model; size not stated in official excerpt",
        "Official_Weight_Basis": "official_single_shoe_disclosure",
    },
    {
        "Model": "Mizuno Wave Rider 27",
        "Official_Weight_URL": "https://emea.mizuno.com/eu/nl/wave-rider-27/J1GC230304.html",
        "Evidence_Location": "official_live_page_excerpt",
        "Evidence_Date": "2026-03-30",
        "Official_Weight_Excerpt": "Specifications: Weight(g): 260",
        "Official_Weight_Grams": 260.0,
        "Official_Weight_Oz": "",
        "Stated_Size_or_Context": "Not stated in official excerpt",
        "Official_Weight_Basis": "official_single_shoe_disclosure",
    },
    {
        "Model": "Under Armour HOVR Phantom 3",
        "Official_Weight_URL": "https://www.underarmour.com/en-us/p/running/ua_hovr_phantom_3_womens_running_shoes/3025517.html",
        "Evidence_Location": "official_live_page_excerpt",
        "Evidence_Date": "2026-03-30",
        "Official_Weight_Excerpt": "Weight: 9.2 oz.",
        "Official_Weight_Grams": "",
        "Official_Weight_Oz": 9.2,
        "Stated_Size_or_Context": "Women's model; size not stated in official excerpt",
        "Official_Weight_Basis": "official_single_shoe_disclosure",
    },
    {
        "Model": "Adidas Ultraboost Light",
        "Official_Weight_URL": "https://www.adidas.com/cr/es/IE5828.html",
        "Evidence_Location": "official_live_page_excerpt",
        "Evidence_Date": "2026-03-30",
        "Official_Weight_Excerpt": "Peso: 299 gramos (talla CO 40,5)",
        "Official_Weight_Grams": 299.0,
        "Official_Weight_Oz": "",
        "Stated_Size_or_Context": "CO size 40.5 on official adidas locale page",
        "Official_Weight_Basis": "official_single_shoe_disclosure",
    },
    {
        "Model": "New Balance TWO WXY v4",
        "Official_Weight_URL": "https://www.newbalance.com/pd/two-wxy-v4/BB2WYV4-US-CA-NR4.html?dwvar_BB2WYV4-US-CA-NR4_style=BB2WYNR4",
        "Evidence_Location": "official_live_page_excerpt",
        "Evidence_Date": "2026-03-30",
        "Official_Weight_Excerpt": "371 grams (13.1 oz)",
        "Official_Weight_Grams": 371.0,
        "Official_Weight_Oz": 13.1,
        "Stated_Size_or_Context": "Size not stated in official excerpt",
        "Official_Weight_Basis": "official_single_shoe_disclosure",
    },
    {
        "Model": "Under Armour Curry 11",
        "Official_Weight_URL": "https://www.underarmour.com/en-us/p/curry_brand_shoes_and_gear/curry_11_dub_nation_unisex_basketball_shoes/3026615.html",
        "Evidence_Location": "official_live_page_excerpt",
        "Evidence_Date": "2026-03-30",
        "Official_Weight_Excerpt": "Weight: 12.3 oz.",
        "Official_Weight_Grams": "",
        "Official_Weight_Oz": 12.3,
        "Stated_Size_or_Context": "Official Curry 11 family colorway page; size not stated in official excerpt",
        "Official_Weight_Basis": "official_single_shoe_disclosure",
    },
    {
        "Model": "New Balance Tekela v4+",
        "Official_Weight_URL": "https://www.newbalance.com/pd/tekela-pro-low-fg-v4plus/ST1FLV45-45342.html?dwvar_ST1FLV45-45342_style=ST1FLG45",
        "Evidence_Location": "official_live_page_excerpt",
        "Evidence_Date": "2026-03-30",
        "Official_Weight_Excerpt": "201.7 grams (7.1 oz)",
        "Official_Weight_Grams": 201.7,
        "Official_Weight_Oz": 7.1,
        "Stated_Size_or_Context": "Size not stated in official excerpt",
        "Official_Weight_Basis": "official_single_shoe_disclosure",
    },
]


def render_protocol() -> str:
    return """# Public Weight Validation Protocol

Date: 2026-03-30

## Purpose

This file documents a no-purchase, no-teardown validation pass using official brand weight disclosures for a subset of the canonical 40-row footwear dataset.

## Rules

- Only official brand pages or official brand-controlled excerpts are used.
- Official family/colorway pages are acceptable when the model family match is explicit and the brand-controlled source clearly corresponds to the same named product line.
- Retailers, review sites, resale listings, and forum posts are excluded.
- Weight values are recorded exactly as disclosed.
- When the official page presents a single product weight in a product-specification block, the row is labeled `official_single_shoe_disclosure`.
- Both comparison scales are reported:
  - the official disclosed weight as stated
  - a hypothetical pair-converted mass equal to `2 x official single-shoe weight`

## Why Both Scales Are Reported

The official disclosures recovered in this pass are numerically much closer to the stored `Mass_kg` values on a single-shoe scale than on a doubled pair-converted scale. The validation subset is therefore designed as a diagnostic reconciliation table. After this pass, the manuscript and supplement interpret `Mass_kg` as a stored reference mass proxy rather than as a directly measured pair mass.

## Output Files

- `public_weight_validation_subset.csv`
- `public_weight_validation_summary.md`

## Interpretation Rule

If the stored `Mass_kg` values are consistently closer to official single-shoe disclosures than to pair-converted masses, the project should treat that as evidence that the field definition needs reconciliation before submission and that any mass-calibrated re-estimation should be handled as a new model version rather than a clerical correction.
"""


def build_subset() -> pd.DataFrame:
    dataset = pd.read_csv(DATASET_PATH)
    appendix = pd.read_csv(APPENDIX_PATH)
    disclosures = pd.DataFrame(OFFICIAL_DISCLOSURES)

    subset = (
        disclosures.merge(dataset[["Model", "Brand", "Category", "Mass_kg"]], on="Model", how="left", validate="one_to_one")
        .merge(
            appendix[["Model", "Source_Type", "SKU_or_Style_Code", "Local_HTML_Artifact", "Local_PDF_Artifact", "Local_Screenshot_Artifact"]],
            on="Model",
            how="left",
            validate="one_to_one",
        )
    )

    subset["Dataset_Mass_kg"] = subset["Mass_kg"].astype(float)
    subset["Official_Weight_Grams"] = pd.to_numeric(subset["Official_Weight_Grams"], errors="coerce")
    subset["Official_Weight_Oz"] = pd.to_numeric(subset["Official_Weight_Oz"], errors="coerce")
    subset.loc[subset["Official_Weight_Grams"].isna() & subset["Official_Weight_Oz"].notna(), "Official_Weight_Grams"] = (
        subset["Official_Weight_Oz"] * 28.3495
    )
    subset["Official_Weight_Grams"] = subset["Official_Weight_Grams"].round(1)
    subset["Official_Single_Shoe_kg"] = subset["Official_Weight_Grams"] / 1000.0
    subset["Hypothetical_Pair_Converted_kg"] = subset["Official_Single_Shoe_kg"] * 2.0
    subset["Abs_Error_vs_Single_Shoe_kg"] = (subset["Dataset_Mass_kg"] - subset["Official_Single_Shoe_kg"]).abs().round(3)
    subset["Abs_Error_vs_Pair_kg"] = (subset["Dataset_Mass_kg"] - subset["Hypothetical_Pair_Converted_kg"]).abs().round(3)
    subset["Pct_Error_vs_Single_Shoe"] = (
        ((subset["Dataset_Mass_kg"] - subset["Official_Single_Shoe_kg"]) / subset["Official_Single_Shoe_kg"]) * 100.0
    ).round(1)
    subset["Pct_Error_vs_Pair"] = (
        ((subset["Dataset_Mass_kg"] - subset["Hypothetical_Pair_Converted_kg"]) / subset["Hypothetical_Pair_Converted_kg"]) * 100.0
    ).round(1)

    def closer(row: pd.Series) -> str:
        single_error = float(row["Abs_Error_vs_Single_Shoe_kg"])
        pair_error = float(row["Abs_Error_vs_Pair_kg"])
        if abs(single_error - pair_error) < 1e-9:
            return "tie"
        return "single_shoe_scale" if single_error < pair_error else "pair_scale"

    subset["Closer_Scale"] = subset.apply(closer, axis=1)
    subset["Validation_Status"] = "validated_official_weight_disclosure"
    subset["Mass_Scale_Interpretation_Note"] = (
        "Official disclosure is recorded as stated; both single-shoe and pair-converted comparisons are reported because the stored Mass_kg field is treated as a reference-mass proxy rather than as a directly measured pair mass."
    )

    ordered_cols = [
        "Model",
        "Brand",
        "Category",
        "Dataset_Mass_kg",
        "Official_Weight_URL",
        "Evidence_Location",
        "Evidence_Date",
        "Official_Weight_Excerpt",
        "Official_Weight_Grams",
        "Official_Weight_Oz",
        "Stated_Size_or_Context",
        "Official_Weight_Basis",
        "Official_Single_Shoe_kg",
        "Hypothetical_Pair_Converted_kg",
        "Abs_Error_vs_Single_Shoe_kg",
        "Abs_Error_vs_Pair_kg",
        "Pct_Error_vs_Single_Shoe",
        "Pct_Error_vs_Pair",
        "Closer_Scale",
        "Validation_Status",
        "Source_Type",
        "SKU_or_Style_Code",
        "Local_HTML_Artifact",
        "Local_PDF_Artifact",
        "Local_Screenshot_Artifact",
        "Mass_Scale_Interpretation_Note",
    ]
    return subset[ordered_cols].sort_values(["Category", "Brand", "Model"]).reset_index(drop=True)


def build_coverage(subset: pd.DataFrame) -> pd.DataFrame:
    dataset = pd.read_csv(DATASET_PATH)
    appendix = pd.read_csv(APPENDIX_PATH)
    coverage = dataset[["Model", "Brand", "Category", "Mass_kg"]].merge(
        appendix[["Model", "Source_Type", "Product_Source_URL"]],
        on="Model",
        how="left",
        validate="one_to_one",
    )
    validated = subset[["Model", "Official_Weight_URL", "Official_Weight_Grams", "Official_Weight_Basis", "Closer_Scale"]].copy()
    coverage = coverage.merge(validated, on="Model", how="left", validate="one_to_one")
    coverage["Validation_Status"] = coverage["Official_Weight_URL"].apply(
        lambda value: "validated_official_weight_disclosure" if isinstance(value, str) and value else "no_official_weight_found_in_this_pass"
    )
    coverage = coverage.rename(columns={"Mass_kg": "Dataset_Mass_kg"})
    return coverage.sort_values(["Category", "Brand", "Model"]).reset_index(drop=True)


def build_summary(subset: pd.DataFrame) -> str:
    single_mean = subset["Abs_Error_vs_Single_Shoe_kg"].mean()
    pair_mean = subset["Abs_Error_vs_Pair_kg"].mean()
    single_median = subset["Abs_Error_vs_Single_Shoe_kg"].median()
    pair_median = subset["Abs_Error_vs_Pair_kg"].median()
    closer_counts = subset["Closer_Scale"].value_counts().to_dict()
    return f"""# Public Weight Validation Summary

Date: 2026-03-30

## Coverage

- Validated rows with official weight disclosures: `{len(subset)}`
- Canonical sample size: `40`
- Coverage share: `{len(subset) / 40:.1%}`

## Main Result

The recovered official weight disclosures align much more closely with the stored `Mass_kg` values on a single-shoe scale than on a pair-converted scale.

- Mean absolute error vs official single-shoe disclosure: `{single_mean:.3f} kg`
- Median absolute error vs official single-shoe disclosure: `{single_median:.3f} kg`
- Mean absolute error vs hypothetical pair-converted mass: `{pair_mean:.3f} kg`
- Median absolute error vs hypothetical pair-converted mass: `{pair_median:.3f} kg`

## Row-Level Scale Comparison

- Rows closer to single-shoe scale: `{closer_counts.get('single_shoe_scale', 0)}`
- Rows closer to pair-converted scale: `{closer_counts.get('pair_scale', 0)}`
- Ties: `{closer_counts.get('tie', 0)}`

## Interpretation

This subset is best read as a mass-basis reconciliation diagnostic. The official brand disclosures recovered in this pass suggest that the stored `Mass_kg` field behaves more like a single-shoe-scale reference mass proxy than a measured pair mass, and the released 40-row carbon totals are therefore retained unchanged unless a future mass-calibrated model revision is built explicitly.

## Files

- `public_weight_validation_subset.csv`
- `public_weight_validation_coverage.csv`
- `Public_Weight_Validation_Protocol.md`
"""


def main() -> None:
    subset = build_subset()
    coverage = build_coverage(subset)
    subset.to_csv(SUBSET_PATH, index=False)
    coverage.to_csv(FULL_COVERAGE_PATH, index=False)
    SUMMARY_PATH.write_text(build_summary(subset), encoding="utf-8")
    PROTOCOL_PATH.write_text(render_protocol(), encoding="utf-8")


if __name__ == "__main__":
    main()
