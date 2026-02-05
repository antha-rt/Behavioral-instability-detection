# utils/translate.py

# ======================================================
# Category translations
# ======================================================

CATEGORY_TRANSLATIONS = {
    "Comer": "Feeding",
    "Beber": "Drinking",
    "Descanso": "Resting",
    "Rumiación": "Rumination",
    "Locomoción": "Locomotion",
    "Exploración": "Exploration",
    "Cuidado corporal": "Body maintenance",
    "Agonista": "Agonistic",
    "Apaciguamiento": "Appeasement",
    "Afiliativa": "Affiliative",
    "Respuesta a coerción": "Response to coercion",
    "Autorregulación": "Self-regulation",
    "Locomoción cola": "Tail movement",
    "Locomoción orejas": "Ears movement",
    "Eliminación": "Micturition",
    "Otras generales": "Others",
    "Vocalización": "Vocalization"
}

# ======================================================
# Behavior translations (future use)
# ======================================================

BEHAVIOR_TRANSLATIONS = {
    # Example:
    # "Masticar 1": "Chew 1",
}

# ======================================================
# Helpers
# ======================================================

def translate_category(label: str) -> str:
    """Translate category label to English if available."""
    return CATEGORY_TRANSLATIONS.get(label, label)


def translate_behavior(label: str) -> str:
    """Translate behavior label to English if available."""
    return BEHAVIOR_TRANSLATIONS.get(label, label)


def translate_series(series, kind="category"):
    """Translate a pandas Series of labels."""
    if kind == "category":
        return series.map(lambda x: CATEGORY_TRANSLATIONS.get(x, x))
    if kind == "behavior":
        return series.map(lambda x: BEHAVIOR_TRANSLATIONS.get(x, x))
    return series
