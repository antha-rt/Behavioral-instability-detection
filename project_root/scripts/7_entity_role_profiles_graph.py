import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from utils.paths import (
    SOCIAL_ROLES_DIR,
)

from utils.translate import translate_category

# ======================================================
# Setup
# ======================================================

COLOR_MAP = "coolwarm"
BIAS_VMIN = -1
BIAS_VMAX = 1

FIGSIZE_HEATMAP = (10, 6)

# Internal system labels (Spanish, logic-safe)
SYSTEM_ORDER = ["Agonista", "Apaciguamiento", "Afiliativa"]

# ======================================================
# LOAD DATA
# ======================================================

roles = pd.read_csv(
    SOCIAL_ROLES_DIR / "individual_roles_by_category.csv"
)

# Ensure consistent ordering
roles["System"] = pd.Categorical(
    roles["System"],
    categories=SYSTEM_ORDER,
    ordered=True
)

individuals = sorted(roles["Individual"].unique())

# ======================================================
# ROLE DEVIATION HEATMAP
# ======================================================

def plot_role_deviation_heatmap():
    """
    Entity × System heatmap using directional bias (BIAS).
    Interpretable as a role fingerprint across interaction systems.
    """

    heatmap_df = roles.pivot(
        index="Individual",
        columns="System",
        values="BIAS"
    ).loc[individuals, SYSTEM_ORDER]

    # Translate system labels for presentation
    system_labels_en = [translate_category(s) for s in SYSTEM_ORDER]

    plt.figure(figsize=FIGSIZE_HEATMAP)

    im = plt.imshow(
        heatmap_df,
        cmap=COLOR_MAP,
        vmin=BIAS_VMIN,
        vmax=BIAS_VMAX,
        aspect="auto"
    )

    plt.colorbar(
        im,
        label="Directional bias (actor ↔ receiver)"
    )

    plt.title("Entity Role Deviation Matrix")
    plt.xlabel("Interaction system")
    plt.ylabel("Entity")

    plt.xticks(
        ticks=np.arange(len(system_labels_en)),
        labels=system_labels_en
    )

    plt.yticks(
        ticks=np.arange(len(individuals)),
        labels=individuals
    )

    plt.tight_layout()
    plt.show()

# ======================================================
# MAIN
# ======================================================

def main():
    plot_role_deviation_heatmap()

# ======================================================
# ENTRY POINT
# ======================================================

if __name__ == "__main__":
    main()
