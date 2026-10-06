from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

from backend.app.modules.context.schemas import (
    ContextBuildRequest,
    CompiledContextPayload,
    ChannelContextPrompt,
    ChannelInstruction,
)
from backend.app.modules.nlp.schemas import NLPAnalysisRequest, NLPAnalysisResponse, NamedEntity
from backend.app.modules.nlp.service import NLPService

CHANNEL_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "linkedin": {
        "name": "LinkedIn Thought Leadership Post",
        "default_audience": "Enterprise leaders, industry peers, and professionals",
        "default_tone": "Insightful, professional, and forward-looking",
        "length_constraints": "200-350 words formatted with readable white space and bullet highlights",
        "guidelines": [
            "Start with an attention-grabbing, authoritative hook (no clickbait).",
            "State the strategic challenge or insight derived from the core facts.",
            "List 3-4 concise, high-value bullet takeaways.",
            "Close with an engaging discussion prompt / call-to-action.",
            "Include 3-5 relevant hashtags based on extracted keywords."
        ],
        "required_elements": ["Hook", "Core Context", "3 Key Takeaways", "Call-to-Action", "Hashtags"]
    },
    "twitter": {
        "name": "X / Twitter Thread",
        "default_audience": "Tech community, researchers, and fast-paced industry followers",
        "default_tone": "Punchy, concise, urgent, and factual",
        "length_constraints": "4-6 connected tweets, each under 280 characters",
        "guidelines": [
            "Tweet 1: High-impact hook summarizing the critical development with thread emoji (🧵👇).",
            "Tweets 2-4: Deep-dive into specific facts, affected entities, and implications.",
            "Tweet 5: Practical takeaway, mitigation, or actionable conclusion.",
            "Number tweets clearly as 1/, 2/, 3/ etc."
        ],
        "required_elements": ["Tweet 1 Hook", "Numbered Fact Tweets", "Conclusion / Action", "Key Hashtags"]
    },
    "advisory": {
        "name": "Security & Operational Advisory",
        "default_audience": "DevSecOps, IT Administrators, and Engineering Leaders",
        "default_tone": "Authoritative, precise, objective, and urgent",
        "length_constraints": "Structured formal briefing (300-600 words)",
        "guidelines": [
            "Include Document Metadata: Advisory ID/Title, Severity Level, Date, and Scope.",
            "Executive Overview: 2-3 sentence synopsis of the issue.",
            "Technical Assessment & Affected Entities: Explicit list of software, CVEs, or systems.",
            "Root Cause & Risk Implications: Direct impact on operations or compliance.",
            "Remediation / Immediate Action Steps: Prioritized checklist of mitigations.",
            "References & Ground Truth Anchors."
        ],
        "required_elements": ["Severity / Impact", "Affected Scope", "Technical Summary", "Actionable Mitigations"]
    },
    "executive_summary": {
        "name": "Executive C-Suite Summary",
        "default_audience": "CEOs, CIOs, Board Members, and Senior Decision Makers",
        "default_tone": "Strategic, clear, risk-conscious, and commercially astute",
        "length_constraints": "1-page briefing (250-400 words)",
        "guidelines": [
            "Executive TL;DR: Bottom-line upfront summary.",
            "Business & Strategic Impact: Financial, operational, and reputational risk analysis.",
            "Key Verified Facts: 3-5 crucial factual data points.",
            "Strategic Recommendations: Clear decision matrix and recommended next steps."
        ],
        "required_elements": ["TL;DR", "Business Impact", "Critical Facts", "Leadership Next Steps"]
    },
    "infographic": {
        "name": "Infographic Data Layout & Blueprint",
        "default_audience": "Visual learners, social audiences, and conference attendees",
        "default_tone": "Graphic, structured, clear, and data-driven",
        "length_constraints": "Structured visual blueprint (Header, Hero Metric, 3 Panels, Footer)",
        "guidelines": [
            "Header & Subtitle: High-contrast title and 1-line explainer.",
            "Hero Metric / Stat Callout: Single most impactful number or key assertion.",
            "3 Key Visual Sections: Structured blocks (e.g. The Challenge, The Facts, The Solution).",
            "Icon / Visual suggestions for each section.",
            "Footer: Source attribution and key takeaway badge."
        ],
        "required_elements": ["Hero Stat", "3 Visual Sections", "Visual Cue Descriptions", "Takeaway Badge"]
    },
    "presentation": {
        "name": "Slide Presentation Deck",
        "default_audience": "Stakeholders, clients, and internal teams in meetings",
        "default_tone": "Structured, presentation-ready, bulleted, and persuasive",
        "length_constraints": "5-slide structured deck layout",
        "guidelines": [
            "Slide 1: Title, Subtitle, Presenter Context, and Target Agenda.",
            "Slide 2: Background, Context, and Market/Technical Drivers.",
            "Slide 3: Core Problem or Findings Breakdown.",
            "Slide 4: Key Evidentiary Facts and Metrics.",
            "Slide 5: Strategic Action Plan, Timeline, and Next Milestones."
        ],
        "required_elements": ["5 Slide Titles", "Speaker Notes per slide", "Key Bullets", "Visual Layout Notes"]
    },
    "video_script": {
        "name": "Short-Form Video Script & Package",
        "default_audience": "YouTube / Tech shorts / Explainer audience",
        "default_tone": "Engaging, conversational, dynamic, and clear",
        "length_constraints": "60-90 second spoken script with timecoded scene directions",
        "guidelines": [
            "Format script in a 2-column table or structured blocks: [Timestamp | Visual / B-Roll | Audio / Spoken Voiceover].",
            "Scene 1 (0:00-0:10): 3-second visual hook and intro question.",
            "Scene 2 (0:10-0:35): Problem breakdown with on-screen text overlays.",
            "Scene 3 (0:35-0:65): The core revelation, facts, and breakdown.",
            "Scene 4 (0:65-0:80): Practical implications and what it means.",
            "Scene 5 (0:80-0:90): Clear outro call to action."
        ],
        "required_elements": ["Timecoded Scenes", "Visual / B-Roll Prompts", "Exact Voiceover Text", "Outro CTA"]
    }
}


