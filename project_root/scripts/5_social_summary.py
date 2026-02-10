import pandas as pd
import numpy as np

from utils.paths import (
    DATA_DIR,
    SOCIAL_ROLES_DIR,
)

from utils.translate import translate_category


# ======================================================
# Setup
# ======================================================

SOCIAL_CATEGORIES = ["Agonista", "Apaciguamiento", "Afiliativa"]

CATEGORY_PROPORTIONS = {
    "Agonista": 0.004123711340206186,
    "Apaciguamiento": 0.006185567010309278,
    "Afiliativa": 0.016494845360824743
}

CATEGORY_WEIGHTS = {
    k: 1 / v for k, v in CATEGORY_PROPORTIONS.items()
}

ALL_INDIVIDUALS = ["N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8"]

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

def load_data():
    ethogram = pd.read_csv(
        DATA_DIR / "ethogram_reference.csv"
    )
    group_scans = pd.read_csv(
        DATA_DIR / "group_scan_observations.csv"
    )
    social = pd.read_csv(
        DATA_DIR / "directed_social_interactions.csv"
    )
    return ethogram, group_scans, social

# ------------------------------------------------------------
# BUILD INDIVIDUAL REGISTRY
# ------------------------------------------------------------

def get_all_individuals():
    return ALL_INDIVIDUALS

# ------------------------------------------------------------
# BUILD SOCIAL LEDGERS
# ------------------------------------------------------------

def build_ledgers(social_df, individuals):
    index = pd.MultiIndex.from_product(
        [individuals, SOCIAL_CATEGORIES],
        names=["Individual", "Category"]
    )

    ledger = pd.DataFrame(
        index=index,
        columns=["OUT", "IN"],
        data=0
    )

    for _, row in social_df.iterrows():
        actor = row["Actor"]
        target = row["Target"]
        category = row["Category"]
        count = row["Count"]

        if category not in SOCIAL_CATEGORIES:
            continue

        ledger.loc[(actor, category), "OUT"] += count
        ledger.loc[(target, category), "IN"] += count

    ledger["NET"] = ledger["OUT"] - ledger["IN"]
    return ledger.reset_index()

# ------------------------------------------------------------
# APPLY RARITY WEIGHTING
# ------------------------------------------------------------

def apply_weights(ledger):
    ledger["WEIGHT"] = ledger["Category"].map(CATEGORY_WEIGHTS)
    ledger["W_NET"] = ledger["NET"] * ledger["WEIGHT"]
    ledger["TOTAL"] = ledger["OUT"] + ledger["IN"]
    ledger["BIAS"] = ledger.apply(
        lambda r: r["NET"] / r["TOTAL"] if r["TOTAL"] > 0 else 0,
        axis=1
    )
    return ledger

# ------------------------------------------------------------
# BUILD DIRECTED EDGE LIST
# ------------------------------------------------------------

def build_edge_list(social_df):
    edges = []

    for _, row in social_df.iterrows():
        category = row["Category"]
        if category not in SOCIAL_CATEGORIES:
            continue

        edges.append({
            "Source": row["Actor"],
            "Target": row["Target"],
            "Category": category,
            "Raw_Count": row["Count"],
            "Weighted_Intensity": (
                row["Count"] * CATEGORY_WEIGHTS[category]
            )
        })

    return pd.DataFrame(edges)

# ------------------------------------------------------------
# ROLE ASSIGNMENT
# ------------------------------------------------------------

def assign_roles(category_df):
    roles = []

    dom_values = category_df["W_NET"]
    high = dom_values.quantile(0.75)
    low = dom_values.quantile(0.25)

    for _, row in category_df.iterrows():
        if row["TOTAL"] == 0:
            role = "Isolated"
        elif row["W_NET"] >= high:
            role = "Primary_Actor"
        elif row["W_NET"] > 0:
            role = "Secondary_Actor"
        elif row["W_NET"] <= low:
            role = "Primary_Receiver"
        else:
            role = "Peripheral"

        roles.append(role)

    category_df["Role"] = roles
    return category_df

# ------------------------------------------------------------
# MAIN PIPELINE
# ------------------------------------------------------------

def main():
    ethogram, group_scans, social = load_data()

    individuals = get_all_individuals()

    ledger = build_ledgers(social, individuals)
    ledger = apply_weights(ledger)

    edge_list = build_edge_list(social)

    role_tables = []

    for category in SOCIAL_CATEGORIES:
        cat_df = ledger[ledger["Category"] == category].copy()
        cat_df = assign_roles(cat_df)
        cat_df["System"] = category
        role_tables.append(cat_df)

    roles_final = pd.concat(role_tables)

    # --------------------------------------------------------
    # OUTPUT FILES
    # --------------------------------------------------------

    ledger.to_csv(
        SOCIAL_ROLES_DIR / "individual_social_ledgers.csv",
        index=False
    )

    edge_list.to_csv(
        SOCIAL_ROLES_DIR / "directed_social_edges.csv",
        index=False
    )

    roles_final.to_csv(
        SOCIAL_ROLES_DIR / "individual_roles_by_category.csv",
        index=False
    )

    # --------------------------------------------------------
    # PRINT ROLE TABLES
    # --------------------------------------------------------

    for category in SOCIAL_CATEGORIES:
        category_en = translate_category(category)

        print("\n" + "=" * 60)
        print(f"ROLES TABLE — {category_en.upper()}")
        print("=" * 60)

        display_df = roles_final[
            roles_final["Category"] == category
            ][[
            "Individual",
            "OUT",
            "IN",
            "NET",
            "W_NET",
            "TOTAL",
            "BIAS",
            "Role"
        ]].sort_values("W_NET", ascending=False)

        print(display_df.to_string(index=False))


# ------------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
