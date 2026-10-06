import re
from typing import List
from backend.app.modules.nlp.schemas import NLPAnalysisResponse
from backend.app.modules.generation.schemas import TweetItem, TwitterArtefact


def structure_twitter(raw_text: str, nlp_data: NLPAnalysisResponse, title: str) -> TwitterArtefact:
    # Check if output is split by --- or 1/N
    parts = re.split(r"\n\s*---\s*\n|\n\s*(?=\d+/\d+)", raw_text)
    tweets: List[TweetItem] = []

    if len(parts) > 1:
        for part in parts:
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
