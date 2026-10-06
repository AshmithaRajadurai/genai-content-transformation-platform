import re
from collections import Counter
from typing import Dict, List, Set

from backend.app.modules.nlp.schemas import KeywordItem

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


def extract_keywords(text: str, top_n: int = 8) -> List[KeywordItem]:
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
