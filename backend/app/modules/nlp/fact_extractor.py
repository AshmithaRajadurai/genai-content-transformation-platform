import re
from typing import List, Tuple


def infer_content_type_and_tone(text: str, primary_topic: str) -> Tuple[str, str]:
    """
    Determines the formal document classification and communication tone.
    """
    lower = text.lower()

    # Classification
    if "cve" in lower or "advisory" in lower or "vulnerability" in lower:
        content_type = "Critical Security Advisory"
    elif "research" in lower or "findings" in lower or "survey" in lower:
        content_type = "Strategic Research Briefing"
    elif "incident" in lower or "breach" in lower or "outage" in lower:
        content_type = "Technical Incident Report"
    elif "policy" in lower or "compliance" in lower or "standard" in lower:
        content_type = "Enterprise Policy Notice"
    else:
        content_type = f"{primary_topic.split('&')[0].strip()} Briefing"

    # Tone
    if any(w in lower for w in ["critical", "emergency", "immediately", "urgent", "exploit"]):
        detected_tone = "Urgent & Action-Oriented"
    elif any(w in lower for w in ["research", "accelerated", "findings", "shift", "future", "growth"]):
        detected_tone = "Thought Leadership & Strategic"
    elif any(w in lower for w in ["mitigation", "steps", "procedure", "specification", "version"]):
        detected_tone = "Technical & In-depth"
    else:
        detected_tone = "Professional & Authoritative"

    return content_type, detected_tone


def extract_key_facts(text: str, top_n: int = 4) -> List[str]:
    """
    Extracts salient factual assertions by scoring individual sentences
    based on metric presence, entity references, and informational verbs.
    """
    # Split text into candidate sentences
    raw_sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])|\n+", text)
    sentences = [s.strip() for s in raw_sentences if len(s.strip()) >= 25]

    if not sentences:
        return ["Primary statement extracted from source input."]

    scored_sentences: List[Tuple[str, float]] = []
    action_verbs = {
        "discovered", "detected", "identified", "reported", "requires",
        "upgrade", "restrict", "grew", "reduces", "slashing", "mitigate", "confirmed"
    }

    for sent in sentences:
        score = 0.0
        lower = sent.lower()

        # Boost if contains metrics, numbers, or percentages
        if re.search(r"\b\d+(?:\.\d+)?%?\b", sent):
            score += 2.0

        # Boost if contains CVE/patch tags
        if re.search(r"\b(?:cve|kb)-\d+", lower):
            score += 3.0

        # Boost if contains key operational verbs
        if any(v in lower for v in action_verbs):
            score += 1.5

        # Length normalization (favor substantive sentences over ultra-short or run-ons)
        word_count = len(sent.split())
        if 8 <= word_count <= 35:
            score += 1.0

        scored_sentences.append((sent, score))

    # Sort by score descending and take top N
    scored_sentences.sort(key=lambda x: x[1], reverse=True)
    top_facts = [s for s, _ in scored_sentences[:top_n]]
    return top_facts
