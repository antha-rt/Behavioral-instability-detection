from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"

BASELINES_DIR = OUTPUTS_DIR / "baselines"
GROUP_SCANS_DIR = OUTPUTS_DIR / "group scans"
ANOMALIES_DIR = OUTPUTS_DIR / "anomalies flags"
SOCIAL_ROLES_DIR = OUTPUTS_DIR / "social roles"

for d in [
    BASELINES_DIR,
    GROUP_SCANS_DIR,
    ANOMALIES_DIR,
    SOCIAL_ROLES_DIR,
]:
    d.mkdir(parents=True, exist_ok=True)
