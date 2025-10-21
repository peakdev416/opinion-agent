# take_forge/opinion_agent/prompt_utiles.py
def build_take_prompt(article: dict) -> str:
    # Keep "utiles" filename for now since you import it that way
    return f"""
        You are a precise extractor of sports opinion takes. Output STRICT JSON.

        Return JSON object with:
        "takes": [
            {{"headline": str (<=160 chars), "explanation": str, "stance": "pro|contra|neutral" or null, "confidence": float 0-1 or null}},
            ... up to 3
        ]

        Article:
        Title: {article['title']}
        Published At: {article.get('published_at')}
        Content:
        {article['content']}
        """
