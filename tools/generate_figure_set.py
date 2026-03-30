#!/usr/bin/env python3
"""Generate journal-style figures for the 40-model footwear manuscript."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("MPLCONFIGDIR", "/tmp/footware-design-mplconfig")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/footware-design-cache")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch


DATASET = ROOT / "expanded_dataset_40_models.csv"
FIGURE_DIR = ROOT / "figures"
OVERVIEW_PATH = ROOT / "strengthening_analysis_figures.png"

CATEGORY_ORDER = ["Running", "Basketball", "Casual", "Soccer"]
MATERIAL_ORDER = [
    "Full Leather",
    "Partial Leather",
    "Synthetic Leather",
    "Synthetic Textile",
    "Recycled Synthetic",
    "Natural Textile",
]

MATERIAL_PALETTE = {
    "Full Leather": "#8C3B2A",
    "Partial Leather": "#C27B57",
    "Synthetic Leather": "#D8A048",
    "Synthetic Textile": "#5A7D9A",
    "Recycled Synthetic": "#2A9D8F",
    "Natural Textile": "#7A8F3B",
}
LEATHER_GROUP_PALETTE = {
    "Leather-associated": "#9B3D2E",
    "Non-leather": "#2F6B7D",
}
CATEGORY_MARKERS = {
    "Running": "o",
    "Basketball": "s",
    "Casual": "D",
    "Soccer": "^",
}


def apply_theme() -> None:
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "figure.facecolor": "#F7F3EC",
            "axes.facecolor": "#FCFBF8",
            "axes.edgecolor": "#3B352F",
            "axes.labelcolor": "#231F1C",
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.labelsize": 10.5,
            "xtick.color": "#231F1C",
            "ytick.color": "#231F1C",
            "text.color": "#231F1C",
            "font.family": "DejaVu Serif",
            "grid.color": "#D8D1C7",
            "grid.linestyle": "-",
            "grid.linewidth": 0.7,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": True,
            "axes.spines.bottom": True,
        }
    )


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATASET)
    df["Is_Leather"] = df["Upper_Material_Type"].isin(
        ["Full Leather", "Partial Leather", "Synthetic Leather"]
    )
    df["Leather_Group"] = np.where(df["Is_Leather"], "Leather-associated", "Non-leather")
    df["Upper_Material_Type"] = pd.Categorical(
        df["Upper_Material_Type"], categories=MATERIAL_ORDER, ordered=True
    )
    df["Category"] = pd.Categorical(df["Category"], categories=CATEGORY_ORDER, ordered=True)
    return df


def finish_figure(fig: plt.Figure, title: str, subtitle: str | None = None) -> None:
    fig.suptitle(title, x=0.04, y=0.978, ha="left", va="top", fontsize=16.5, fontweight="bold")
    if subtitle:
        fig.text(0.04, 0.942, subtitle, ha="left", va="top", fontsize=10.0, color="#4D463E")
    fig.subplots_adjust(top=0.87)


def save_figure(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=320, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def annotate_panel(ax: plt.Axes, label: str) -> None:
    ax.text(
        0.0,
        1.02,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=11,
        fontweight="bold",
        color="#5B5249",
    )


def draw_workflow_box(
    ax: plt.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    title: str,
    lines: list[str],
    *,
    facecolor: str,
    edgecolor: str = "#5A5148",
) -> None:
    x, y = xy
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.018,rounding_size=0.03",
        linewidth=1.2,
        facecolor=facecolor,
        edgecolor=edgecolor,
    )
    ax.add_patch(patch)
    ax.text(
        x + 0.02,
        y + height - 0.035,
        title,
        ha="left",
        va="top",
        fontsize=9.8,
        fontweight="bold",
        color="#2E2924",
    )
    ax.text(
        x + 0.02,
        y + height - 0.082,
        "\n".join(lines),
        ha="left",
        va="top",
        fontsize=8.3,
        color="#3E3730",
        linespacing=1.18,
    )


def draw_workflow_arrow(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: str = "#8A6F54",
) -> None:
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=13,
        linewidth=1.4,
        color=color,
        shrinkA=4,
        shrinkB=4,
        connectionstyle="arc3,rad=0.0",
    )
    ax.add_patch(arrow)


def plot_methodology_figure() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(12.4, 7.8))
    fig.patch.set_facecolor("#F7F3EC")
    ax.set_facecolor("#FCFBF8")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.5,
        0.855,
        "Sample and Model Setup",
        ha="center",
        va="center",
        fontsize=10.2,
        fontweight="bold",
        color="#6A5E51",
    )
    ax.text(
        0.5,
        0.565,
        "Impact Assessment and Statistical Evaluation",
        ha="center",
        va="center",
        fontsize=10.2,
        fontweight="bold",
        color="#6A5E51",
    )
    ax.text(
        0.5,
        0.255,
        "Released Reproducibility Package",
        ha="center",
        va="center",
        fontsize=10.2,
        fontweight="bold",
        color="#6A5E51",
    )

    boxes = [
        (
            (0.05, 0.64),
            0.24,
            0.15,
            "1. Product Sampling",
            [
                "40 models from 16 brands",
                "4 categories, 10 per category",
                "Purposive U.S.-market sample",
            ],
            "#E8DCCB",
        ),
        (
            (0.38, 0.64),
            0.24,
            0.15,
            "2. Coding and Inputs",
            [
                "Brand, category, and price",
                "Lifespan and upper material",
                "Leather-associated indicator",
            ],
            "#DCE8EF",
        ),
        (
            (0.71, 0.64),
            0.24,
            0.15,
            "3. Screening LCA Model",
            [
                "Functional unit: one pair",
                "Cradle-to-grave phase structure",
                "Shared allocation assumptions",
            ],
            "#E7E4D6",
        ),
        (
            (0.05, 0.35),
            0.24,
            0.16,
            "4. Impact Indicators",
            [
                "Carbon impact (kg CO2e)",
                "Water footprint (L)",
                "Ecotoxicity (CTUe)",
            ],
            "#DDEAD9",
        ),
        (
            (0.38, 0.35),
            0.24,
            0.16,
            "5. Statistical Tests",
            [
                "Descriptives and ANOVA",
                "Price correlation and regression",
                "Bootstrap and leave-one-out",
            ],
            "#F0E0D8",
        ),
        (
            (0.71, 0.35),
            0.24,
            0.16,
            "6. Sensitivity",
            [
                "Tornado analysis",
                "Monte Carlo simulation",
                "Manufacturing scenarios",
            ],
            "#E5DFF0",
        ),
        (
            (0.08, 0.07),
            0.84,
            0.14,
            "7. Released Outputs",
            [
                "Canonical dataset and supplementary tables",
                "Figure assets and tagged PDF/DOCX artifacts",
                "Regeneration scripts for full rebuild",
            ],
            "#EFE6D8",
        ),
    ]

    for xy, width, height, title, lines, facecolor in boxes:
        draw_workflow_box(ax, xy, width, height, title, lines, facecolor=facecolor)

    draw_workflow_arrow(ax, (0.29, 0.715), (0.38, 0.715))
    draw_workflow_arrow(ax, (0.62, 0.715), (0.71, 0.715))
    draw_workflow_arrow(ax, (0.17, 0.64), (0.17, 0.51))
    draw_workflow_arrow(ax, (0.50, 0.64), (0.50, 0.51))
    draw_workflow_arrow(ax, (0.83, 0.64), (0.83, 0.51))
    draw_workflow_arrow(ax, (0.17, 0.35), (0.17, 0.21))
    draw_workflow_arrow(ax, (0.50, 0.35), (0.50, 0.21))
    draw_workflow_arrow(ax, (0.83, 0.35), (0.83, 0.21))

    finish_figure(
        fig,
        "Figure 1. Methodological Workflow for the 40-Model Screening Study",
        "The workflow links purposive product sampling, simplified LCA construction, multi-criteria indicators, statistical testing, and regenerated artifacts.",
    )
    fig.tight_layout(rect=[0, 0, 1, 0.89])
    return fig


def plot_figure_1(df: pd.DataFrame) -> plt.Figure:
    fig, axes = plt.subplots(2, 2, figsize=(12.6, 9.2), sharex=False)
    axes = axes.flatten()
    for idx, category in enumerate(CATEGORY_ORDER):
        ax = axes[idx]
        subset = df[df["Category"] == category].sort_values("CO2e_Total", ascending=True)
        colors = subset["Upper_Material_Type"].map(MATERIAL_PALETTE)
        ax.barh(subset["Model"], subset["CO2e_Total"], color=colors, edgecolor="none")
        ax.set_title(category, loc="left", pad=8)
        ax.set_xlabel("kg CO2e per pair")
        if idx % 2 == 0:
            ax.set_ylabel("Model")
        else:
            ax.set_ylabel("")
        ax.tick_params(axis="y", labelsize=8.5)
        ax.tick_params(axis="x", labelsize=8.5)
        ax.grid(axis="x", alpha=0.7)
        ax.grid(axis="y", visible=False)
        ax.set_axisbelow(True)
        max_val = subset["CO2e_Total"].max()
        for y, value in enumerate(subset["CO2e_Total"]):
            ax.text(value + max_val * 0.015, y, f"{value:.2f}", va="center", fontsize=7.5, color="#3D3731")
    legend_handles = [
        Patch(facecolor=MATERIAL_PALETTE[key], edgecolor="none", label=key) for key in MATERIAL_ORDER
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        ncol=3,
        frameon=False,
        bbox_to_anchor=(0.5, -0.01),
        fontsize=9,
    )
    finish_figure(
        fig,
        "Figure 2. Product-Level Carbon Footprints by Category and Upper Material",
        "Each panel shows the 10 sampled models within a category, sorted by cradle-to-grave screening CO2e.",
    )
    fig.tight_layout(rect=[0, 0.05, 1, 0.91])
    return fig


def plot_figure_2(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8.4, 6.4))
    for category in CATEGORY_ORDER:
        for group in ["Leather-associated", "Non-leather"]:
            subset = df[(df["Category"] == category) & (df["Leather_Group"] == group)]
            ax.scatter(
                subset["Price_USD"],
                subset["CO2e_Total"],
                s=82,
                marker=CATEGORY_MARKERS[category],
                c=LEATHER_GROUP_PALETTE[group],
                alpha=0.88,
                edgecolors="#FAF7F2",
                linewidths=0.7,
            )

    coef = np.polyfit(df["Price_USD"], df["CO2e_Total"], 1)
    x = np.linspace(df["Price_USD"].min(), df["Price_USD"].max(), 200)
    ax.plot(x, coef[0] * x + coef[1], color="#5A524B", linewidth=1.5, linestyle="--", alpha=0.8)

    ax.set_xlabel("Retail price (USD)")
    ax.set_ylabel("kg CO2e per pair")
    ax.set_xlim(df["Price_USD"].min() - 8, df["Price_USD"].max() + 12)
    ax.set_ylim(-0.2, df["CO2e_Total"].max() + 2.5)
    ax.text(
        0.98,
        0.955,
        "Pearson r = -0.13\np = 0.43",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=10,
        bbox={"facecolor": "#F4EEE5", "edgecolor": "#B8AA97", "boxstyle": "round,pad=0.4"},
    )

    group_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            markerfacecolor=color,
            markeredgecolor="#FAF7F2",
            markeredgewidth=0.7,
            markersize=9,
            label=label,
        )
        for label, color in LEATHER_GROUP_PALETTE.items()
    ]
    category_handles = [
        Line2D([0], [0], marker=marker, color="#4C443C", linestyle="None", markersize=8, label=label)
        for label, marker in CATEGORY_MARKERS.items()
    ]
    legend_one = ax.legend(
        handles=group_handles,
        loc="upper left",
        bbox_to_anchor=(0.01, 0.99),
        frameon=False,
        title="Material group",
        fontsize=9,
        title_fontsize=10,
        borderaxespad=0.0,
    )
    ax.add_artist(legend_one)
    ax.legend(
        handles=category_handles,
        loc="upper left",
        bbox_to_anchor=(0.40, 0.99),
        frameon=False,
        title="Category",
        fontsize=9,
        title_fontsize=10,
        borderaxespad=0.0,
    )

    finish_figure(
        fig,
        "Figure 3. Retail Price Is a Poor Proxy for Carbon Impact",
        "Leather-associated models remain high impact across a broad price range, while non-leather models cluster low.",
    )
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    return fig


def plot_figure_3(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8.4, 6.4))
    for material in MATERIAL_ORDER:
        subset = df[df["Upper_Material_Type"] == material]
        if subset.empty:
            continue
        ax.scatter(
            subset["CO2e_Total"],
            subset["Water_L"],
            s=96,
            c=MATERIAL_PALETTE[material],
            alpha=0.9,
            edgecolors="#FBF8F3",
            linewidths=0.7,
            label=material,
        )

    x = np.linspace(df["CO2e_Total"].min(), df["CO2e_Total"].max(), 200)
    coef = np.polyfit(df["CO2e_Total"], df["Water_L"], 1)
    ax.plot(x, coef[0] * x + coef[1], linestyle="--", color="#534B44", linewidth=1.5, alpha=0.75)
    ax.axvline(df["CO2e_Total"].median(), linestyle=":", color="#7A6F65", linewidth=1)
    ax.axhline(df["Water_L"].median(), linestyle=":", color="#7A6F65", linewidth=1)
    ax.set_xlabel("kg CO2e per pair")
    ax.set_ylabel("Water footprint (L per pair)")
    ax.set_xlim(-0.2, df["CO2e_Total"].max() + 2.0)
    ax.set_ylim(0, df["Water_L"].max() + 90)
    ax.text(
        0.98,
        0.955,
        "Pearson r = 0.998\nSpearman ρ = 0.990",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=10,
        bbox={"facecolor": "#F4EEE5", "edgecolor": "#B8AA97", "boxstyle": "round,pad=0.4"},
    )
    ax.legend(
        frameon=False,
        ncol=2,
        fontsize=8.3,
        loc="upper left",
        bbox_to_anchor=(0.0, 1.005),
        borderaxespad=0.0,
        handletextpad=0.5,
        columnspacing=1.2,
    )
    finish_figure(
        fig,
        "Figure 4. Carbon and Water Impacts Move Together Across the Sample",
        "The same leather-heavy product architectures dominate both climate and water burdens.",
    )
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    return fig


def plot_figure_4() -> plt.Figure:
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.8), gridspec_kw={"width_ratios": [1.3, 1]})
    ax_left, ax_right = axes

    base = 18.38
    tornado = [
        ("Leather EF", 13.4, 23.4),
        ("Mass estimate", 15.1, 21.7),
        ("Manufacturing", 16.4, 20.4),
        ("Transport", 17.5, 19.3),
        ("End-of-life", 18.0, 18.8),
    ]
    labels = [item[0] for item in tornado][::-1]
    lows = np.array([item[1] for item in tornado][::-1])
    highs = np.array([item[2] for item in tornado][::-1])
    y = np.arange(len(labels))
    ax_left.barh(y, base - lows, left=lows, color="#C96B4A", alpha=0.85, label="Lower bound")
    ax_left.barh(y, highs - base, left=base, color="#D4AE63", alpha=0.9, label="Upper bound")
    ax_left.axvline(base, color="#3A322B", linewidth=1.3, linestyle="--")
    ax_left.set_yticks(y, labels)
    ax_left.set_xlabel("Nike Air Force 1 scenario result (kg CO2e)")
    ax_left.set_title("Tornado Sensitivity", loc="left", pad=8)
    ax_left.legend(frameon=False, loc="lower right", fontsize=8.8)
    ax_left.grid(axis="y", visible=False)
    ax_left.text(
        base + 0.1,
        len(labels) - 0.55,
        "Base = 18.38",
        fontsize=8.8,
        color="#3A322B",
        ha="left",
        va="center",
    )

    wardrobe_labels = ["All leather casual", "Mixed (1 leather, 2 synthetic)", "All synthetic athletic"]
    wardrobe_values = [52.5, 20.3, 4.2]
    wardrobe_pct = [24.3, 11.1, 2.5]
    colors = ["#9B3D2E", "#C27B57", "#2F6B7D"]
    bars = ax_right.barh(wardrobe_labels, wardrobe_values, color=colors, edgecolor="none")
    ax_right.invert_yaxis()
    ax_right.set_xlabel("Annual footwear carbon impact (kg CO2e)")
    ax_right.set_title("Wardrobe Context", loc="left", pad=8)
    ax_right.grid(axis="y", visible=False)
    for bar, pct in zip(bars, wardrobe_pct):
        ax_right.text(
            bar.get_width() + 1.0,
            bar.get_y() + bar.get_height() / 2,
            f"{bar.get_width():.1f} kg | {pct:.1f}% of wardrobe",
            va="center",
            fontsize=8.7,
            color="#3C352E",
        )

    finish_figure(
        fig,
        "Figure 5. Sensitivity and Consumer Context",
        "Material assumptions drive the largest uncertainty swings, yet wardrobe-level outcomes remain strongly material-dependent.",
    )
    fig.tight_layout(rect=[0, 0, 1, 0.885])
    return fig


def plot_overview(df: pd.DataFrame) -> plt.Figure:
    fig = plt.figure(figsize=(14, 11))
    gs = fig.add_gridspec(2, 2, hspace=0.34, wspace=0.22)

    # Panel A: top 12 / bottom 12 products
    ax_a = fig.add_subplot(gs[0, 0])
    subset = pd.concat(
        [
            df.sort_values("CO2e_Total", ascending=False).head(6),
            df.sort_values("CO2e_Total", ascending=True).head(6),
        ]
    ).drop_duplicates().sort_values("CO2e_Total")
    ax_a.barh(
        subset["Model"],
        subset["CO2e_Total"],
        color=subset["Upper_Material_Type"].map(MATERIAL_PALETTE),
        edgecolor="none",
    )
    ax_a.set_xlabel("kg CO2e per pair")
    ax_a.set_title("Extremes in the Sample", loc="left", pad=8)
    ax_a.tick_params(axis="y", labelsize=8.2)
    annotate_panel(ax_a, "A")

    # Panel B: price vs carbon
    ax_b = fig.add_subplot(gs[0, 1])
    for group, color in LEATHER_GROUP_PALETTE.items():
        subset = df[df["Leather_Group"] == group]
        ax_b.scatter(
            subset["Price_USD"],
            subset["CO2e_Total"],
            s=80,
            c=color,
            alpha=0.88,
            edgecolors="#FBF8F3",
            linewidths=0.7,
            label=group,
        )
    ax_b.set_xlabel("Retail price (USD)")
    ax_b.set_ylabel("kg CO2e per pair")
    ax_b.set_title("Weak Price Signal", loc="left", pad=8)
    ax_b.legend(frameon=False, fontsize=8.6)
    annotate_panel(ax_b, "B")

    # Panel C: carbon vs water
    ax_c = fig.add_subplot(gs[1, 0])
    for material in ["Full Leather", "Synthetic Textile", "Recycled Synthetic", "Partial Leather", "Synthetic Leather"]:
        subset = df[df["Upper_Material_Type"] == material]
        if subset.empty:
            continue
        ax_c.scatter(
            subset["CO2e_Total"],
            subset["Water_L"],
            s=84,
            c=MATERIAL_PALETTE[material],
            alpha=0.9,
            edgecolors="#FBF8F3",
            linewidths=0.7,
            label=material,
        )
    ax_c.set_xlabel("kg CO2e per pair")
    ax_c.set_ylabel("Water (L per pair)")
    ax_c.set_title("Carbon-Water Alignment", loc="left", pad=8)
    ax_c.legend(frameon=False, fontsize=8.0, ncol=2)
    annotate_panel(ax_c, "C")

    # Panel D: wardrobe context
    ax_d = fig.add_subplot(gs[1, 1])
    scenario_names = ["Leather-heavy", "Mixed", "Synthetic-only"]
    scenario_values = [52.5, 20.3, 4.2]
    ax_d.bar(scenario_names, scenario_values, color=["#9B3D2E", "#C27B57", "#2F6B7D"], width=0.62)
    ax_d.set_ylabel("Annual kg CO2e")
    ax_d.set_title("Wardrobe Impact Range", loc="left", pad=8)
    for idx, value in enumerate(scenario_values):
        ax_d.text(idx, value + 1.0, f"{value:.1f}", ha="center", va="bottom", fontsize=8.8)
    annotate_panel(ax_d, "D")

    finish_figure(
        fig,
        "Strengthening Analysis Figures",
        "Overview of the main carbon, water, price, and context patterns in the 40-model dataset.",
    )
    fig.subplots_adjust(top=0.90)
    return fig


def main() -> None:
    apply_theme()
    df = load_dataset()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    outputs = [
        ("figure_0_methodology_workflow.png", plot_methodology_figure()),
        ("figure_1_category_model_carbon.png", plot_figure_1(df)),
        ("figure_2_price_vs_carbon.png", plot_figure_2(df)),
        ("figure_3_carbon_vs_water.png", plot_figure_3(df)),
        ("figure_4_sensitivity_and_context.png", plot_figure_4()),
    ]

    for filename, fig in outputs:
        save_figure(fig, FIGURE_DIR / filename)

    save_figure(plot_overview(df), OVERVIEW_PATH)


if __name__ == "__main__":
    main()
