RISK_KEYWORDS = {
    "high": [
        "indemnify",
        "penalty",
        "non-compete",
        "unilateral termination",
        "sole discretion",
        "irrevocable"
    ],
    "medium": [
        "arbitration",
        "jurisdiction",
        "auto renew",
        "lock-in"
    ]
}


def score_clause(text):
    t = text.lower()

    for k in RISK_KEYWORDS["high"]:
        if k in t:
            return "High"

    for k in RISK_KEYWORDS["medium"]:
        if k in t:
            return "Medium"

    return "Low"


def contract_score(scores):
    if "High" in scores:
        return "High"
    if "Medium" in scores:
        return "Medium"
    return "Low"
