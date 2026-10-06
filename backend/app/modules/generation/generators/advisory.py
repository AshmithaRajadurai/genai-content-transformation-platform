import re
import uuid
from backend.app.modules.nlp.schemas import NLPAnalysisResponse
from backend.app.modules.generation.schemas import AdvisoryArtefact


def structure_advisory(raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> AdvisoryArtefact:
    # Extract advisory ID (CVE or ADV)
    cve_match = re.search(r"\b(CVE-\d{4}-\d+)\b", raw_text, re.IGNORECASE)
    adv_id = cve_match.group(1).upper() if cve_match else f"ADV-2026-{uuid.uuid4().hex[:4].upper()}"

    # Severity
    severity = "CRITICAL (CVSS 9.8)" if "cve" in raw_text.lower() or "critical" in raw_text.lower() else "HIGH / OPERATIONAL"

    # Impact statement
    impact_match = re.search(r"1\.\s*EXECUTIVE OVERVIEW\n\s*(.*?)(?=\n\n2\.|\n2\.)", raw_text, re.DOTALL)
    impact = impact_match.group(1).strip() if impact_match else (nlp_data.key_facts[0] if nlp_data.key_facts else "Urgent operational risk identified.")

    # Affected systems from entities
    systems = [e.name for e in nlp_data.entities if e.type in ["PRODUCT", "TECHNOLOGY", "ORGANIZATION"]]
    if not systems:
        systems = ["Enterprise Core Services", "Authentication Infrastructure"]

    # Mitigations
    mitigations = [
        "Apply official vendor patch KB-89104 or upgrade affected binaries immediately.",
        "Restrict perimeter ingress traffic on administrative and authentication ports.",
        "Verify real-time audit logs for anomalous authentication requests."
    ]

    # References
    refs = [adv_id] + [e.name for e in nlp_data.entities if "CVE" in e.name or "KB" in e.name]

    return AdvisoryArtefact(
        advisory_id=adv_id,
        severity=severity,
        title=title,
        impact=impact,
        affected_systems=systems[:4],
        mitigation_steps=mitigations,
        monitoring_actions=[
            "Deploy telemetry alerts for unexpected privilege escalation attempts.",
            "Review daily egress network connections against known threat intelligence."
        ],
        references=list(set(refs))
    )
