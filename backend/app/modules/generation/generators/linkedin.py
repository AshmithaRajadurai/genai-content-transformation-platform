import re
from backend.app.modules.nlp.schemas import NLPAnalysisResponse
from backend.app.modules.generation.schemas import LinkedInArtefact


def structure_linkedin(raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> LinkedInArtefact:
    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
    heading = title
    hook = lines[0] if lines else f"Critical update on {nlp_data.topic}."

    # Extract hashtags
    hashtags = re.findall(r"#\w+", raw_text)
    if not hashtags:
        hashtags = [f"#{re.sub(r'[^a-zA-Z0-9]', '', kw.title())}" for kw in nlp_data.keywords[:4] if kw]

    # Extract takeaways (look for bullet lines)
    takeaways = [
        re.sub(r"^[🔹•\-\*\d\.]+\s*", "", line)
        for line in lines
        if any(line.startswith(p) for p in ["🔹", "•", "-", "*"]) or "takeaway" in line.lower()
    ]
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
