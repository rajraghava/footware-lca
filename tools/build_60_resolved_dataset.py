#!/usr/bin/env python3
"""Build a 60-row fast-path dataset from all currently source-resolved expansion rows."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
BASE_DATASET = ROOT / "expanded_dataset_40_models.csv"
BASE_SOURCES = ROOT / "product_source_appendix_40_models.csv"
PILOT_DATASET = ROOT / "expanded_dataset_43_pilot.csv"
PILOT_SOURCES = ROOT / "product_source_appendix_43_pilot.csv"
SCAFFOLD = ROOT / "archived_specs" / "expansion_100_model_scaffold.csv"

RESOLVED_DATASET = ROOT / "expanded_dataset_60_resolved.csv"
RESOLVED_SOURCES = ROOT / "product_source_appendix_60_resolved.csv"
PILOT_OUTDIR = ROOT / "pilot_outputs"
RESOLVED_SUMMARY = PILOT_OUTDIR / "resolved_60_summary.md"
RESOLVED_COMPARISON = PILOT_OUTDIR / "resolved_60_comparison.csv"
RESOLVED_NEW_ROWS = PILOT_OUTDIR / "resolved_60_new_rows.csv"

LEATHER_TYPES = {"Full Leather", "Partial Leather", "Synthetic Leather"}
PILOT_MODELS = {"Nike Book 1", "Puma MB.04", "Nike Dunk Low"}
RESOLVED_STATUSES = {
    "round1_model_ready_candidate",
    "resolved_round1_source_validated",
    "resolved_round2_source_validated",
}

REFERENCE_DATE = "2026-03-29"


FAST_PATH_SPECS = [
    {
        "Model": "New Balance Fresh Foam BB v3",
        "Brand": "New Balance",
        "Category": "Basketball",
        "Upper_Material": "Breathable mesh upper",
        "Upper_Material_Type": "Synthetic Textile",
        "Midsole": "Fresh Foam X",
        "Outsole": "Rubber",
        "Mass_kg": 0.36,
        "Price_USD": 129.99,
        "Lifespan_Years": 1.5,
        "Recyclability_Score": "Medium",
        "Disassembly_Difficulty": "High",
        "Notes": "60-row resolved fast-path addition; modeled from basketball synthetic-textile archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to comparable basketball footwear using a breathable mesh upper, Fresh Foam X midsole, and rubber outsole construction; the current official snippet did not surface a stable disclosed weight.",
        "Lifespan_Basis": "Moderate-use screening assumption for versatile basketball performance footwear.",
    },
    {
        "Model": "Nike Ja 2",
        "Brand": "Nike",
        "Category": "Basketball",
        "Upper_Material": "Performance textile upper",
        "Upper_Material_Type": "Synthetic Textile",
        "Midsole": "Lightweight foam + Air Zoom",
        "Outsole": "Rubber",
        "Mass_kg": 0.35,
        "Price_USD": 125.00,
        "Lifespan_Years": 1.5,
        "Recyclability_Score": "Medium",
        "Disassembly_Difficulty": "High",
        "Notes": "60-row resolved fast-path addition; modeled from basketball synthetic-textile archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to comparable basketball footwear using a textile upper, lightweight foam, forefoot Air Zoom, and rubber outsole construction.",
        "Lifespan_Basis": "Moderate-use screening assumption for versatile basketball performance footwear.",
    },
    {
        "Model": "Under Armour Curry Fox 1",
        "Brand": "Under Armour",
        "Category": "Basketball",
        "Upper_Material": "Lightweight upper with molded strap",
        "Upper_Material_Type": "Synthetic Textile",
        "Midsole": "UA Flow",
        "Outsole": "Rubber",
        "Mass_kg": 0.34,
        "Price_USD": 120.00,
        "Lifespan_Years": 1.5,
        "Recyclability_Score": "Medium",
        "Disassembly_Difficulty": "High",
        "Notes": "60-row resolved fast-path addition; modeled from basketball synthetic-textile archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to comparable basketball footwear using a lightweight strapped upper, Flow-type midsole architecture, and rubber traction elements.",
        "Lifespan_Basis": "Moderate-use screening assumption for versatile basketball performance footwear.",
    },
    {
        "Model": "Adidas Samba OG",
        "Brand": "Adidas",
        "Category": "Casual",
        "Upper_Material": "Leather upper + suede overlays",
        "Upper_Material_Type": "Full Leather",
        "Midsole": "Foam",
        "Outsole": "Rubber",
        "Mass_kg": 0.35,
        "Price_USD": 100.00,
        "Lifespan_Years": 2.5,
        "Recyclability_Score": "Low",
        "Disassembly_Difficulty": "Medium",
        "Notes": "60-row resolved fast-path addition; modeled from casual full-leather archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to comparable casual footwear using a leather upper with suede overlays, a low-profile foam midsole, and a rubber outsole construction.",
        "Lifespan_Basis": "Extended casual-use screening assumption for durable leather lifestyle sneakers.",
    },
    {
        "Model": "Nike Cortez",
        "Brand": "Nike",
        "Category": "Casual",
        "Upper_Material": "Leather upper",
        "Upper_Material_Type": "Full Leather",
        "Midsole": "Foam",
        "Outsole": "Rubber",
        "Mass_kg": 0.35,
        "Price_USD": 105.00,
        "Lifespan_Years": 2.5,
        "Recyclability_Score": "Low",
        "Disassembly_Difficulty": "Medium",
        "Notes": "60-row resolved fast-path addition; modeled from casual full-leather archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to comparable casual footwear using a leather upper, foam midsole, and rubber outsole construction.",
        "Lifespan_Basis": "Extended casual-use screening assumption for durable leather lifestyle sneakers.",
    },
    {
        "Model": "Vans Knu Skool",
        "Brand": "Vans",
        "Category": "Casual",
        "Upper_Material": "Suede upper",
        "Upper_Material_Type": "Full Leather",
        "Midsole": "Foam",
        "Outsole": "Vulcanized rubber",
        "Mass_kg": 0.39,
        "Price_USD": 85.00,
        "Lifespan_Years": 2.0,
        "Recyclability_Score": "Low",
        "Disassembly_Difficulty": "Medium",
        "Notes": "60-row resolved fast-path addition; modeled from casual full-leather archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to comparable casual footwear using a suede upper, padded collar, foam interior, and vulcanized rubber outsole construction.",
        "Lifespan_Basis": "Longer-life casual screening assumption for suede-heavy skate-inspired lifestyle footwear.",
    },
    {
        "Model": "ASICS Gel-Nimbus 27",
        "Brand": "ASICS",
        "Category": "Running",
        "Upper_Material": "Engineered jacquard mesh",
        "Upper_Material_Type": "Synthetic Textile",
        "Midsole": "FF BLAST PLUS",
        "Outsole": "HYBRID ASICSGRIP",
        "Mass_kg": 0.305,
        "Price_USD": 165.00,
        "Lifespan_Years": 1.0,
        "Recyclability_Score": "Medium",
        "Disassembly_Difficulty": "High",
        "Notes": "60-row resolved fast-path addition; modeled from running synthetic-textile archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to the current official disclosed shoe weight carried forward in the existing dataset's running-weight convention.",
        "Lifespan_Basis": "Daily-use screening assumption for high-mileage performance footwear.",
    },
    {
        "Model": "ASICS Novablast 5",
        "Brand": "ASICS",
        "Category": "Running",
        "Upper_Material": "Engineered jacquard mesh",
        "Upper_Material_Type": "Synthetic Textile",
        "Midsole": "FF BLAST MAX",
        "Outsole": "Rubber",
        "Mass_kg": 0.255,
        "Price_USD": 150.00,
        "Lifespan_Years": 1.0,
        "Recyclability_Score": "Medium",
        "Disassembly_Difficulty": "High",
        "Notes": "60-row resolved fast-path addition; modeled from running synthetic-textile archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to the current official disclosed shoe weight carried forward in the existing dataset's running-weight convention.",
        "Lifespan_Basis": "Daily-use screening assumption for high-mileage performance footwear.",
    },
    {
        "Model": "Brooks Glycerin 22",
        "Brand": "Brooks",
        "Category": "Running",
        "Upper_Material": "Engineered jacquard knit",
        "Upper_Material_Type": "Synthetic Textile",
        "Midsole": "DNA Tuned",
        "Outsole": "Rubber",
        "Mass_kg": 0.289,
        "Price_USD": 165.00,
        "Lifespan_Years": 1.0,
        "Recyclability_Score": "Medium",
        "Disassembly_Difficulty": "High",
        "Notes": "60-row resolved fast-path addition; modeled from running synthetic-textile archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to the current official disclosed shoe weight carried forward in the existing dataset's running-weight convention.",
        "Lifespan_Basis": "Daily-use screening assumption for high-mileage performance footwear.",
    },
    {
        "Model": "Hoka Bondi 9",
        "Brand": "Hoka",
        "Category": "Running",
        "Upper_Material": "Engineered mesh upper",
        "Upper_Material_Type": "Synthetic Textile",
        "Midsole": "Super critical foam",
        "Outsole": "Durabrasion rubber",
        "Mass_kg": 0.297,
        "Price_USD": 175.00,
        "Lifespan_Years": 1.0,
        "Recyclability_Score": "Medium",
        "Disassembly_Difficulty": "High",
        "Notes": "60-row resolved fast-path addition; modeled from running synthetic-textile archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to the current official disclosed shoe weight carried forward in the existing dataset's running-weight convention.",
        "Lifespan_Basis": "Daily-use screening assumption for high-mileage performance footwear.",
    },
    {
        "Model": "Hoka Mach 6",
        "Brand": "Hoka",
        "Category": "Running",
        "Upper_Material": "Creel jacquard upper",
        "Upper_Material_Type": "Synthetic Textile",
        "Midsole": "Super critical foam",
        "Outsole": "Rubber",
        "Mass_kg": 0.189,
        "Price_USD": 140.00,
        "Lifespan_Years": 1.0,
        "Recyclability_Score": "Medium",
        "Disassembly_Difficulty": "High",
        "Notes": "60-row resolved fast-path addition; modeled from running synthetic-textile archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to the current official disclosed shoe weight carried forward in the existing dataset's running-weight convention.",
        "Lifespan_Basis": "Daily-use screening assumption for high-mileage performance footwear.",
    },
    {
        "Model": "Nike Vomero 18",
        "Brand": "Nike",
        "Category": "Running",
        "Upper_Material": "Engineered mesh upper",
        "Upper_Material_Type": "Synthetic Textile",
        "Midsole": "ZoomX + ReactX",
        "Outsole": "Rubber",
        "Mass_kg": 0.325,
        "Price_USD": 155.00,
        "Lifespan_Years": 1.0,
        "Recyclability_Score": "Medium",
        "Disassembly_Difficulty": "High",
        "Notes": "60-row resolved fast-path addition; modeled from running synthetic-textile archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to the current official disclosed shoe weight carried forward in the existing dataset's running-weight convention.",
        "Lifespan_Basis": "Daily-use screening assumption for high-mileage performance footwear.",
    },
    {
        "Model": "On Cloudsurfer 2",
        "Brand": "On",
        "Category": "Running",
        "Upper_Material": "Recycled polyester upper",
        "Upper_Material_Type": "Recycled Synthetic",
        "Midsole": "CloudTec Phase + Helion",
        "Outsole": "Rubber",
        "Mass_kg": 0.261,
        "Price_USD": 160.00,
        "Lifespan_Years": 1.0,
        "Recyclability_Score": "High",
        "Disassembly_Difficulty": "Medium",
        "Notes": "60-row resolved fast-path addition; modeled from running recycled-synthetic archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to the current official disclosed shoe weight carried forward in the existing dataset's running-weight convention.",
        "Lifespan_Basis": "Daily-use screening assumption for high-mileage performance footwear.",
    },
    {
        "Model": "Adidas F50 Elite",
        "Brand": "Adidas",
        "Category": "Soccer",
        "Upper_Material": "Speed-focused synthetic upper",
        "Upper_Material_Type": "Synthetic Textile",
        "Midsole": "Foam",
        "Outsole": "Rubber",
        "Mass_kg": 0.26,
        "Price_USD": 260.00,
        "Lifespan_Years": 1.5,
        "Recyclability_Score": "Medium",
        "Disassembly_Difficulty": "High",
        "Notes": "60-row resolved fast-path addition; modeled from soccer synthetic-textile archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to comparable elite speed boots using a lightweight synthetic upper and rubberized firm-ground outsole construction.",
        "Lifespan_Basis": "Moderate-use screening assumption for elite synthetic soccer footwear.",
    },
    {
        "Model": "New Balance 442 v2 Team",
        "Brand": "New Balance",
        "Category": "Soccer",
        "Upper_Material": "Premium full-grain leather",
        "Upper_Material_Type": "Full Leather",
        "Midsole": "Foam",
        "Outsole": "Rubber",
        "Mass_kg": 0.31,
        "Price_USD": 99.99,
        "Lifespan_Years": 2.0,
        "Recyclability_Score": "Low",
        "Disassembly_Difficulty": "Medium",
        "Notes": "60-row resolved fast-path addition; modeled from soccer full-leather archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to comparable full-leather soccer footwear using a premium leather upper and lightweight plate/outsole construction.",
        "Lifespan_Basis": "Longer-life screening assumption for sturdier leather soccer footwear.",
    },
    {
        "Model": "Nike Mercurial Vapor 16 Elite",
        "Brand": "Nike",
        "Category": "Soccer",
        "Upper_Material": "Gripknit + Flyknit upper",
        "Upper_Material_Type": "Synthetic Textile",
        "Midsole": "Air Zoom",
        "Outsole": "Rubber",
        "Mass_kg": 0.23,
        "Price_USD": 280.00,
        "Lifespan_Years": 1.5,
        "Recyclability_Score": "Medium",
        "Disassembly_Difficulty": "High",
        "Notes": "60-row resolved fast-path addition; modeled from soccer synthetic-textile archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to comparable elite speed boots using a knit-based synthetic upper, Air Zoom platform, and lightweight outsole construction.",
        "Lifespan_Basis": "Moderate-use screening assumption for elite synthetic soccer footwear.",
    },
    {
        "Model": "Puma Ultra 5 Ultimate",
        "Brand": "Puma",
        "Category": "Soccer",
        "Upper_Material": "GripControl Pro skin + PWRTAPE",
        "Upper_Material_Type": "Synthetic Textile",
        "Midsole": "Foam",
        "Outsole": "Rubber",
        "Mass_kg": 0.22,
        "Price_USD": 230.00,
        "Lifespan_Years": 1.5,
        "Recyclability_Score": "Medium",
        "Disassembly_Difficulty": "High",
        "Notes": "60-row resolved fast-path addition; modeled from soccer synthetic-textile archetype using current official source data from archived_specs.",
        "Mass_Basis": "Fast-path reference mass anchored to comparable elite speed boots using a thin synthetic support skin, PWRTAPE frame, and lightweight outsole construction.",
        "Lifespan_Basis": "Moderate-use screening assumption for elite synthetic soccer footwear.",
    },
]


def get_archetype_table(base: pd.DataFrame) -> dict[tuple[str, str], dict[str, float]]:
    table: dict[tuple[str, str], dict[str, float]] = {}
    metrics = [
        "CO2e_Materials",
        "CO2e_Manufacturing",
        "CO2e_Transport",
        "CO2e_Packaging",
        "CO2e_EOL",
        "Water_L",
        "Land_m2",
        "Ecotox_CTUe",
    ]
    grouped = base.groupby(["Category", "Upper_Material_Type"])
    for key, frame in grouped:
        mean_mass = frame["Mass_kg"].mean()
        values = {"Mass_kg": mean_mass}
        for metric in metrics:
            values[metric] = float(frame[metric].mean() / mean_mass)
        table[key] = values
    return table


def round_land(value: float) -> float:
    return round(value, 2)


def round_ecotox(value: float) -> int:
    return int(round(value))


def build_modeled_row(spec: dict[str, object], archetypes: dict[tuple[str, str], dict[str, float]]) -> dict[str, object]:
    key = (str(spec["Category"]), str(spec["Upper_Material_Type"]))
    intensity = archetypes[key]
    mass = float(spec["Mass_kg"])
    row = dict(spec)
    row["CO2e_Materials"] = round(mass * intensity["CO2e_Materials"], 2)
    row["CO2e_Manufacturing"] = round(mass * intensity["CO2e_Manufacturing"], 2)
    row["CO2e_Transport"] = round(mass * intensity["CO2e_Transport"], 2)
    row["CO2e_Packaging"] = round(mass * intensity["CO2e_Packaging"], 2)
    row["CO2e_EOL"] = round(mass * intensity["CO2e_EOL"], 2)
    row["CO2e_Total"] = round(
        row["CO2e_Materials"]
        + row["CO2e_Manufacturing"]
        + row["CO2e_Transport"]
        + row["CO2e_Packaging"]
        + row["CO2e_EOL"],
        2,
    )
    row["Water_L"] = int(round(mass * intensity["Water_L"]))
    row["Land_m2"] = round_land(mass * intensity["Land_m2"])
    row["Ecotox_CTUe"] = round_ecotox(mass * intensity["Ecotox_CTUe"])
    return row


def canonical_row_order(base: pd.DataFrame) -> list[str]:
    return list(base.columns)


def append_in_category_blocks(base: pd.DataFrame, added_rows: pd.DataFrame) -> pd.DataFrame:
    ordered_frames = []
    for category in ["Basketball", "Casual", "Running", "Soccer"]:
        ordered_frames.append(base[base["Category"] == category])
        ordered_frames.append(added_rows[added_rows["Category"] == category])
    return pd.concat(ordered_frames, ignore_index=True)


def build_traceability_note(scaffold_row: pd.Series) -> str:
    source_type = scaffold_row["Source_Entry_Type"]
    brand = scaffold_row["Brand"]
    model = scaffold_row["Model"]
    if source_type == "official_exact_pdp":
        return f"Resolved official {brand} product page used for {model}; source trail preserved through the archived-specs workflow."
    if source_type == "official_collection_page":
        return f"Resolved official {brand} model-family or collection page used for {model}; exact single-SKU archival remains incomplete."
    if source_type == "official_regional_pdp":
        return f"Resolved official regional {brand} PDP used for {model}; it acts as the current best official proxy within the archived-specs workflow."
    return f"Resolved official {brand} source used for {model}; archival details are tracked through the archived-specs workflow."


def build_price_note(scaffold_row: pd.Series, used_price: float) -> str:
    captured = scaffold_row["MSRP_USD_At_Capture"]
    if pd.notna(captured):
        return f"Fast-path dataset uses the current public price captured from the resolved official source (`{float(captured):.2f}` USD basis) and keeps that screening value fixed for reproducibility."
    return f"Fast-path dataset uses the resolved official-source price anchor adopted during the 2026-03-29 expansion workflow (`{used_price:.2f}` USD screening basis); the live page did not preserve a clean USD MSRP field in the scaffold."


def build_source_row(spec: dict[str, object], scaffold_row: pd.Series) -> dict[str, object]:
    return {
        "Model": spec["Model"],
        "Brand": spec["Brand"],
        "Category": spec["Category"],
        "Product_Source_URL": scaffold_row["Official_Source_URL"],
        "Price_Source_URL": scaffold_row["Official_Source_URL"],
        "Accessed_Date": REFERENCE_DATE,
        "Source_Type": scaffold_row["Source_Entry_Type"],
        "Traceability_Note": build_traceability_note(scaffold_row),
        "Price_Coding_Note": build_price_note(scaffold_row, float(spec["Price_USD"])),
        "Mass_Basis": spec["Mass_Basis"],
        "Lifespan_Basis": spec["Lifespan_Basis"],
    }


def comparison_frame(base: pd.DataFrame, resolved: pd.DataFrame, new_rows: pd.DataFrame, sources: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {"Metric": "n", "Base_40": len(base), "Resolved_60": len(resolved), "Delta": len(resolved) - len(base)},
        {
            "Metric": "Mean_CO2e",
            "Base_40": round(float(base["CO2e_Total"].mean()), 3),
            "Resolved_60": round(float(resolved["CO2e_Total"].mean()), 3),
            "Delta": round(float(resolved["CO2e_Total"].mean() - base["CO2e_Total"].mean()), 3),
        },
        {
            "Metric": "Median_CO2e",
            "Base_40": round(float(base["CO2e_Total"].median()), 3),
            "Resolved_60": round(float(resolved["CO2e_Total"].median()), 3),
            "Delta": round(float(resolved["CO2e_Total"].median() - base["CO2e_Total"].median()), 3),
        },
        {
            "Metric": "Leather_Associated_Count",
            "Base_40": int(base["Upper_Material_Type"].isin(LEATHER_TYPES).sum()),
            "Resolved_60": int(resolved["Upper_Material_Type"].isin(LEATHER_TYPES).sum()),
            "Delta": int(resolved["Upper_Material_Type"].isin(LEATHER_TYPES).sum() - base["Upper_Material_Type"].isin(LEATHER_TYPES).sum()),
        },
        {
            "Metric": "Added_Resolved_Rows",
            "Base_40": 0,
            "Resolved_60": len(new_rows),
            "Delta": len(new_rows),
        },
    ]
    for category in ["Basketball", "Casual", "Running", "Soccer"]:
        rows.append(
            {
                "Metric": f"{category}_Count",
                "Base_40": int((base["Category"] == category).sum()),
                "Resolved_60": int((resolved["Category"] == category).sum()),
                "Delta": int((resolved["Category"] == category).sum() - (base["Category"] == category).sum()),
            }
        )
    for source_type in ["official_exact_pdp", "official_collection_page", "official_regional_pdp"]:
        rows.append(
            {
                "Metric": f"Added_{source_type}",
                "Base_40": 0,
                "Resolved_60": int((sources["Source_Type"] == source_type).sum()),
                "Delta": int((sources["Source_Type"] == source_type).sum()),
            }
        )
    return pd.DataFrame(rows)


def write_summary(base: pd.DataFrame, resolved: pd.DataFrame, new_rows: pd.DataFrame, new_sources: pd.DataFrame) -> None:
    source_counts = new_sources["Source_Type"].value_counts().to_dict()
    lines = [
        "# 60-Row Resolved Fast-Path Summary",
        "",
        f"Date: {REFERENCE_DATE}",
        "",
        "This dataset extends the canonical 40-row manuscript line with every currently source-resolved expansion candidate from `archived_specs`, without waiting for the remaining manual browser queue or unresolved search-entry rows.",
        "",
        "## Added Rows",
        "",
    ]
    for category in ["Basketball", "Casual", "Running", "Soccer"]:
        frame = new_rows[new_rows["Category"] == category]
        if frame.empty:
            continue
        lines.append(f"### {category}")
        lines.append("")
        for row in frame.itertuples(index=False):
            lines.append(
                f"- `{row.Model}`: `{row.Upper_Material_Type}`, `{row.Mass_kg:.3f}` kg reference mass, `{row.Lifespan_Years:.1f}`-year lifespan, `{row.CO2e_Total:.2f}` kg CO2e."
            )
        lines.append("")
    lines.extend(
        [
            "## Dataset Delta",
            "",
            f"- Mean CO2e: `{base['CO2e_Total'].mean():.3f}` -> `{resolved['CO2e_Total'].mean():.3f}`",
            f"- Median CO2e: `{base['CO2e_Total'].median():.3f}` -> `{resolved['CO2e_Total'].median():.3f}`",
            f"- Leather-associated count: `{base['Upper_Material_Type'].isin(LEATHER_TYPES).sum()}` -> `{resolved['Upper_Material_Type'].isin(LEATHER_TYPES).sum()}`",
            "",
            "## Added Source Tiers",
            "",
            f"- `official_exact_pdp`: `{source_counts.get('official_exact_pdp', 0)}`",
            f"- `official_collection_page`: `{source_counts.get('official_collection_page', 0)}`",
            f"- `official_regional_pdp`: `{source_counts.get('official_regional_pdp', 0)}`",
            "",
            "## Files",
            "",
            "- `expanded_dataset_60_resolved.csv`",
            "- `product_source_appendix_60_resolved.csv`",
            "- `pilot_outputs/resolved_60_new_rows.csv`",
            "- `pilot_outputs/resolved_60_comparison.csv`",
            "",
            "This 60-row file is a fast-path modeled extension, not the canonical manuscript dataset and not a finished 100-row release.",
        ]
    )
    RESOLVED_SUMMARY.write_text("\n".join(lines) + "\n")


def main() -> None:
    PILOT_OUTDIR.mkdir(parents=True, exist_ok=True)

    base_dataset = pd.read_csv(BASE_DATASET)
    base_sources = pd.read_csv(BASE_SOURCES)
    pilot_dataset = pd.read_csv(PILOT_DATASET)
    pilot_sources = pd.read_csv(PILOT_SOURCES)
    scaffold = pd.read_csv(SCAFFOLD)

    pilot_rows = pilot_dataset[pilot_dataset["Model"].isin(PILOT_MODELS)].copy()
    pilot_source_rows = pilot_sources[pilot_sources["Model"].isin(PILOT_MODELS)].copy()

    scaffold_resolved = scaffold[scaffold["Sample_Status"].isin(RESOLVED_STATUSES)].copy()
    fast_path_specs = [spec for spec in FAST_PATH_SPECS if spec["Model"] not in PILOT_MODELS]

    archetypes = get_archetype_table(base_dataset)
    modeled_rows = []
    modeled_source_rows = []

    for spec in fast_path_specs:
        scaffold_row = scaffold_resolved.loc[scaffold_resolved["Model"] == spec["Model"]]
        if scaffold_row.empty:
            raise ValueError(f"Missing scaffold row for {spec['Model']}")
        scaffold_series = scaffold_row.iloc[0]
        modeled_rows.append(build_modeled_row(spec, archetypes))
        modeled_source_rows.append(build_source_row(spec, scaffold_series))

    added_rows = pd.concat([pilot_rows, pd.DataFrame(modeled_rows)], ignore_index=True)
    added_sources = pd.concat([pilot_source_rows, pd.DataFrame(modeled_source_rows)], ignore_index=True)

    dataset = append_in_category_blocks(base_dataset, added_rows)
    sources = pd.concat([base_sources, added_sources], ignore_index=True)

    column_order = canonical_row_order(base_dataset)
    dataset = dataset[column_order]

    comparison = comparison_frame(base_dataset, dataset, added_rows, added_sources)

    dataset.to_csv(RESOLVED_DATASET, index=False)
    sources.to_csv(RESOLVED_SOURCES, index=False)
    added_rows.to_csv(RESOLVED_NEW_ROWS, index=False)
    comparison.to_csv(RESOLVED_COMPARISON, index=False)
    write_summary(base_dataset, dataset, added_rows, added_sources)


if __name__ == "__main__":
    main()
