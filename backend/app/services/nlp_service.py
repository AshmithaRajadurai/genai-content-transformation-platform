import math
import re
from collections import Counter
from typing import Dict, List, Set, Tuple

from backend.app.models.nlp_model import (
    KeywordItem,
    NamedEntity,
    NLPAnalysisRequest,
    NLPAnalysisResponse
)

# Standard English stopwords
STOPWORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can",
    "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't",
    "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
    "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him",
    "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't",
    "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor",
    "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out",
    "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some",
    "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there",
    "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to",
    "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's",
    "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've",
    "your", "yours", "yourself", "yourselves", "also", "including", "across", "within", "per", "using"
}

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


class NLPService:
    @classmethod
    def extract_keywords(cls, text: str, top_n: int = 8) -> List[KeywordItem]:
        """
        Extracts salient keywords and multi-word keyphrases using normalized
        term frequency and n-gram candidate ranking.
        """
        # Clean text into words
        raw_tokens = re.findall(r"\b[a-zA-Z0-9\-_]{2,}\b", text.lower())
        tokens = [t for t in raw_tokens if t not in STOPWORDS and not t.isdigit()]

        if not tokens:
            return []

        # 1. Unigram frequency
        unigram_counts = Counter(tokens)

        # 2. Bigrams & Trigrams extraction
        words_original = re.findall(r"\b[a-zA-Z0-9\-_]{2,}\b", text)
        ngrams: List[str] = []
        for i in range(len(words_original) - 1):
            w1 = words_original[i].lower()
            w2 = words_original[i + 1].lower()
            if w1 not in STOPWORDS and w2 not in STOPWORDS:
                ngrams.append(f"{w1} {w2}")
            if i < len(words_original) - 2:
                w3 = words_original[i + 2].lower()
                if w1 not in STOPWORDS and w3 not in STOPWORDS:
                    ngrams.append(f"{w1} {w2} {w3}")

        ngram_counts = Counter(ngrams)

        # Special priority for technical tags (e.g. CVE-..., KB-...)
        special_tags = re.findall(r"\b(?:cve|kb)-\d{4,}-\d{2,}\b", text, re.IGNORECASE)
        for tag in special_tags:
            ngram_counts[tag.lower()] += 5

        # Merge candidate scores
        candidates: Dict[str, float] = {}
        max_unigram = max(unigram_counts.values()) if unigram_counts else 1
        for word, count in unigram_counts.items():
            candidates[word] = count / max_unigram

        max_ngram = max(ngram_counts.values()) if ngram_counts else 1
        for phrase, count in ngram_counts.items():
            # Boost multi-word phrases for specificity
            score = (count / max_ngram) * 1.3
            candidates[phrase] = score

        # Sort and deduplicate overlapping substrings
        sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        selected: List[KeywordItem] = []
        selected_terms: List[str] = []

        for term, score in sorted_candidates:
            # Skip if already partially represented by a stronger multi-word phrase
            if any(term in s and term != s for s in selected_terms):
                continue
            norm_score = min(1.0, round(score * 0.9 + 0.1, 2))
            selected.append(KeywordItem(keyword=term, relevance=norm_score))
            selected_terms.append(term)
            if len(selected) >= top_n:
                break

        return selected

    @classmethod
    def identify_topics(cls, text: str) -> Tuple[str, List[str]]:
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

    @classmethod
    def extract_named_entities(cls, text: str) -> List[NamedEntity]:
        """
        Extracts domain entities using structural patterns and capitalization rules:
        - Vulnerabilities (CVE-..., CVSS)
        - Security Patches (KB-...)
        - Products & Systems (e.g. Enterprise Cloud Gateway)
        - Organizations (e.g. Research Groups, Ministries)
        - Roles (CTO, SecOps, Administrator)
        """
        entities_dict: Dict[Tuple[str, str], int] = Counter()

        # 1. CVE Vulnerabilities
        cves = re.findall(r"\bCVE-\d{4}-\d{4,7}\b", text, re.IGNORECASE)
        for cve in cves:
            entities_dict[(cve.upper(), "VULNERABILITY")] += 1

        # 2. Security Patches (KB numbers)
        kbs = re.findall(r"\bKB-\d{4,7}\b", text, re.IGNORECASE)
        for kb in kbs:
            entities_dict[(kb.upper(), "SECURITY_PATCH")] += 1

        # 3. Standards & Metrics
        cvss_matches = re.findall(r"\bCVSS(?::[\d.]+)?\b", text, re.IGNORECASE)
        for cvss in cvss_matches:
            entities_dict[(cvss.upper(), "BENCHMARK")] += 1

        # 4. Organizations (e.g. "Ministry of...", "... Research Group")
        org_matches = re.findall(r"\b(?:[A-Z][a-z]+ )*(?:Ministry|Institute|Agency|Group|Department|Corporation|Authority)\b", text)
        for org in org_matches:
            if len(org.strip()) > 3:
                entities_dict[(org.strip(), "ORGANIZATION")] += 1

        # 5. Technical Roles
        roles = re.findall(r"\b(?:CTO|CISO|CEO|CIO|SecOps|DevOps|DevSecOps|System Administrator|Auditor)\b", text, re.IGNORECASE)
        for role in roles:
            entities_dict[(role.upper(), "ROLE")] += 1

        # 6. Capitalized Multi-word Product Names
        product_candidates = re.findall(r"\b(?:Enterprise|Cloud|OpenAI|Google|Azure|AWS|Linux|Windows)\s+[A-Z][a-zA-Z0-9]+(?:\s+[A-Z][a-zA-Z0-9]+)?\b", text)
        for prod in product_candidates:
            entities_dict[(prod.strip(), "PRODUCT")] += 1

        # Convert to NamedEntity models
        entities: List[NamedEntity] = [
            NamedEntity(name=name, type=etype, frequency=count)
            for (name, etype), count in entities_dict.items()
        ]

        # Fallback if no specific regex triggered: extract capitalized multi-word phrases
        if not entities:
            general_proper = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)\b", text)
            for item in set(general_proper[:4]):
                entities.append(NamedEntity(name=item, type="ENTITY", frequency=1))

        return entities

    @classmethod
    def infer_content_type_and_tone(cls, text: str, primary_topic: str) -> Tuple[str, str]:
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

    @classmethod
    def extract_key_facts(cls, text: str, top_n: int = 4) -> List[str]:
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
        action_verbs = {"discovered", "detected", "identified", "reported", "requires", "upgrade", "restrict", "grew", "reduces", "slashing", "mitigate", "confirmed"}

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

    @classmethod
    def analyze(cls, payload: NLPAnalysisRequest) -> NLPAnalysisResponse:
        """
        Executes the full NLP semantic extraction pipeline:
        Keywords → Topics → Named Entities → Content Classification → Key Facts → Context Summary.
        """
        text = payload.content.strip()

        # 1. Keywords & Keyphrases
        keyword_items = cls.extract_keywords(text, top_n=8)
        keywords_list = [item.keyword for item in keyword_items]

        # 2. Topic Identification
        primary_topic, all_topics = cls.identify_topics(text)

        # 3. Named Entity Recognition (NER)
        entities = cls.extract_named_entities(text)

        # 4. Content Type & Tone
        content_type, detected_tone = cls.infer_content_type_and_tone(text, primary_topic)

        # 5. Key Facts Extraction
        key_facts = cls.extract_key_facts(text, top_n=4)

        # 6. Context Summary Formulation
        if key_facts:
            summary_context = f"{content_type}: {key_facts[0]}"
        else:
            summary_context = f"{content_type} concerning {primary_topic.lower()} with {len(keywords_list)} salient keywords extracted."

        # 7. Confidence Score
        confidence = min(99.0, max(85.0, 88.0 + (len(keyword_items) * 0.8) + (len(entities) * 0.5)))

        return NLPAnalysisResponse(
            topic=primary_topic,
            topics=all_topics,
            content_type=content_type,
            detected_tone=detected_tone,
            keywords=keywords_list,
            keyword_items=keyword_items,
            entities=entities,
            key_facts=key_facts,
            summary_context=summary_context,
            confidence_score=round(confidence, 1)
        )
