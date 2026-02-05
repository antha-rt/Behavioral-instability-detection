import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from utils.paths import (
    BASELINES_DIR,
    GROUP_SCANS_DIR,
)


from utils.translate import translate_category

# ======================================================
# Setup
# ======================================================

COLOR_MAP = "coolwarm"
VMIN = -0.40
VMAX = 0.40

# ======================================================
# Load data
# ======================================================

baseline = pd.read_csv(BASELINES_DIR / "category_baseline.csv")
baseline = baseline.rename(columns={"Proportion": "Baseline_Proportion"})

all_categories = baseline["Category"].tolist()

scans = pd.read_csv(
    GROUP_SCANS_DIR / "scans_category_proportions_all_days.csv"
)

# ======================================================
# FUNCTION: BUILD HEATMAP FOR ONE DAY
# ======================================================

def plot_day_heatmap(day):

    day_data = scans[scans["Day"] == day]

    if day_data.empty:
        print(f"No data for Day {day}")
        return

    scan_ids = sorted(day_data["Scan"].unique())

    # --------------------------------------------------
    # Build full Scan × Category grid
    # --------------------------------------------------
    full_index = pd.MultiIndex.from_product(
        [scan_ids, all_categories],
        names=["Scan", "Category"]
    )

    day_full = (
        day_data
        .set_index(["Scan", "Category"])
        .reindex(full_index, fill_value=0)
        .reset_index()
    )

    # --------------------------------------------------
    # Merge baseline + compute deviation
    # --------------------------------------------------
    day_full = day_full.merge(
        baseline,
        on="Category",
        how="left"
    )

    day_full["Deviation"] = (
        day_full["Proportion"] - day_full["Baseline_Proportion"]
    )

    # --------------------------------------------------
    # Pivot for heatmap
    # --------------------------------------------------
    heatmap_df = day_full.pivot(
        index="Category",
        columns="Scan",
        values="Deviation"
    )

    # Keep category order consistent with baseline
    heatmap_df = heatmap_df.loc[all_categories]

    # --------------------------------------------------
    # Translate category labels (PRESENTATION ONLY)
    # --------------------------------------------------
    heatmap_df.index = heatmap_df.index.map(translate_category)
    category_labels_en = [translate_category(c) for c in all_categories]

    # --------------------------------------------------
    # Plot
    # --------------------------------------------------
    plt.figure(figsize=(14, 8))
    im = plt.imshow(
        heatmap_df,
        aspect="auto",
        cmap=COLOR_MAP,
        vmin=VMIN,
        vmax=VMAX
    )

    plt.colorbar(im, label="Deviation from baseline")

    plt.title(f"Category deviation heatmap — Day {day}")
    plt.xlabel("Scan (≈ time)")
    plt.ylabel("Behavioral category")

    plt.xticks(
        ticks=np.arange(len(scan_ids)),
        labels=scan_ids
    )

    plt.yticks(
        ticks=np.arange(len(category_labels_en)),
        labels=category_labels_en
    )

    plt.tight_layout()
    plt.show()

# ======================================================
# RUN: ALL DAYS
# ======================================================

for day in sorted(scans["Day"].unique()):
    plot_day_heatmap(day)
