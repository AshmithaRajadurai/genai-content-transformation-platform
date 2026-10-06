import re
from typing import Dict, List, Set, Tuple

# Domain Topic Lexicons
TOPIC_LEXICONS: Dict[str, Set[str]] = {
    "Enterprise AI & Autonomous Workflows": {
        "ai", "llm", "agentic", "agent", "agents", "multi-agent", "generative", "model", "models",
        "prompt", "prompts", "token", "tokens", "fidelity", "repurposing", "transformer", "transformers",
        "synthesis", "knowledge", "workflow", "workflows", "autonomous"
    },
    "Cybersecurity & Threat Intelligence": {
        "cve", "vulnerability", "vulnerabilities", "cvss", "exploit", "exploits", "patch", "patches",
        "security", "rce", "phishing", "malware", "firewall", "ingress", "privilege", "privileges",
        "attacker", "attackers", "advisory", "advisories", "root", "authentication", "breach",
        "breaches", "mitigation", "threat", "threats", "payload", "remediation"
    },
    "Cloud Architecture & Infrastructure": {
        "cloud", "gateway", "gateways", "cluster", "clusters", "server", "servers", "port", "ports",
        "api", "apis", "network", "traffic", "latency", "docker", "kubernetes", "endpoint",
        "endpoints", "infrastructure", "ingress", "uptime"
    },
    "Executive Strategy & Industry Research": {
        "cto", "c-suite", "executive", "executives", "survey", "surveys", "briefing", "time-to-publish",
        "productivity", "findings", "adoption", "accelerated", "yoy", "roi", "strategy", "organizations"
    }
}


def identify_topics(text: str) -> Tuple[str, List[str]]:
    """
    Classifies the text into primary and secondary topical categories
    based on domain lexicon densities.
    """
    raw_words = re.findall(r"\b[a-zA-Z0-9\-_]+\b", text.lower())
    words = set(raw_words)
    for w in list(words):
        if w.endswith("ies") and len(w) > 4:
            words.add(w[:-3] + "y")
        elif w.endswith("s") and len(w) > 3:
            words.add(w[:-1])

    scores: Dict[str, int] = {}
    for domain, lexicon in TOPIC_LEXICONS.items():
        matched = words.intersection(lexicon)
        scores[domain] = len(matched)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    active_topics = [domain for domain, count in ranked if count > 0]

    if not active_topics:
        return "General Knowledge & Communication", ["General Knowledge & Communication"]

    primary_topic = active_topics[0]
    return primary_topic, active_topics
