#!/usr/bin/env python3
"""Build a 43-row pilot dataset by appending the strongest round-1 candidates."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
BASE_DATASET = ROOT / "expanded_dataset_40_models.csv"
BASE_SOURCES = ROOT / "product_source_appendix_40_models.csv"
PILOT_DATASET = ROOT / "expanded_dataset_43_pilot.csv"
PILOT_SOURCES = ROOT / "product_source_appendix_43_pilot.csv"
PILOT_OUTDIR = ROOT / "pilot_outputs"
PILOT_SUMMARY = PILOT_OUTDIR / "pilot_43_summary.md"
PILOT_COMPARISON = PILOT_OUTDIR / "pilot_43_comparison.csv"


PILOT_ROWS = [
    {
        "Model": "Nike Book 1",
        "Brand": "Nike",
        "Category": "Basketball",
        "Upper_Material": "Leather + textile",
        "Upper_Material_Type": "Partial Leather",
        "Midsole": "Foam + Air Zoom",
        "Outsole": "Rubber",
        "Mass_kg": 0.39,
        "Price_USD": 145,
        "Lifespan_Years": 2.0,
        "CO2e_Materials": 4.40,
        "CO2e_Manufacturing": 1.10,
        "CO2e_Transport": 0.66,
        "CO2e_Packaging": 0.22,
        "CO2e_EOL": 0.09,
        "CO2e_Total": 6.47,
        "Water_L": 335,
        "Land_m2": 1.10,
        "Ecotox_CTUe": 72,
        "Recyclability_Score": "Medium",
        "Disassembly_Difficulty": "High",
        "Notes": "43-row pilot addition; exact PDP and local HTML capture from archived_specs.",
    },
    {
        "Model": "Puma MB.04",
        "Brand": "Puma",
        "Category": "Basketball",
        "Upper_Material": "Double-layered mesh",
        "Upper_Material_Type": "Synthetic Textile",
        "Midsole": "NITROFOAM",
        "Outsole": "Rubber",
        "Mass_kg": 0.34,
        "Price_USD": 115,
        "Lifespan_Years": 1.5,
        "CO2e_Materials": 0.77,
        "CO2e_Manufacturing": 0.19,
        "CO2e_Transport": 0.12,
        "CO2e_Packaging": 0.04,
        "CO2e_EOL": 0.02,
        "CO2e_Total": 1.14,
        "Water_L": 29,
        "Land_m2": 0.01,
        "Ecotox_CTUe": 8,
        "Recyclability_Score": "Medium",
        "Disassembly_Difficulty": "High",
        "Notes": "43-row pilot addition; exact PDP and local HTML capture from archived_specs.",
    },
    {
        "Model": "Nike Dunk Low",
        "Brand": "Nike",
        "Category": "Casual",
        "Upper_Material": "Leather upper",
        "Upper_Material_Type": "Full Leather",
        "Midsole": "Foam",
        "Outsole": "Rubber",
        "Mass_kg": 0.39,
        "Price_USD": 105,
        "Lifespan_Years": 2.5,
        "CO2e_Materials": 10.80,
        "CO2e_Manufacturing": 2.70,
        "CO2e_Transport": 1.62,
        "CO2e_Packaging": 0.54,
        "CO2e_EOL": 0.22,
        "CO2e_Total": 15.88,
        "Water_L": 745,
        "Land_m2": 2.45,
        "Ecotox_CTUe": 160,
        "Recyclability_Score": "Low",
        "Disassembly_Difficulty": "Medium",
        "Notes": "43-row pilot addition; exact PDP and local HTML capture from archived_specs.",
    },
]


PILOT_SOURCE_ROWS = [
    {
        "Model": "Nike Book 1",
        "Brand": "Nike",
        "Category": "Basketball",
        "Product_Source_URL": "https://www.nike.com/t/book-1-scorpion-basketball-shoes-FxlwhV/HJ4388-001",
        "Price_Source_URL": "https://www.nike.com/t/book-1-scorpion-basketball-shoes-FxlwhV/HJ4388-001",
        "Accessed_Date": "2026-03-29",
        "Source_Type": "official_exact_pdp",
        "Traceability_Note": "Exact Nike Book 1 product page recovered from the archived-specs workflow.",
        "Price_Coding_Note": "Pilot dataset uses the current public list price captured from the resolved official PDP; later markdowns may differ.",
        "Mass_Basis": "Pilot stored reference mass anchored to comparable basketball footwear with partial-leather forefoot, foam + Air Zoom midsole, and rubber outsole construction.",
        "Lifespan_Basis": "Longer-life basketball screening assumption reflecting leather-assisted upper durability relative to purely textile peers.",
    },
    {
        "Model": "Puma MB.04",
        "Brand": "Puma",
        "Category": "Basketball",
        "Product_Source_URL": "https://us.puma.com/us/en/pd/mb.04-team-mens-basketball-shoes/312174?swatch=01",
        "Price_Source_URL": "https://us.puma.com/us/en/pd/mb.04-team-mens-basketball-shoes/312174?swatch=01",
        "Accessed_Date": "2026-03-29",
        "Source_Type": "official_exact_pdp",
        "Traceability_Note": "Exact PUMA MB.04 product page recovered from the archived-specs workflow.",
        "Price_Coding_Note": "Pilot dataset uses the current public list price captured from the resolved official PDP; later markdowns may differ.",
        "Mass_Basis": "Pilot stored reference mass anchored to comparable basketball footwear using a double-layered mesh upper, NITROFOAM midsole, and rubber outsole construction.",
        "Lifespan_Basis": "Standard basketball screening assumption for synthetic performance footwear.",
    },
    {
        "Model": "Nike Dunk Low",
        "Brand": "Nike",
        "Category": "Casual",
        "Product_Source_URL": "https://www.nike.com/t/dunk-low-womens-shoes-MzZlKQ/DD1503-101",
        "Price_Source_URL": "https://www.nike.com/t/dunk-low-womens-shoes-MzZlKQ/DD1503-101",
        "Accessed_Date": "2026-03-29",
        "Source_Type": "official_exact_pdp",
        "Traceability_Note": "Exact Nike Dunk Low product page recovered from the archived-specs workflow.",
        "Price_Coding_Note": "Pilot dataset uses the current public list price basis from the resolved official PDP; the live page may also surface markdowns on some colorways.",
        "Mass_Basis": "Pilot stored reference mass anchored to comparable full-leather casual sneakers using a foam midsole and rubber outsole construction.",
        "Lifespan_Basis": "Multi-year casual-use screening assumption for durable leather sneaker construction.",
    },
]


def comparison_frame(base: pd.DataFrame, pilot: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "Metric": "n",
            "Base_40": len(base),
            "Pilot_43": len(pilot),
            "Delta": len(pilot) - len(base),
        },
        {
            "Metric": "Mean_CO2e",
            "Base_40": round(float(base["CO2e_Total"].mean()), 3),
            "Pilot_43": round(float(pilot["CO2e_Total"].mean()), 3),
            "Delta": round(float(pilot["CO2e_Total"].mean() - base["CO2e_Total"].mean()), 3),
        },
        {
            "Metric": "Median_CO2e",
            "Base_40": round(float(base["CO2e_Total"].median()), 3),
            "Pilot_43": round(float(pilot["CO2e_Total"].median()), 3),
            "Delta": round(float(pilot["CO2e_Total"].median() - base["CO2e_Total"].median()), 3),
        },
        {
            "Metric": "Leather_Associated_Count",
            "Base_40": int(base["Upper_Material_Type"].isin({"Full Leather", "Partial Leather", "Synthetic Leather"}).sum()),
            "Pilot_43": int(pilot["Upper_Material_Type"].isin({"Full Leather", "Partial Leather", "Synthetic Leather"}).sum()),
            "Delta": int(
                pilot["Upper_Material_Type"].isin({"Full Leather", "Partial Leather", "Synthetic Leather"}).sum()
                - base["Upper_Material_Type"].isin({"Full Leather", "Partial Leather", "Synthetic Leather"}).sum()
            ),
        },
        {
            "Metric": "Basketball_Count",
            "Base_40": int((base["Category"] == "Basketball").sum()),
            "Pilot_43": int((pilot["Category"] == "Basketball").sum()),
            "Delta": int((pilot["Category"] == "Basketball").sum() - (base["Category"] == "Basketball").sum()),
        },
        {
            "Metric": "Casual_Count",
            "Base_40": int((base["Category"] == "Casual").sum()),
            "Pilot_43": int((pilot["Category"] == "Casual").sum()),
            "Delta": int((pilot["Category"] == "Casual").sum() - (base["Category"] == "Casual").sum()),
        },
    ]
    return pd.DataFrame(rows)


def write_summary(base: pd.DataFrame, pilot: pd.DataFrame, comparison: pd.DataFrame) -> None:
    added = pd.DataFrame(PILOT_ROWS)
    lines = [
        "# 43-Row Pilot Summary",
        "",
        "Date: 2026-03-29",
        "",
        "This pilot extends the canonical 40-row dataset with the 3 strongest round-1 model-ready candidates from archived_specs.",
        "",
        "## Added Rows",
        "",
    ]
    for row in added.itertuples(index=False):
        lines.extend(
            [
                f"- `{row.Model}`",
                f"  Category: `{row.Category}`; material type: `{row.Upper_Material_Type}`; stored mass proxy: `{row.Mass_kg:.2f}` kg; lifespan: `{row.Lifespan_Years:.1f}` years; total: `{row.CO2e_Total:.2f}` kg CO2e.",
            ]
        )
    lines.extend(
        [
            "",
            "## Dataset Delta",
            "",
            f"- Mean CO2e: `{base['CO2e_Total'].mean():.3f}` -> `{pilot['CO2e_Total'].mean():.3f}`",
            f"- Median CO2e: `{base['CO2e_Total'].median():.3f}` -> `{pilot['CO2e_Total'].median():.3f}`",
            f"- Leather-associated count: `{base['Upper_Material_Type'].isin({'Full Leather', 'Partial Leather', 'Synthetic Leather'}).sum()}` -> "
            f"`{pilot['Upper_Material_Type'].isin({'Full Leather', 'Partial Leather', 'Synthetic Leather'}).sum()}`",
            "",
            "## Files",
            "",
            "- `expanded_dataset_43_pilot.csv`",
            "- `product_source_appendix_43_pilot.csv`",
            "- `pilot_outputs/pilot_43_comparison.csv`",
            "",
            "The pilot is separate from the canonical 40-row manuscript dataset and should be treated as a workflow testbed until manually reviewed.",
        ]
    )
    PILOT_SUMMARY.write_text("\n".join(lines) + "\n")
    comparison.to_csv(PILOT_COMPARISON, index=False)


def main() -> None:
    PILOT_OUTDIR.mkdir(parents=True, exist_ok=True)

    base_dataset = pd.read_csv(BASE_DATASET)
    base_sources = pd.read_csv(BASE_SOURCES)

    pilot_dataset = pd.concat([base_dataset, pd.DataFrame(PILOT_ROWS)], ignore_index=True)
    pilot_sources = pd.concat([base_sources, pd.DataFrame(PILOT_SOURCE_ROWS)], ignore_index=True)

    pilot_dataset.to_csv(PILOT_DATASET, index=False)
    pilot_sources.to_csv(PILOT_SOURCES, index=False)

    comparison = comparison_frame(base_dataset, pilot_dataset)
    write_summary(base_dataset, pilot_dataset, comparison)


if __name__ == "__main__":
    main()
