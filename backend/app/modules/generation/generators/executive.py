from backend.app.modules.nlp.schemas import NLPAnalysisResponse
from backend.app.modules.generation.schemas import ExecutiveSummaryArtefact


def structure_executive(raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> ExecutiveSummaryArtefact:
    tldr = nlp_data.key_facts[0] if nlp_data.key_facts else f"Strategic update concerning {nlp_data.topic} requiring leadership review."
    business_impact = (
        "Failure to address identified exposure impacts operational continuity, service-level compliance, and brand equity. "
        "Coordinated response across engineering and executive stakeholders mitigates systemic downtime risk."
    )
    recommendations = [
        "Mandate engineering priority on remediation sprint within 24 hours.",
        "Authorize interim operational safeguards on perimeter interfaces.",
        "Brief board audit committee on risk containment posture."
    ]

    return ExecutiveSummaryArtefact(
        title=title,
        tldr=tldr,
        business_impact=business_impact,
        key_points=nlp_data.key_facts[:4],
        recommendations=recommendations,
        decision_timeline="Immediate (24-48 Hours)"
    )
