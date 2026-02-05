import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from utils.paths import BASELINES_DIR, GROUP_SCANS_DIR
from utils.translate import translate_category

# ======================================================
# Setup
# ======================================================

CAT_CONFIG = {
    "Rumiación": {"limit": 0.30, "color": "#1f77b4"},
    "Comer": {"limit": 0.75, "color": "#d62728"},
    "Afiliativa": {"limit": 0.15, "color": "#2ca02c"},
}

CATEGORY = "Rumiación"   # Internal label (Spanish, data-consistent)
DAY = 3

LIMIT = CAT_CONFIG.get(CATEGORY, {"limit": 0.30})["limit"]
PLOT_COLOR = CAT_CONFIG.get(CATEGORY, {"color": "#1f77b4"})["color"]

# Translated label for presentation only
CATEGORY_EN = translate_category(CATEGORY)

# ======================================================
# LOAD AND PREPARE DATA
# ======================================================

baseline = pd.read_csv(BASELINES_DIR / "category_baseline.csv")
scans = pd.read_csv(GROUP_SCANS_DIR / "scans_category_proportions_all_days.csv")

# 1. Baseline mean for the selected category
baseline_mean = baseline.loc[
    baseline["Category"] == CATEGORY, "Proportion"
].values[0]

# 2. Category variability (IQR) across all days
category_all_scans = scans.loc[
    scans["Category"] == CATEGORY, "Proportion"
]

q1_dev = category_all_scans.quantile(0.25) - baseline_mean
q3_dev = category_all_scans.quantile(0.75) - baseline_mean

# 3. Data for the selected day
day_data = scans[
    (scans["Day"] == DAY) & (scans["Category"] == CATEGORY)
].copy()

day_data = day_data.sort_values("Scan")
day_data["Deviation"] = day_data["Proportion"] - baseline_mean

# ======================================================
# VISUALIZATION
# ======================================================

fig, ax = plt.subplots(figsize=(12, 6))

# Baseline and normal range (IQR)
ax.axhline(
    0,
    color="black",
    linestyle="--",
    linewidth=1,
    alpha=0.7,
    label="Global mean (0)"
)

ax.fill_between(
    day_data["Scan"],
    q1_dev,
    q3_dev,
    color="gray",
    alpha=0.15,
    label=f"Normal range (IQR, {CATEGORY_EN})"
)

# Observed deviations
ax.plot(
    day_data["Scan"],
    day_data["Deviation"],
    marker="o",
    linewidth=2.5,
    markersize=8,
    color=PLOT_COLOR,
    label=f"Deviation on Day {DAY}"
)

# Aesthetics and scale
ax.set_ylim(-LIMIT, LIMIT)
ax.set_title(
    f"Deviation Analysis: {CATEGORY_EN} (Day {DAY})",
    fontsize=15,
    pad=20
)
ax.set_xlabel("Scan (time intervals)", fontsize=12)
ax.set_ylabel("Deviation from baseline", fontsize=12)

# Annotate extreme points for readability
for _, row in day_data.iterrows():
    if abs(row["Deviation"]) > (LIMIT * 0.7):
        ax.annotate(
            f"{row['Deviation']:.2f}",
            (row["Scan"], row["Deviation"]),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=9
        )

ax.grid(axis="y", linestyle=":", alpha=0.6)
ax.legend(loc="upper left", frameon=True)

plt.tight_layout()
plt.show()
