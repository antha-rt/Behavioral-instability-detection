"""
Exploratory script to inspect per-category deviation magnitude.
Outputs are diagnostic and not part of the main analysis pipeline,
they use original (Spanish) labels.
Not intended for presentation or final figures.
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))


from utils.paths import (
    DATA_DIR,
    OUTPUTS_DIR,
    BASELINES_DIR,
    GROUP_SCANS_DIR,
    ANOMALIES_DIR,
    SOCIAL_ROLES_DIR,
)

baseline = pd.read_csv( BASELINES_DIR / "category_baseline.csv")
scans = pd.read_csv( GROUP_SCANS_DIR / "scans_category_proportions_all_days.csv")


df_total = scans.merge(
    baseline.rename(columns={"Proportion": "Baseline_Prop"}),
    on="Category",
    how="left"
)


df_total["Deviation"] = df_total["Proportion"] - df_total["Baseline_Prop"]

# ======================================================
# 98 P
# ======================================================

category_limits_series = df_total.groupby("Category")["Deviation"].apply(
    lambda x: x.abs().quantile(0.98)
).sort_values(ascending=False)


print("-" * 50)
print(f"{'CATEGORÍA':<25} | {'LÍMITE (P98)':<15}")
print("-" * 50)

for cat, limit in category_limits_series.items():
    print(f"{cat:<25} | {limit:>15.4f}")

print("-" * 50)