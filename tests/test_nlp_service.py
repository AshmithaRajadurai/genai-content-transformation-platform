import pytest
from backend.app.models.nlp_model import NLPAnalysisRequest
from backend.app.services.nlp_service import NLPService


def test_extract_keywords():
    text = (
        "Enterprise multi-agent AI architectures reduce content repurposing time "
        "while sustaining factual fidelity across communication channels."
    )
    keywords = NLPService.extract_keywords(text, top_n=6)
    assert len(keywords) > 0
    keyword_terms = [k.keyword for k in keywords]
    assert any("ai" in t or "multi-agent" in t or "fidelity" in t for t in keyword_terms)


def test_identify_topics_cybersecurity():
    security_text = (
        "Critical vulnerability CVE-2026-4401 in gateway authentication module. "
        "Attackers can achieve root privileges. Apply patch KB-89104 immediately."
    )
    primary_topic, all_topics = NLPService.identify_topics(security_text)
    assert "Cybersecurity" in primary_topic
    assert "Cybersecurity & Threat Intelligence" in all_topics


def test_identify_topics_enterprise_ai():
    ai_text = (
        "Adoption of multi-agent generative AI models grew 280% YoY according to survey findings."
    )
    primary_topic, _ = NLPService.identify_topics(ai_text)
    assert "Enterprise AI" in primary_topic


def test_named_entity_recognition():
    text = (
        "The Ministry of Technology discovered CVE-2026-4401 in Enterprise Cloud Gateway. "
        "SecOps engineers must deploy patch KB-89104 according to CVSS 9.8 guidelines."
    )
    entities = NLPService.extract_named_entities(text)
    entity_names = [e.name for e in entities]
    entity_types = {e.name: e.type for e in entities}

    assert any("CVE-2026-4401" in name for name in entity_names)
    assert any("KB-89104" in name for name in entity_names)
    assert any("Ministry" in name for name in entity_names)
    assert any(etype == "VULNERABILITY" for etype in entity_types.values())


def test_key_facts_extraction():
    text = (
        "A remote code execution vulnerability was detected in Cloud Gateway. "
        "Severity is rated at 9.8 Critical. "
        "Enterprise adoption accelerated 280% in Q1 2026. "
        "Apply version 4.9.2 immediately."
    )
    facts = NLPService.extract_key_facts(text, top_n=3)
    assert len(facts) >= 2
    # Ensure facts contain numbers or key verbs
    assert any("9.8" in f or "280%" in f or "vulnerability" in f.lower() for f in facts)


def test_full_nlp_analysis_user_prompt_example():
    # Exactly matching user's architecture specification:
    user_example = "The Ministry issued a cybersecurity advisory after detecting a phishing campaign targeting financial institutions."
    payload = NLPAnalysisRequest(content=user_example)
    result = NLPService.analyze(payload)

    assert "Cybersecurity" in result.topic
    assert "Advisory" in result.content_type
    assert result.confidence_score > 85.0

    # Keywords should capture salient concepts
    keywords_lower = [k.lower() for k in result.keywords]
    assert any("cybersecurity" in k or "phishing" in k or "financial" in k for k in keywords_lower)

    # Entity should capture Ministry
    assert any("Ministry" in e.name for e in result.entities)

    # Key facts should capture the detected phishing campaign
    assert len(result.key_facts) >= 1
