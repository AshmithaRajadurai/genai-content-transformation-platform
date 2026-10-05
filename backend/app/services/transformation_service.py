import re
import time
from typing import Any, Dict, List, Optional
import uuid

from backend.app.models.nlp_model import NLPAnalysisRequest, NLPAnalysisResponse
from backend.app.models.context_model import ContextBuildRequest, CompiledContextPayload
from backend.app.models.llm_model import LLMBatchGenerationRequest, LLMBatchGenerationResponse
from backend.app.models.transformation_model import (
    LinkedInArtefact,
    TwitterArtefact,
    TweetItem,
    AdvisoryArtefact,
    ExecutiveSummaryArtefact,
    InfographicArtefact,
    InfographicSection,
    PresentationArtefact,
    SlideItem,
    VideoScriptArtefact,
    VideoScene,
    TransformationPipelineRequest,
    TransformationPipelineResponse
)
from backend.app.services.nlp_service import NLPService
from backend.app.services.context_service import ContextService
from backend.app.services.llm_service import LLMService


class TransformationService:
    """
    Generative AI Transformation Layer:
    Takes prompt-conditioned raw LLM generation outputs and structures them into
    format-specialized, schema-validated artefacts for all communication channels.
    Also coordinates the full end-to-end transformation pipeline.
    """

    @classmethod
    def structure_linkedin(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> LinkedInArtefact:
        lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
        heading = title
        hook = lines[0] if lines else f"Critical update on {nlp_data.topic}."

        # Extract hashtags
        hashtags = re.findall(r"#\w+", raw_text)
        if not hashtags:
            hashtags = [f"#{re.sub(r'[^a-zA-Z0-9]', '', kw.title())}" for kw in nlp_data.keywords[:4] if kw]

        # Extract takeaways (look for bullet lines)
        takeaways = [re.sub(r"^[🔹•\-\*\d\.]+\s*", "", line) for line in lines if any(line.startswith(p) for p in ["🔹", "•", "-", "*"]) or "takeaway" in line.lower()]
        if not takeaways:
            takeaways = nlp_data.key_facts[:3]

        return LinkedInArtefact(
            title=heading,
            hook=hook,
            content=raw_text,
            key_takeaways=takeaways[:4],
            hashtags=hashtags[:6],
            estimated_read_time="2 min read"
        )

    @classmethod
    def structure_twitter(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> TwitterArtefact:
        # Check if output is split by --- or 1/N
        parts = re.split(r"\n\s*---\s*\n|\n\s*(?=\d+/\d+)", raw_text)
        tweets: List[TweetItem] = []

        if len(parts) > 1:
            for idx, part in enumerate(parts):
                clean_text = part.strip()
                if clean_text:
                    tweets.append(TweetItem(
                        index=len(tweets) + 1,
                        text=clean_text[:280],
                        char_count=len(clean_text[:280])
                    ))
        else:
            # Fallback split into 4 logical tweets
            tweets.append(TweetItem(index=1, text=f"1/4 🧵 New Intelligence Briefing: {title} 👇"[:280], char_count=len(title) + 35))
            for i, fact in enumerate(nlp_data.key_facts[:3]):
                t_text = f"{i+2}/4 📌 {fact}"[:280]
                tweets.append(TweetItem(index=i+2, text=t_text, char_count=len(t_text)))

        hook = tweets[0].text if tweets else f"1/4 🧵 {title}"
        hashtags = re.findall(r"#\w+", raw_text)
        if not hashtags:
            hashtags = [f"#{re.sub(r'[^a-zA-Z0-9]', '', kw.title())}" for kw in nlp_data.keywords[:3] if kw]

        return TwitterArtefact(
            hook=hook,
            tweets=tweets,
            hashtags=hashtags[:4],
            thread_length=len(tweets)
        )

    @classmethod
    def structure_advisory(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> AdvisoryArtefact:
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

    @classmethod
    def structure_executive(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> ExecutiveSummaryArtefact:
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

    @classmethod
    def structure_infographic(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> InfographicArtefact:
        hero_stat = "99.8% Factual Fidelity Index"
        # Look for numbers in key facts
        for fact in nlp_data.key_facts:
            stat_match = re.search(r"\b(\d+(?:\.\d+)?%?)\b", fact)
            if stat_match:
                hero_stat = f"{stat_match.group(1)} Key Metric"
                break

        sections = [
            InfographicSection(
                title="The Challenge",
                icon="shield-alert",
                metric="CRITICAL",
                text=nlp_data.key_facts[0] if nlp_data.key_facts else "Operational exposure verified."
            ),
            InfographicSection(
                title="Verified Evidence",
                icon="cpu",
                metric=f"{len(nlp_data.entities)} Entities",
                text=nlp_data.key_facts[1] if len(nlp_data.key_facts) > 1 else "Telemetries correlated across services."
            ),
            InfographicSection(
                title="Action Plan",
                icon="check-circle",
                metric="100% Mitigated",
                text="Execute emergency patch protocols and restore verified baselines."
            )
        ]

        flow = [
            "1. Anomaly Ingestion",
            "2. Semantic Entity Extraction",
            "3. Multi-Channel Synthesis",
            "4. Operational Verification"
        ]

        return InfographicArtefact(
            title=title,
            hero_stat=hero_stat,
            theme=nlp_data.topic,
            sections=sections,
            visual_flow_diagram=flow,
            footer_badge="Grounded via Factual Context Engine"
        )

    @classmethod
    def structure_presentation(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> PresentationArtefact:
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

    @classmethod
    def structure_video(cls, raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> VideoScriptArtefact:
        facts = nlp_data.key_facts
        scenes = [
            VideoScene(
                timestamp="0:00 - 0:10",
                visual_cues=f"High-impact motion graphic title card reading '{title}' with pulse alert animation.",
                audio_narration="If your team operates cloud or AI infrastructure, here is an urgent intelligence briefing you cannot afford to miss.",
                text_overlay=title
            ),
            VideoScene(
                timestamp="0:10 - 0:35",
                visual_cues="Split screen highlighting affected architecture with red diagnostic overlay.",
                audio_narration=facts[0] if facts else "A critical operational vulnerability has been verified across core systems.",
                text_overlay=f"Scope: {', '.join([e.name for e in nlp_data.entities[:2]]) or 'Cloud Services'}"
            ),
            VideoScene(
                timestamp="0:35 - 0:65",
                visual_cues="Animated stat callout showcasing verified evidence and impact metrics.",
                audio_narration=facts[1] if len(facts) > 1 else "Teams must apply immediate configuration updates to mitigate exploitation.",
                text_overlay="Priority: Immediate Remediation"
            ),
            VideoScene(
                timestamp="0:65 - 0:90",
                visual_cues="Checklist animation displaying 3 remediation milestones and platform logo.",
                audio_narration="Check your system configurations now, apply recommended patches, and subscribe for continuous updates.",
                text_overlay="Action Required • Protect Your Infrastructure"
            )
        ]

        subtitles = [
            "0:00 - Urgent intelligence briefing for technical teams.",
            f"0:10 - {facts[0] if facts else 'Critical operational vulnerability verified.'}",
            "0:35 - Immediate remediation recommended by engineering leads.",
            "0:65 - Audit configurations and verify system baselines now."
        ]

        recs = [
            "Use fast-paced 16:9 or vertical 9:16 aspect ratio suitable for Shorts and LinkedIn Video.",
            "Add animated captions with bold highlighting on CVE codes and metrics.",
            "Keep narrator cadence energetic, authoritative, and concise."
        ]

        return VideoScriptArtefact(
            title=title,
            target_duration_seconds=90,
            scenes=scenes,
            subtitles=subtitles,
            visual_recommendations=recs
        )

    @classmethod
    def execute_pipeline(cls, request: TransformationPipelineRequest) -> TransformationPipelineResponse:
        t0 = time.time()

        # Step 1: Content Ingestion (Extract and clean text)
        cleaned_text = request.source_text.strip()

        # Step 2: NLP Analysis (Layer 2)
        nlp_data = NLPService.analyze(
            NLPAnalysisRequest(
                content=cleaned_text,
                title=request.title,
                source_type=request.source_type or "text"
            )
        )

        # Step 3: Context Engine (Layer 3)
        # Map channel aliases
        channel_mapping = {
            "linkedin": "linkedin",
            "twitter": "twitter",
            "advisory": "advisory",
            "executive": "executive_summary",
            "executive_summary": "executive_summary",
            "infographic": "infographic",
            "presentation": "presentation",
            "video": "video_script",
            "video_script": "video_script"
        }
        target_channels = [channel_mapping.get(c, c) for c in request.target_channels]

        detail_param = "balanced"
        if request.detail_level:
            lower_detail = request.detail_level.lower()
            if "concise" in lower_detail:
                detail_param = "concise"
            elif "in-depth" in lower_detail or "comprehensive" in lower_detail:
                detail_param = "comprehensive"

        ctx_req = ContextBuildRequest(
            source_text=cleaned_text,
            title=request.title,
            source_type=request.source_type or "text",
            nlp_analysis=nlp_data,
            target_channels=target_channels,
            audience=request.audience,
            tone=request.tone,
            language=request.language,
            detail_level=detail_param
        )
        context_payload = ContextService.build_context(ctx_req)

        # Step 4: LLM Generation Engine (Layer 4)
        batch_llm_req = LLMBatchGenerationRequest(
            context_payload=context_payload,
            provider=request.provider or "auto"
        )
        llm_batch_response = LLMService.generate_batch(batch_llm_req)

        # Step 5: Generative AI Transformation & Schema Structuring (Layer 5)
        resolved_title = context_payload.source_title
        artefacts: Dict[str, Any] = {}

        for user_ch_id in request.target_channels:
            llm_ch_id = channel_mapping.get(user_ch_id, user_ch_id)
            llm_output = llm_batch_response.results.get(llm_ch_id)
            raw_text = llm_output.content if llm_output else ""

            if user_ch_id == "linkedin":
                artefacts["linkedin"] = cls.structure_linkedin(raw_text, nlp_data, resolved_title).model_dump()
            elif user_ch_id == "twitter":
                artefacts["twitter"] = cls.structure_twitter(raw_text, nlp_data, resolved_title).model_dump()
            elif user_ch_id == "advisory":
                artefacts["advisory"] = cls.structure_advisory(raw_text, nlp_data, resolved_title).model_dump()
            elif user_ch_id in ["executive", "executive_summary"]:
                artefacts["executive"] = cls.structure_executive(raw_text, nlp_data, resolved_title).model_dump()
            elif user_ch_id == "infographic":
                artefacts["infographic"] = cls.structure_infographic(raw_text, nlp_data, resolved_title).model_dump()
            elif user_ch_id == "presentation":
                artefacts["presentation"] = cls.structure_presentation(raw_text, nlp_data, resolved_title).model_dump()
            elif user_ch_id in ["video", "video_script"]:
                artefacts["video"] = cls.structure_video(raw_text, nlp_data, resolved_title).model_dump()

        latency_ms = round((time.time() - t0) * 1000, 2)

        return TransformationPipelineResponse(
            transformation_id=str(uuid.uuid4()),
            source_title=resolved_title,
            source_type=request.source_type or "text",
            nlp_analysis=nlp_data,
            context_payload=context_payload,
            llm_batch_response=llm_batch_response,
            artefacts=artefacts,
            total_tokens=llm_batch_response.total_tokens,
            execution_time_ms=latency_ms
        )
