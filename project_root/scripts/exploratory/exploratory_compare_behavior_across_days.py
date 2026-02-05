"""
Exploratory comparison of behavioral category proportions across days.
Used to inspect early vs late scan redistribution patterns.
Outputs are diagnostic and not part of the main analysis pipeline,
they use original (Spanish) labels.
Not intended for presentation or final figures.

"""


import pandas as pd

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))


from utils.paths import (
    DATA_DIR,
    GROUP_SCANS_DIR,
)

# ======================================================
# Setup
# ======================================================

ethogram = pd.read_csv(
    DATA_DIR / "ethogram_reference.csv"
)
ethogram_clean = ethogram[["Behavior", "Category"]]

scans = pd.read_csv(
    DATA_DIR / "group_scan_observations.csv"
)
scans["Behavior"] = scans["Behavior"].str.strip()

# Ensure exploratory output folder exists
EXPLORATORY_DIR = GROUP_SCANS_DIR / "exploratory"
EXPLORATORY_DIR.mkdir(parents=True, exist_ok=True)

# ======================================================
# Analysis function
# ======================================================

def analyze_day(day: int):
    print(f"\n=== Processing Day {day} ===")

    # Filter day
    day_data = scans[scans["Day"] == day]

    # Attach categories
    scans_cat = day_data.merge(
        ethogram_clean,
        on="Behavior",
        how="left"
    )

    # Aggregate by scan and category
    scan_category = (
        scans_cat
        .groupby(["Scan", "Category"])["Count"]
        .sum()
        .reset_index()
    )

    # Totals per scan
    scan_totals = (
        scan_category
        .groupby("Scan")["Count"]
        .sum()
        .reset_index(name="Total")
    )

    scan_category = scan_category.merge(
        scan_totals,
        on="Scan"
    )

    # Proportions
    scan_category["Proportion"] = (
        scan_category["Count"] / scan_category["Total"]
    )

    # Pivot: scan × category
    summary = (
        scan_category
        .pivot_table(
            index="Scan",
            columns="Category",
            values="Proportion",
            fill_value=0
        )
    )

    # Early / late split (transposed)
    early = summary.loc[1:6].T
    late = summary.loc[7:12].T

    # Save outputs
    summary.to_csv(
        EXPLORATORY_DIR / f"day{day}_scan_category_proportions_total.csv"
    )
    early.to_csv(
        EXPLORATORY_DIR / f"day{day}_scan_1_6_total.csv"
    )
    late.to_csv(
        EXPLORATORY_DIR / f"day{day}_scan_7_12_total.csv"
    )

    # Console output
    print("Early session (1–6):")
    print(early.round(2))

    print("Late session (7–12):")
    print(late.round(2))


# ======================================================
# Explicit calls (Pattern 2)
# ======================================================

analyze_day(1)
analyze_day(2)
analyze_day(3)
