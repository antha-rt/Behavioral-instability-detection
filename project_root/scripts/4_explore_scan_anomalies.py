import pandas as pd

from utils.paths import (
    DATA_DIR,
    ANOMALIES_DIR,
)

from utils.translate import translate_category

# ======================================================
# Load data
# ======================================================

flags = pd.read_csv(
    ANOMALIES_DIR / "scan_anomaly_flags_with_severity.csv"
)

scan_observations = pd.read_csv(
    DATA_DIR / "group_scan_observations.csv"
)

ethogram = pd.read_csv(
    DATA_DIR / "ethogram_reference.csv"
)[["Behavior", "Category"]]

# ======================================================
# Severity ordering
# ======================================================

SEVERITY_ORDER = {
    "HIGH": 0,
    "MEDIUM": 1,
    "LOW": 2,
}

flags["SeverityRank"] = flags["Severity"].map(SEVERITY_ORDER)

alerts = (
    flags
    .sort_values(["SeverityRank", "Day", "Scan"])
    .reset_index(drop=True)
)

# ======================================================
# Helper: print alert list grouped by Day (ENGLISH VIEW)
# ======================================================

def show_alerts(alerts_df):
    print("\n=== Anomaly Alerts ===")

    last_day = None
    for i, row in alerts_df.iterrows():
        if row.Day != last_day:
            print(
                f"\n--- Day {row.Day} "
                + "-" * 48
            )
            last_day = row.Day

        category_en = translate_category(row.Category)

        print(
            f"{i+1:>3} | "
            f"Severity: {row.Severity:<6} | "
            f"Scan {row.Scan:<3} | "
            f"{category_en:<16} | "
            f"{row.Flag}"
        )

# ======================================================
# Interactive investigation loop
# ======================================================

while True:
    show_alerts(alerts)

    choice = input(
        "\nSelect alert number to inspect "
        "(Enter to exit): "
    ).strip()

    if not choice:
        print("Exiting explorer.")
        break

    idx = int(choice) - 1
    selected = alerts.iloc[idx]

    day = selected.Day
    scan = selected.Scan
    category = selected.Category              # Spanish (for filtering)
    category_en = translate_category(category)  # English (for display)

    drill = (
        scan_observations
        .merge(ethogram, on="Behavior", how="left")
        .query(
            "Day == @day and Scan == @scan and Category == @category"
        )
        .groupby("Behavior")["Count"]
        .sum()
        .reset_index()
        .sort_values("Count", ascending=False)
    )

    total = drill["Count"].sum()
    drill["Proportion"] = drill["Count"] / total

    print("\n=== Alert Investigation ===")
    print(
        f"Severity: {selected.Severity}\n"
        f"Day {day} | Scan {scan} | "
        f"Category: {category_en}\n"
    )

    print(drill.round(3))

    input("\nPress Enter to return to alert list...")

