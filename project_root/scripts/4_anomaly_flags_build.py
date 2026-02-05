import pandas as pd

from utils.paths import (
    BASELINES_DIR,
    GROUP_SCANS_DIR,
    ANOMALIES_DIR,
)

from utils.translate import translate_series

# ======================================================
# Load scan-level proportions
# ======================================================

scan_category = pd.read_csv(
    GROUP_SCANS_DIR / "scans_category_proportions_all_days.csv"
)

# Expected columns:
# Day | Scan | Category | Proportion

# ======================================================
# Compute per-category quantile thresholds
# ======================================================

QUANTILES = {
    "low": [0.01, 0.02, 0.05],
    "high": [0.95, 0.98, 0.99],
}

category_stats = (
    scan_category
    .groupby("Category")["Proportion"]
    .quantile(
        QUANTILES["low"] + QUANTILES["high"]
    )
    .unstack()
)

category_stats.columns = [
    "p01", "p02", "p05",
    "p95", "p98", "p99",
]

# ======================================================
# Flag + severity logic
# ======================================================

def flag_with_severity(row):
    cat = row["Category"]
    val = row["Proportion"]

    if cat not in category_stats.index:
        return None, None

    stats = category_stats.loc[cat]

    # HIGH severity
    if val > stats["p99"]:
        return "HIGH_OUTLIER", "HIGH"
    if val < stats["p01"]:
        return "LOW_OUTLIER", "HIGH"

    # MEDIUM severity
    if val > stats["p98"]:
        return "HIGH_OUTLIER", "MEDIUM"
    if val < stats["p02"]:
        return "LOW_OUTLIER", "MEDIUM"

    # LOW severity
    if val > stats["p95"]:
        return "HIGH_OUTLIER", "LOW"
    if val < stats["p05"]:
        return "LOW_OUTLIER", "LOW"

    return None, None


scan_category[["Flag", "Severity"]] = (
    scan_category
    .apply(
        lambda r: pd.Series(flag_with_severity(r)),
        axis=1
    )
)

flags = scan_category[scan_category["Flag"].notnull()]

flags.to_csv(
    ANOMALIES_DIR / "scan_anomaly_flags_with_severity.csv",
    index=False
)


# ======================================================
# Print output (English, translated copy)
# ======================================================

from utils.translate import translate_series

print("\n=== Scan-level anomaly flags (with severity) ===")

flags_print = flags.copy()

# Translate category labels for display only
flags_print["Category"] = translate_series(
    flags_print["Category"],
    kind="category"
)

print(
    flags_print
    .sort_values(["Day", "Scan", "Severity"])
    .round(3)
)

