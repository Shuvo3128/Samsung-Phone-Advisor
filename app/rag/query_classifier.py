import re
from enum import Enum
from typing import Tuple, Dict


# ======================================================
# INTENT ENUM
# ======================================================
class Intent(str, Enum):
    GREETING = "GREETING"
    HELP = "HELP"
    DOMAIN = "DOMAIN"
    AMBIGUOUS = "AMBIGUOUS"
    FALLBACK = "FALLBACK"

    # domain sub-intents
    COMPARE = "COMPARE"
    RECOMMEND = "RECOMMEND"
    SPEC = "SPEC"


# ======================================================
# HIGH-LEVEL QUERY CLASSIFIER (Conversation vs Domain)
# ======================================================
class QueryClassifier:

    GREETING_PATTERNS = [
        r"\bhi\b",
        r"\bhello\b",
        r"\bhey\b",
        r"\bhow are you\b",
    ]

    HELP_PATTERNS = [
        r"\bhelp\b",
        r"\bwhat can you do\b",
        r"\bhow does this work\b",
    ]

    DOMAIN_KEYWORDS = [
        "samsung", "galaxy", "compare", "vs",
        "battery", "camera", "price",
        "best", "recommend", "spec", "under",
    ]

    @staticmethod
    def classify(question: str) -> Intent:
        q = question.lower().strip()

        if not q or len(q) < 2:
            return Intent.FALLBACK

        # Greeting
        for p in QueryClassifier.GREETING_PATTERNS:
            if re.search(p, q):
                return Intent.GREETING

        # Help
        for p in QueryClassifier.HELP_PATTERNS:
            if re.search(p, q):
                return Intent.HELP

        # Domain (Samsung / phones)
        if any(k in q for k in QueryClassifier.DOMAIN_KEYWORDS):
            if len(q.split()) < 3:
                return Intent.AMBIGUOUS
            return Intent.DOMAIN

        return Intent.FALLBACK


# ======================================================
# DOMAIN INTENT CLASSIFIER
# ======================================================
def classify_domain_intent(question: str) -> Intent:
    q = question.lower()

    if "compare" in q or "vs" in q:
        return Intent.COMPARE

    if "best" in q or "recommend" in q or "under" in q:
        return Intent.RECOMMEND

    return Intent.SPEC


# ======================================================
# ENTITY EXTRACTION
# ======================================================
def extract_entities(question: str, intent: Intent) -> Dict:
    entities = {}

    q = question.lower().strip()

    if intent == Intent.COMPARE:
        clean_q = re.sub(r"\bcompare\b", "", q)
        parts = re.split(r"\band\b|\bvs\b", clean_q, flags=re.IGNORECASE)

        if len(parts) >= 2:
            entities["model_1"] = parts[0].strip().title()
            entities["model_2"] = parts[1].strip().title()

    elif intent == Intent.RECOMMEND:
        match = re.search(r"under\s*\$?(\d+)", q)
        entities["max_price"] = int(match.group(1)) if match else 1000

    else:  # SPEC
        # remove common spec phrases
        clean_model = re.sub(
            r"(what are the specs of|show specs of|specs of|what is the specs of)",
            "",
            q,
            flags=re.IGNORECASE,
        )
        entities["model_name"] = clean_model.strip().title()

    return entities




# ======================================================
# MAIN HELPER (USED BY ROUTER)
# ======================================================
def analyze_query(question: str) -> Tuple[Intent, Dict]:
    """
    Returns:
    - domain_intent (COMPARE / RECOMMEND / SPEC)
    - extracted entities dict
    """
    domain_intent = classify_domain_intent(question)
    entities = extract_entities(question, domain_intent)
    return domain_intent, entities
