from backend.app.modules.nlp.schemas import NLPAnalysisResponse
from backend.app.modules.generation.schemas import VideoScene, VideoScriptArtefact


def structure_video(raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> VideoScriptArtefact:
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
