import json
from take_forge.core.openai_client import client, DEFAULT_MODEL

_client = client

def analyze_query(query: str):
    """
    Analyze a user's question to determine intent (query vs summary) and extract metadata hints.
    The response is structured JSON usable as filters for the retrieval pipelines.
    """
    prompt = f"""
        You are the TakeForge query analyzer.
        Determine if the question is a focused query (specific player, team, stat)
        or a broad summary request (trends, comparisons, or overviews).

        Return JSON in this format:
        {{
        "mode": "query" | "summary",
        "tags": [lowercase keywords],
        "entities": [names],
        "tone": "positive" | "neutral" | "negative" | null,
        "stance": "pro" | "contra" | null,
        "confidence": float
        }}

        Examples:
        - "What do analysts say about Kyrie Irving’s defense?" → query
        - "Summarize opinions on the Celtics’ chemistry this season." → summary
        - "How do experts feel about Zion’s conditioning and injuries?" → query

        User query: {query}
        """
    try:
        resp = _client.chat.completions.create(
            model=DEFAULT_MODEL,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        print(f"[Analyzer] Failed to parse LLM response: {e}")
        return {"mode": "query", "tags": [], "entities": [], "confidence": 0.6}
