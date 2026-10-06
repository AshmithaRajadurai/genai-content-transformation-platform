import re
from collections import Counter
from typing import Dict, List, Tuple

from backend.app.modules.nlp.schemas import NamedEntity


def extract_named_entities(text: str) -> List[NamedEntity]:
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
