import os
import pandas as pd

from utils.paths import (
    DATA_DIR,
    OUTPUTS_DIR,
)

from utils.translate import translate_series

# ======================================================
# Setup
# ======================================================
os.makedirs("../outputs", exist_ok=True)

# Load reference ethogram
ethogram = pd.read_csv(DATA_DIR / "ethogram_reference.csv")
ethogram_clean = ethogram[["Behavior", "Category"]]

# Load group scans
scans = pd.read_csv(DATA_DIR / "group_scan_observations.csv")
scans["Behavior"] = scans["Behavior"].str.strip()

# ======================================================
# 1. BUILD CATEGORY BASELINE
# ======================================================
# Total counts per behavior
baseline_counts = (
    scans
    .groupby("Behavior")["Count"]
    .sum()
)

total_events = baseline_counts.sum()

baseline_df = (
    baseline_counts
    .reset_index()
    .merge(ethogram_clean, on="Behavior", how="left")
)

baseline_df["Proportion"] = baseline_df["Count"] / total_events

# All categories from ethogram (including event-only ones)
all_categories = (
    ethogram_clean["Category"]
    .dropna()
    .unique()
)

category_baseline = (
    baseline_df
    .groupby("Category")["Proportion"]
    .sum()
    .reindex(all_categories, fill_value=0)
    .reset_index()
    .sort_values("Proportion", ascending=False)
)

# ------------------------------------------------------
# Save baseline
# ------------------------------------------------------
OUTPUTS_BASELINES_DIR = OUTPUTS_DIR / "baselines"
OUTPUTS_BASELINES_DIR.mkdir(parents=True, exist_ok=True)

category_baseline.to_csv(
    OUTPUTS_BASELINES_DIR / "category_baseline.csv",
    index=False
)

# ------------------------------------------------------
# PRINT baseline
# ------------------------------------------------------
print("\nSaved category baseline:")

category_baseline_print = category_baseline.copy()
category_baseline_print["Category"] = translate_series(
    category_baseline_print["Category"],
    kind="category"
)

print(category_baseline_print.round(3))

# ======================================================
# 2. BUILD SCAN-LEVEL CATEGORY PROPORTIONS (ALL DAYS)
# ======================================================
# Attach categories
scans_cat = scans.merge(
    ethogram_clean,
    on="Behavior",
    how="left"
)

# Aggregate by day, scan, category
scans_category = (
    scans_cat
    .groupby(["Day", "Scan", "Category"])["Count"]
    .sum()
    .reset_index()
)

# Totals per scan
scan_totals = (
    scans_category
    .groupby(["Day", "Scan"])["Count"]
    .sum()
    .reset_index(name="Total")
)

scans_category = scans_category.merge(
    scan_totals,
    on=["Day", "Scan"]
)

# Proportions
scans_category["Proportion"] = (
    scans_category["Count"] / scans_category["Total"]
)

# Keep only what we need
scans_category = scans_category[
    ["Day", "Scan", "Category", "Proportion"]
].sort_values(["Day", "Scan"])

# ------------------------------------------------------
# Save scan-level proportions (Spanish, untouched)
# ------------------------------------------------------
OUTPUTS_GROUP_SCANS_DIR = OUTPUTS_DIR / "group scans"
OUTPUTS_GROUP_SCANS_DIR.mkdir(parents=True, exist_ok=True)

scans_category.to_csv(
    OUTPUTS_GROUP_SCANS_DIR / "scans_category_proportions_all_days.csv",
    index=False
)
