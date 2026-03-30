#!/usr/bin/env python3
"""Build a mass-calibrated v2 dataset for the canonical 40-row release."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
V1_DATASET = ROOT / "expanded_dataset_40_models.csv"
V1_APPENDIX = ROOT / "product_source_appendix_40_models.csv"
WEIGHT_VALIDATION = ROOT / "public_weight_validation_subset.csv"

V2_DATASET = ROOT / "expanded_dataset_40_models_v2.csv"
V2_APPENDIX = ROOT / "product_source_appendix_40_models_v2.csv"
V2_ROW_CHANGES = ROOT / "mass_calibrated_v2_row_changes.csv"
V2_SPEC = ROOT / "Mass_Calibrated_V2_Spec.md"

REFERENCE_DATE = "2026-03-30"
STAGE_COLS = [
    "CO2e_Materials",
    "CO2e_Manufacturing",
    "CO2e_Transport",
    "CO2e_Packaging",
    "CO2e_EOL",
]
ENV_COLS = ["Water_L", "Land_m2", "Ecotox_CTUe"]


def round_land(values: pd.Series) -> pd.Series:
    return values.round(2)


def round_ecotox(values: pd.Series) -> pd.Series:
    return values.round().astype(int)


def build_mass_basis(row: pd.Series) -> str:
    if row["Mass_Calibration_Source"] == "official_single_shoe_disclosure":
        context = str(row["Stated_Size_or_Context"]).strip()
        context_note = f" Official context: {context}." if context and context != "nan" else ""
        return (
            f"V2 pair mass is defined as 2 x the official single-shoe disclosure "
            f"({row['Single_Shoe_Reference_Mass_kg_v2']:.3f} kg per shoe; "
            f"{row['Pair_Mass_kg_v2']:.3f} kg per pair) without additional size correction."
            f"{context_note} The v1 stored proxy ({row['Stored_Mass_kg_v1']:.3f} kg) is retained only as the original screening reference."
        )
    return (
        f"V2 pair mass is defined as 2 x the v1 stored reference mass proxy "
        f"({row['Stored_Mass_kg_v1']:.3f} kg single-shoe-scale proxy; "
        f"{row['Pair_Mass_kg_v2']:.3f} kg explicit pair mass) because no official single-shoe disclosure was recovered "
        "in the public-weight validation subset."
    )


def build_calibration_note(row: pd.Series) -> str:
    if row["Mass_Calibration_Source"] == "official_single_shoe_disclosure":
        return (
            f"Official single-shoe disclosure used for v2 calibration; pair mass set to "
            f"2 x {row['Single_Shoe_Reference_Mass_kg_v2']:.3f} kg."
        )
    return (
        f"No official single-shoe disclosure recovered; pair mass set to 2 x the v1 stored proxy "
        f"({row['Stored_Mass_kg_v1']:.3f} kg)."
    )


def main() -> None:
    dataset = pd.read_csv(V1_DATASET)
    appendix = pd.read_csv(V1_APPENDIX)
    weights = pd.read_csv(WEIGHT_VALIDATION)

    weight_cols = [
        "Model",
        "Official_Weight_URL",
        "Official_Weight_Basis",
        "Official_Single_Shoe_kg",
        "Stated_Size_or_Context",
        "Validation_Status",
    ]
    merged = dataset.merge(weights[weight_cols], on="Model", how="left", validate="one_to_one")

    merged["Stored_Mass_kg_v1"] = merged["Mass_kg"].astype(float)
    merged["Single_Shoe_Reference_Mass_kg_v2"] = merged["Official_Single_Shoe_kg"].fillna(merged["Stored_Mass_kg_v1"]).astype(float)
    merged["Pair_Mass_kg_v2"] = (merged["Single_Shoe_Reference_Mass_kg_v2"] * 2.0).astype(float)
    merged["Mass_Calibration_Source"] = np.where(
        merged["Official_Single_Shoe_kg"].notna(),
        "official_single_shoe_disclosure",
        "doubled_stored_proxy",
    )
    merged["Mass_Calibration_Factor"] = (merged["Pair_Mass_kg_v2"] / merged["Stored_Mass_kg_v1"]).round(3)

    for col in STAGE_COLS:
        intensity = merged[col].astype(float) / merged["Stored_Mass_kg_v1"]
        merged[col] = (intensity * merged["Pair_Mass_kg_v2"]).round(2)

    merged["CO2e_Total"] = (
        merged["CO2e_Materials"]
        + merged["CO2e_Manufacturing"]
        + merged["CO2e_Transport"]
        + merged["CO2e_Packaging"]
        + merged["CO2e_EOL"]
    ).round(2)

    water_intensity = merged["Water_L"].astype(float) / merged["Stored_Mass_kg_v1"]
    land_intensity = merged["Land_m2"].astype(float) / merged["Stored_Mass_kg_v1"]
    ecotox_intensity = merged["Ecotox_CTUe"].astype(float) / merged["Stored_Mass_kg_v1"]

    merged["Water_L"] = (water_intensity * merged["Pair_Mass_kg_v2"]).round().astype(int)
    merged["Land_m2"] = round_land(land_intensity * merged["Pair_Mass_kg_v2"])
    merged["Ecotox_CTUe"] = round_ecotox(ecotox_intensity * merged["Pair_Mass_kg_v2"])
    merged["Mass_kg"] = merged["Pair_Mass_kg_v2"].round(3)

    merged["Notes"] = merged["Notes"].astype(str).str.rstrip(".") + (
        ". Mass-calibrated v2 release; explicit pair mass is derived from an official single-shoe disclosure where available or from 2 x the v1 stored reference mass proxy otherwise."
    )

    dataset_cols = list(dataset.columns) + [
        "Stored_Mass_kg_v1",
        "Single_Shoe_Reference_Mass_kg_v2",
        "Pair_Mass_kg_v2",
        "Mass_Calibration_Source",
        "Mass_Calibration_Factor",
        "Official_Weight_URL",
        "Official_Weight_Basis",
        "Stated_Size_or_Context",
        "Validation_Status",
    ]
    v2_dataset = merged[dataset_cols].copy()
    v2_dataset.to_csv(V2_DATASET, index=False)

    appendix_v2 = appendix.merge(
        merged[
            [
                "Model",
                "Stored_Mass_kg_v1",
                "Single_Shoe_Reference_Mass_kg_v2",
                "Pair_Mass_kg_v2",
                "Mass_Calibration_Source",
                "Mass_Calibration_Factor",
                "Official_Weight_URL",
                "Official_Weight_Basis",
                "Stated_Size_or_Context",
                "Validation_Status",
            ]
        ],
        on="Model",
        how="left",
        validate="one_to_one",
    )
    appendix_v2["Original_Mass_Basis_V1"] = appendix_v2["Mass_Basis"]
    appendix_v2["Mass_Basis"] = appendix_v2.apply(build_mass_basis, axis=1)
    appendix_v2["Accessed_Date"] = REFERENCE_DATE
    appendix_v2["Mass_Calibration_Note"] = appendix_v2.apply(build_calibration_note, axis=1)
    appendix_cols = list(appendix.columns) + [
        "Original_Mass_Basis_V1",
        "Stored_Mass_kg_v1",
        "Single_Shoe_Reference_Mass_kg_v2",
        "Pair_Mass_kg_v2",
        "Mass_Calibration_Source",
        "Mass_Calibration_Factor",
        "Official_Weight_URL",
        "Official_Weight_Basis",
        "Stated_Size_or_Context",
        "Validation_Status",
        "Mass_Calibration_Note",
    ]
    appendix_v2 = appendix_v2[appendix_cols]
    appendix_v2.to_csv(V2_APPENDIX, index=False)

    row_changes = pd.DataFrame(
        {
            "Model": merged["Model"],
            "Category": merged["Category"],
            "Upper_Material_Type": merged["Upper_Material_Type"],
            "Stored_Mass_kg_v1": merged["Stored_Mass_kg_v1"].round(3),
            "Pair_Mass_kg_v2": merged["Pair_Mass_kg_v2"].round(3),
            "Mass_Calibration_Source": merged["Mass_Calibration_Source"],
            "Mass_Calibration_Factor": merged["Mass_Calibration_Factor"],
            "CO2e_Total_v1": dataset["CO2e_Total"].astype(float).round(2),
            "CO2e_Total_v2": merged["CO2e_Total"].astype(float).round(2),
            "CO2e_Total_Delta": (merged["CO2e_Total"].astype(float) - dataset["CO2e_Total"].astype(float)).round(2),
            "Official_Weight_URL": merged["Official_Weight_URL"].fillna(""),
        }
    ).sort_values(["Category", "Model"])
    row_changes.to_csv(V2_ROW_CHANGES, index=False)

    official_count = int((merged["Mass_Calibration_Source"] == "official_single_shoe_disclosure").sum())
    proxy_count = int((merged["Mass_Calibration_Source"] == "doubled_stored_proxy").sum())
    mean_factor = float(merged["Mass_Calibration_Factor"].mean())
    mean_total_v1 = float(dataset["CO2e_Total"].mean())
    mean_total_v2 = float(merged["CO2e_Total"].mean())
    median_total_v1 = float(dataset["CO2e_Total"].median())
    median_total_v2 = float(merged["CO2e_Total"].median())
    top_shift = row_changes.sort_values("CO2e_Total_Delta", ascending=False).head(5)

    lines = [
        "# Mass-Calibrated V2 Spec",
        "",
        f"Date: {REFERENCE_DATE}",
        "",
        "This file defines the explicit rules used to construct `expanded_dataset_40_models_v2.csv` as a separate mass-calibrated sensitivity dataset. It does not replace the released canonical 40-row screening dataset.",
        "",
        "## Step 1. Mass Rule",
        "",
        "- Primary functional unit remains one pair of footwear.",
        "- For each row, v2 first defines a single-shoe reference mass.",
        "- If an official single-shoe disclosure is present in `public_weight_validation_subset.csv`, that value is used directly.",
        "- Otherwise, the v1 stored mass proxy is treated as a single-shoe-scale reference mass.",
        "- V2 pair mass is then defined as `2 x single_shoe_reference_mass`.",
        "",
        "## Step 2. Recalibration Rule",
        "",
        "- The v1 row-level phase intensities are preserved rather than replaced.",
        "- For each row and each environmental field, v1 implied intensity is computed as `field_v1 / stored_mass_v1`.",
        "- V2 environmental fields are computed as `implied_intensity_v1 x pair_mass_v2`.",
        "- This keeps product-specific architecture patterns intact while making the mass basis explicit.",
        "- Official single-shoe disclosures override the stored proxy only for the seven validated rows; all other rows use `2 x stored_mass_v1`.",
        "",
        "## Step 3. Generated Files",
        "",
        "- `expanded_dataset_40_models_v2.csv`",
        "- `product_source_appendix_40_models_v2.csv`",
        "- `mass_calibrated_v2_row_changes.csv`",
        "",
        "## Coverage",
        "",
        f"- Official single-shoe disclosure rows: `{official_count}`",
        f"- Doubled stored-proxy rows: `{proxy_count}`",
        f"- Mean mass calibration factor: `{mean_factor:.3f}`",
        "",
        "## Headline Delta",
        "",
        f"- Mean CO2e total: `{mean_total_v1:.3f}` -> `{mean_total_v2:.3f}`",
        f"- Median CO2e total: `{median_total_v1:.3f}` -> `{median_total_v2:.3f}`",
        "",
        "## Largest Row-Level Shifts",
        "",
    ]
    for row in top_shift.itertuples(index=False):
        lines.append(
            f"- `{row.Model}`: `{row.CO2e_Total_v1:.2f}` -> `{row.CO2e_Total_v2:.2f}` kg CO2e (`+{row.CO2e_Total_Delta:.2f}`; factor `{row.Mass_Calibration_Factor:.3f}`; source `{row.Mass_Calibration_Source}`)"
        )
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "This v2 dataset is a mass-calibrated sensitivity release. Because the original 40-row release is already embedded in a fixed screening model, v2 should be treated as a new versioned dataset rather than as a silent correction of v1.",
        ]
    )
    V2_SPEC.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
