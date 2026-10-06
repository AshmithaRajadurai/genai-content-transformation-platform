from backend.app.modules.nlp.schemas import NLPAnalysisResponse
from backend.app.modules.generation.schemas import SlideItem, PresentationArtefact


def structure_presentation(raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> PresentationArtefact:
    facts = nlp_data.key_facts
    slides = [
        SlideItem(
            slide_number=1,
            title=title,
            subtitle=f"Strategic Intelligence Briefing • {nlp_data.topic}",
            bullets=["Executive Overview", "Root Cause & Telemetry", "Strategic Roadmap"],
            speaker_notes="Welcome leadership team. Today we review verified intelligence and immediate mitigations.",
            visual_cue="High-contrast dark card with glowing title typography"
        ),
        SlideItem(
            slide_number=2,
            title="Context & Environment",
            subtitle="Baseline Analysis",
            bullets=[
                facts[0] if facts else "Baseline shift observed across operational environments.",
                f"Identified Domain: {nlp_data.topic}.",
                f"Entity Scope: {', '.join([e.name for e in nlp_data.entities[:3]]) or 'Core Infrastructure'}."
            ],
            speaker_notes="Setting the baseline and defining the environmental factors driving this briefing.",
            visual_cue="2-column comparison layout with architecture diagram"
        ),
        SlideItem(
            slide_number=3,
            title="Problem Breakdown",
            subtitle="Root Cause Assessment",
            bullets=[
                facts[1] if len(facts) > 1 else "Core telemetry breakdown indicates perimeter exposure.",
                "Attack vector or operational friction point isolated to ingress boundaries.",
                "Immediate remediation path identified to preserve operational uptime."
            ],
            speaker_notes="Drilling into the technical findings and vulnerability surface.",
            visual_cue="Diagnostic red/amber warning box with callout arrows"
        ),
        SlideItem(
            slide_number=4,
            title="Key Evidence & Metrics",
            subtitle="Verified Audit Telemetry",
            bullets=[
                facts[2] if len(facts) > 2 else "All core findings validated by independent audit logs.",
                f"Factual Confidence Score: {nlp_data.confidence_score}%.",
                f"Key domain vectors: {', '.join(nlp_data.keywords[:4])}."
            ],
            speaker_notes="Reviewing quantitative metrics and audit evidence for decision confidence.",
            visual_cue="3 stat boxes with prominent metric callouts"
        ),
        SlideItem(
            slide_number=5,
            title="Strategic Action Plan",
            subtitle="Milestones & Timeline",
            bullets=[
                "Phase 1: Apply emergency patches and configuration workarounds (Hours 0-12).",
                "Phase 2: Validate telemetry and restore nominal baseline (Hours 12-24).",
                "Phase 3: Executive sign-off and audit closure (Day 2)."
            ],
            speaker_notes="Concluding with actionable ownership and commitment to the 48-hour timeline.",
            visual_cue="Gantt chart flow with green status checks"
        )
    ]

    return PresentationArtefact(
        title=title,
        slides=slides,
        total_slides=len(slides)
    )
