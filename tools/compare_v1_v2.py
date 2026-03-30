#!/usr/bin/env python3
"""Compare the canonical 40-row dataset against the mass-calibrated v2 dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from scipy import stats

from analyze_expanded_dataset import load_dataset, ols


ROOT = Path(__file__).resolve().parents[1]
V1_DATASET = ROOT / "expanded_dataset_40_models.csv"
V2_DATASET = ROOT / "expanded_dataset_40_models_v2.csv"
SUMMARY_CSV = ROOT / "v1_v2_comparison.csv"
REGRESSION_CSV = ROOT / "v1_v2_regression_comparison.csv"
CATEGORY_CSV = ROOT / "v1_v2_category_comparison.csv"
SUMMARY_MD = ROOT / "v1_v2_summary.md"
REFERENCE_DATE = "2026-03-30"


def fit_main_model(df: pd.DataFrame):
    X = pd.DataFrame({"Intercept": 1.0, "Price_USD": df["Price_USD"], "Is_Leather": df["Is_Leather"]})
    return ols(df["CO2e_Total"], X)


def summary_rows(v1: pd.DataFrame, v2: pd.DataFrame) -> pd.DataFrame:
    joined = v1[["Model", "CO2e_Total"]].merge(
        v2[["Model", "CO2e_Total"]], on="Model", suffixes=("_v1", "_v2"), validate="one_to_one"
    )
    pearson = stats.pearsonr(joined["CO2e_Total_v1"], joined["CO2e_Total_v2"])
    spearman = stats.spearmanr(joined["CO2e_Total_v1"], joined["CO2e_Total_v2"])
    main_v1 = fit_main_model(v1)
    main_v2 = fit_main_model(v2)
    rows = [
        {"Metric": "n", "V1": len(v1), "V2": len(v2), "Delta": len(v2) - len(v1), "Pct_Delta": 0.0},
        {
            "Metric": "Mean_CO2e_Total",
            "V1": round(float(v1["CO2e_Total"].mean()), 3),
            "V2": round(float(v2["CO2e_Total"].mean()), 3),
            "Delta": round(float(v2["CO2e_Total"].mean() - v1["CO2e_Total"].mean()), 3),
            "Pct_Delta": round(float((v2["CO2e_Total"].mean() / v1["CO2e_Total"].mean() - 1) * 100), 1),
        },
        {
            "Metric": "Median_CO2e_Total",
            "V1": round(float(v1["CO2e_Total"].median()), 3),
            "V2": round(float(v2["CO2e_Total"].median()), 3),
            "Delta": round(float(v2["CO2e_Total"].median() - v1["CO2e_Total"].median()), 3),
            "Pct_Delta": round(float((v2["CO2e_Total"].median() / v1["CO2e_Total"].median() - 1) * 100), 1),
        },
        {
            "Metric": "Mean_Annualized_CO2e",
            "V1": round(float(v1["Annualized_CO2e"].mean()), 3),
            "V2": round(float(v2["Annualized_CO2e"].mean()), 3),
            "Delta": round(float(v2["Annualized_CO2e"].mean() - v1["Annualized_CO2e"].mean()), 3),
            "Pct_Delta": round(float((v2["Annualized_CO2e"].mean() / v1["Annualized_CO2e"].mean() - 1) * 100), 1),
        },
        {
            "Metric": "Material_Share",
            "V1": round(float(v1["CO2e_Materials"].sum() / v1["CO2e_Total"].sum()), 3),
            "V2": round(float(v2["CO2e_Materials"].sum() / v2["CO2e_Total"].sum()), 3),
            "Delta": round(float(v2["CO2e_Materials"].sum() / v2["CO2e_Total"].sum() - v1["CO2e_Materials"].sum() / v1["CO2e_Total"].sum()), 3),
            "Pct_Delta": "",
        },
        {
            "Metric": "Leather_Count",
            "V1": int(v1["Is_Leather"].sum()),
            "V2": int(v2["Is_Leather"].sum()),
            "Delta": int(v2["Is_Leather"].sum() - v1["Is_Leather"].sum()),
            "Pct_Delta": 0.0,
        },
        {
            "Metric": "Leather_Estimate",
            "V1": round(float(main_v1.coefficients.loc["Is_Leather", "coef"]), 3),
            "V2": round(float(main_v2.coefficients.loc["Is_Leather", "coef"]), 3),
            "Delta": round(float(main_v2.coefficients.loc["Is_Leather", "coef"] - main_v1.coefficients.loc["Is_Leather", "coef"]), 3),
            "Pct_Delta": round(float((main_v2.coefficients.loc["Is_Leather", "coef"] / main_v1.coefficients.loc["Is_Leather", "coef"] - 1) * 100), 1),
        },
        {
            "Metric": "Price_Coefficient",
            "V1": round(float(main_v1.coefficients.loc["Price_USD", "coef"]), 5),
            "V2": round(float(main_v2.coefficients.loc["Price_USD", "coef"]), 5),
            "Delta": round(float(main_v2.coefficients.loc["Price_USD", "coef"] - main_v1.coefficients.loc["Price_USD", "coef"]), 5),
            "Pct_Delta": round(float((main_v2.coefficients.loc["Price_USD", "coef"] / main_v1.coefficients.loc["Price_USD", "coef"] - 1) * 100), 1),
        },
        {
            "Metric": "R2",
            "V1": round(float(main_v1.r2), 3),
            "V2": round(float(main_v2.r2), 3),
            "Delta": round(float(main_v2.r2 - main_v1.r2), 3),
            "Pct_Delta": "",
        },
        {
            "Metric": "Pearson_Rowwise_CO2e",
            "V1": "",
            "V2": round(float(pearson.statistic), 3),
            "Delta": "",
            "Pct_Delta": "",
        },
        {
            "Metric": "Spearman_Rowwise_CO2e",
            "V1": "",
            "V2": round(float(spearman.statistic), 3),
            "Delta": "",
            "Pct_Delta": "",
        },
    ]
    return pd.DataFrame(rows)


def regression_rows(v1: pd.DataFrame, v2: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for label, df in [("V1", v1), ("V2", v2)]:
        result = fit_main_model(df)
        for term in ["Intercept", "Price_USD", "Is_Leather"]:
            coef = result.coefficients.loc[term]
            rows.append(
                {
                    "Dataset": label,
                    "Term": term,
                    "Coef": round(float(coef["coef"]), 5),
                    "SE": round(float(coef["se"]), 5),
                    "T": round(float(coef["t"]), 3),
                    "P": round(float(coef["p"]), 6),
                    "R2": round(float(result.r2), 3),
                    "Adjusted_R2": round(float(result.adjusted_r2), 3),
                }
            )
    return pd.DataFrame(rows)


def category_rows(v1: pd.DataFrame, v2: pd.DataFrame) -> pd.DataFrame:
    left = v1.groupby("Category")["CO2e_Total"].agg(n_v1="count", mean_v1="mean", median_v1="median")
    right = v2.groupby("Category")["CO2e_Total"].agg(n_v2="count", mean_v2="mean", median_v2="median")
    merged = left.join(right, how="outer").reset_index()
    merged["mean_delta"] = merged["mean_v2"] - merged["mean_v1"]
    merged["median_delta"] = merged["median_v2"] - merged["median_v1"]
    for col in ["mean_v1", "median_v1", "mean_v2", "median_v2", "mean_delta", "median_delta"]:
        merged[col] = merged[col].round(3)
    return merged


def write_summary(v1: pd.DataFrame, v2: pd.DataFrame, overall: pd.DataFrame, categories: pd.DataFrame) -> None:
    top_increase = (
        v1[["Model", "CO2e_Total"]]
        .merge(v2[["Model", "CO2e_Total"]], on="Model", suffixes=("_v1", "_v2"))
        .assign(delta=lambda d: d["CO2e_Total_v2"] - d["CO2e_Total_v1"])
        .sort_values("delta", ascending=False)
        .head(5)
    )
    leather_v1 = float(overall.loc[overall["Metric"] == "Leather_Estimate", "V1"].iloc[0])
    leather_v2 = float(overall.loc[overall["Metric"] == "Leather_Estimate", "V2"].iloc[0])
    lines = [
        "# V1 vs V2 Comparison Summary",
        "",
        f"Date: {REFERENCE_DATE}",
        "",
        "This comparison contrasts the canonical 40-row screening release (`v1`) with the mass-calibrated pair-basis sensitivity release (`v2`).",
        "",
        "## Headline Changes",
        "",
        f"- Mean CO2e total: `{overall.loc[overall['Metric'] == 'Mean_CO2e_Total', 'V1'].iloc[0]:.3f}` -> `{overall.loc[overall['Metric'] == 'Mean_CO2e_Total', 'V2'].iloc[0]:.3f}`",
        f"- Median CO2e total: `{overall.loc[overall['Metric'] == 'Median_CO2e_Total', 'V1'].iloc[0]:.3f}` -> `{overall.loc[overall['Metric'] == 'Median_CO2e_Total', 'V2'].iloc[0]:.3f}`",
        f"- Leather coefficient: `{leather_v1:.3f}` -> `{leather_v2:.3f}`",
        f"- Row-wise Spearman correlation: `{overall.loc[overall['Metric'] == 'Spearman_Rowwise_CO2e', 'V2'].iloc[0]:.3f}`",
        "",
        "## Category Means",
        "",
    ]
    for row in categories.itertuples(index=False):
        lines.append(f"- `{row.Category}`: `{row.mean_v1:.3f}` -> `{row.mean_v2:.3f}` kg CO2e")
    lines.extend(["", "## Largest Row-Level Increases", ""])
    for row in top_increase.itertuples(index=False):
        lines.append(f"- `{row.Model}`: `{row.CO2e_Total_v1:.2f}` -> `{row.CO2e_Total_v2:.2f}` kg CO2e (`+{row.delta:.2f}`)")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "V2 preserves much of the row ordering but materially raises absolute totals because most rows move from a stored reference-mass proxy to an explicit pair mass. It should therefore be treated as a sensitivity release rather than as a drop-in replacement for v1.",
        ]
    )
    SUMMARY_MD.write_text("\n".join(lines) + "\n")


def main() -> None:
    v1 = load_dataset(V1_DATASET)
    v2 = load_dataset(V2_DATASET)

    overall = summary_rows(v1, v2)
    regressions = regression_rows(v1, v2)
    categories = category_rows(v1, v2)

    overall.to_csv(SUMMARY_CSV, index=False)
    regressions.to_csv(REGRESSION_CSV, index=False)
    categories.to_csv(CATEGORY_CSV, index=False)
    write_summary(v1, v2, overall, categories)


if __name__ == "__main__":
    main()