class ContextService:
    """
    Context Engine:
    Combines raw source documents, extracted NLP entities/facts/keywords,
    target audience personas, and strict factual guardrails into optimized,
    channel-specialized prompts ready for the LLM Engine.
    """

    CHANNEL_DEFINITIONS = CHANNEL_DEFINITIONS

    @classmethod
    def resolve_title(cls, request: ContextBuildRequest, nlp_data: NLPAnalysisResponse) -> str:
        if request.title and request.title.strip():
            return request.title.strip()
        first_line = request.source_text.strip().split("\n")[0].strip("# \t\r")
        if first_line and len(first_line) <= 100:
            return first_line
        return f"{nlp_data.topic} Intelligence Briefing"

    @classmethod
    def generate_global_system_instruction(
        cls,
        nlp_data: NLPAnalysisResponse,
        audience: str,
        tone: str,
        language: str,
        detail_level: str
    ) -> str:
        entities_list = ", ".join([f"{e.name} ({e.type})" for e in nlp_data.entities[:8]])
        if not entities_list:
            entities_list = "None identified"

        return (
            "You are the Core Generative AI Engine for the Content Transformation Platform.\n"
            "Your objective is to transform raw source intelligence into high-impact, channel-specialized artefacts.\n\n"
            "STRICT FACTUAL GROUNDING & ANTI-HALLUCINATION RULES:\n"
            "1. Ground all outputs strictly in the provided Core Verified Facts and Source Context.\n"
            "2. Preserve all specific entity names, CVE codes, dates, and metrics exactly as provided without alteration.\n"
            f"   Protected Entities: {entities_list}\n"
            "3. Do NOT fabricate statistics, CVE identifiers, technical capabilities, or external quotes not grounded in the source.\n"
            f"4. Target Audience: {audience}\n"
            f"5. Communication Tone: {tone}\n"
            f"6. Output Language: {language}\n"
            f"7. Detail Depth: {detail_level.upper()} (respect word count limits and structural constraints).\n"
        )

    @classmethod
    def generate_channel_prompt(
        cls,
        channel_id: str,
        source_title: str,
        nlp_data: NLPAnalysisResponse,
        audience: str,
        tone: str,
        language: str,
        detail_level: str
    ) -> ChannelContextPrompt:
        channel_config = CHANNEL_DEFINITIONS.get(
            channel_id,
            {
                "name": f"{channel_id.replace('_', ' ').title()} Output",
                "default_audience": audience,
                "default_tone": tone,
                "length_constraints": "Standard balanced output",
                "guidelines": ["Produce high quality structured content grounded in the provided facts."],
                "required_elements": ["Key Facts", "Structured Breakdown"]
            }
        )

        channel_name = channel_config["name"]
        length_constraints = channel_config["length_constraints"]
        guidelines = channel_config.get("guidelines", [])
        required_elements = channel_config.get("required_elements", [])

        # Formulate Channel System Prompt
        system_prompt = (
            f"You are an elite content transformation specialist specializing in {channel_name}.\n"
            f"Target Audience: {audience} (Tone: {tone}).\n"
            f"Target Length: {length_constraints}.\n"
            f"Language: {language}.\n"
            "Execution Directives:\n" +
            "\n".join([f"- {g}" for g in guidelines]) + "\n" +
            "Mandatory Output Elements:\n" +
            "\n".join([f"- [REQUIRED] {elem}" for elem in required_elements])
        )

        # Formulate Grounding Rules
        grounding_rules = [
            f"Stay strictly truthful to the {len(nlp_data.key_facts)} verified facts extracted from '{source_title}'.",
            "Do not introduce speculative claims or ungrounded statistics.",
            f"Format specifically for {channel_name} with clear headings and readable spacing."
        ]
        if nlp_data.entities:
            top_entity_names = [e.name for e in nlp_data.entities[:6]]
            grounding_rules.append(f"Ensure accurate reference to: {', '.join(top_entity_names)}.")

        # Build Formatted User Prompt
        facts_block = "\n".join([f"{i+1}. {fact}" for i, fact in enumerate(nlp_data.key_facts)])
        keywords_block = ", ".join(nlp_data.keywords[:10])
        entities_block = ", ".join([f"{e.name} [{e.type}]" for e in nlp_data.entities[:8]])

        user_prompt = (
            f"DOCUMENT TITLE: {source_title}\n"
            f"IDENTIFIED TOPIC: {nlp_data.topic} ({nlp_data.content_type})\n"
            f"KEYWORDS: {keywords_block}\n"
            f"RECOGNIZED ENTITIES: {entities_block if entities_block else 'None'}\n\n"
            "CORE VERIFIED FACTS:\n"
            f"{facts_block}\n\n"
            "CONTEXT SUMMARY:\n"
            f"{nlp_data.summary_context}\n\n"
            f"TASK INSTRUCTION:\n"
            f"Transform this verified intelligence into a publication-ready {channel_name}.\n"
            f"Audience: {audience}\n"
            f"Tone: {tone}\n"
            f"Language: {language}\n"
            f"Detail Level: {detail_level}\n"
            f"Length: {length_constraints}\n"
            "Output the final formatted content now."
        )

        return ChannelContextPrompt(
            channel_id=channel_id,
            channel_name=channel_name,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            grounding_rules=grounding_rules
        )

    @classmethod
    def build_context(cls, request: ContextBuildRequest) -> CompiledContextPayload:
        # Step 1: Resolve NLP Analysis
        nlp_data: NLPAnalysisResponse
        if request.nlp_analysis is not None:
            nlp_data = request.nlp_analysis
        else:
            nlp_data = NLPService.analyze(
                NLPAnalysisRequest(
                    content=request.source_text,
                    title=request.title,
                    source_type=request.source_type or "text"
                )
            )

        # Step 2: Resolve Document Title
        source_title = cls.resolve_title(request, nlp_data)

        # Step 3: Audience & Tone Resolution
        audience = request.audience or "General Enterprise & Technical Leaders"
        tone = request.tone or "Professional & Authoritative"
        language = request.language or "English"
        detail_level = request.detail_level or "balanced"

        # Step 4: Build Global System Instructions
        global_instruction = cls.generate_global_system_instruction(
            nlp_data=nlp_data,
            audience=audience,
            tone=tone,
            language=language,
            detail_level=detail_level
        )

        # Step 5: Build Channel Prompts for each requested channel
        target_channels = request.target_channels
        if not target_channels:
            target_channels = ["linkedin", "executive_summary"]

        channel_prompts: Dict[str, ChannelContextPrompt] = {}
        for channel_id in target_channels:
            prompt = cls.generate_channel_prompt(
                channel_id=channel_id,
                source_title=source_title,
                nlp_data=nlp_data,
                audience=audience,
                tone=tone,
                language=language,
                detail_level=detail_level
            )
            channel_prompts[channel_id] = prompt

        return CompiledContextPayload(
            source_title=source_title,
            source_type=request.source_type or "text",
            identified_topic=nlp_data.topic,
            core_facts=nlp_data.key_facts,
            guaranteed_entities=nlp_data.entities,
            salient_keywords=nlp_data.keywords,
            context_summary=nlp_data.summary_context,
            audience_persona=audience,
            tone_guideline=tone,
            language=language,
            detail_level=detail_level,
            global_system_instruction=global_instruction,
            channel_prompts=channel_prompts,
            compiled_at=datetime.now(timezone.utc).isoformat()
        )
