import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from utils.paths import (
    DATA_DIR,
    BASELINES_DIR,
)

from utils.translate import translate_category

# ======================================================
# Setup
# ======================================================

COLOR_MAP = "coolwarm"
VMIN = -0.40
VMAX = 0.40

# Event-based annotations (vertical markers BETWEEN events)
EVENT_MARKERS = {
    3.5: "Students enter",
    4.5: "Restrained",
    5.5: "Invasive procedure",
    11.5: "Released",
    13.5: "Redirected agonism"
}

# ======================================================
# LOAD DATA
# ======================================================

baseline = pd.read_csv(
    BASELINES_DIR / "category_baseline.csv"
)
baseline = baseline.rename(columns={"Proportion": "Baseline_Proportion"})

all_categories = baseline["Category"].tolist()

focal = pd.read_csv(
    DATA_DIR / "N2_individual_observation.csv"
)

ethogram = pd.read_csv(
    DATA_DIR / "ethogram_reference.csv"
)

# ======================================================
# MAP BEHAVIOR → CATEGORY USING ETHOGRAM
# ======================================================

behavior_to_category = dict(
    zip(ethogram["Behavior"], ethogram["Category"])
)

focal["Category"] = focal["Behavior"].map(behavior_to_category)

# Drop anything unmapped (defensive, but good practice)
focal = focal.dropna(subset=["Category"])

# ======================================================
# BUILD EVENT × CATEGORY PROPORTIONS
# ======================================================

events = sorted(focal["Event"].unique())

full_index = pd.MultiIndex.from_product(
    [events, all_categories],
    names=["Event", "Category"]
)

event_cat = (
    focal
    .groupby(["Event", "Category"])["Count"]
    .sum()
    .reindex(full_index, fill_value=0)
    .reset_index()
)

# Normalize to proportions PER EVENT
event_totals = (
    event_cat
    .groupby("Event")["Count"]
    .transform("sum")
)

event_cat["Proportion"] = np.where(
    event_totals > 0,
    event_cat["Count"] / event_totals,
    0
)

# ======================================================
# MERGE BASELINE + COMPUTE DEVIATION
# ======================================================

event_cat = event_cat.merge(
    baseline,
    on="Category",
    how="left"
)

event_cat["Deviation"] = (
    event_cat["Proportion"] - event_cat["Baseline_Proportion"]
)

# ======================================================
# PIVOT FOR HEATMAP
# ======================================================

heatmap_df = event_cat.pivot(
    index="Category",
    columns="Event",
    values="Deviation"
)

heatmap_df = heatmap_df.loc[all_categories]

# --------------------------------------------------
# Translate category labels (PRESENTATION ONLY)
# --------------------------------------------------
heatmap_df.index = heatmap_df.index.map(translate_category)
category_labels_en = [translate_category(c) for c in all_categories]

# ======================================================
# PLOT
# ======================================================

plt.figure(figsize=(16, 9))

im = plt.imshow(
    heatmap_df,
    aspect="auto",
    cmap=COLOR_MAP,
    vmin=VMIN,
    vmax=VMAX
)

plt.colorbar(im, label="Deviation from baseline")

plt.xlabel("Event sequence (behavior-driven)")
plt.ylabel("Behavioral category")

plt.xticks(
    ticks=np.arange(len(events)),
    labels=events
)

plt.yticks(
    ticks=np.arange(len(all_categories)),
    labels=category_labels_en
)

# ------------------------------------------------------
# EVENT ANNOTATIONS
# ------------------------------------------------------

ax = plt.gca()

for x_pos, label in EVENT_MARKERS.items():
    ax.axvline(
        x=x_pos - 1,  # align with imshow index
        color="black",
        linestyle="--",
        alpha=0.6
    )
    ax.text(
        x_pos - 1,
        -0.8,
        label,
        rotation=90,
        verticalalignment="bottom",
        horizontalalignment="right",
        fontsize=9
    )

plt.tight_layout()
plt.show()
