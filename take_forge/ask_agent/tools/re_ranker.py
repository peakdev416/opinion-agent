def score_metadata(meta: dict, filters: dict) -> float:
    """Compute metadata-based relevance score (shared by query & summary pipelines)."""
    score = 0.0

    tags_str = (meta.get("tags") or "").lower()
    entities_str = (meta.get("entities") or "").lower()

    query_tags = [t.lower() for t in filters.get("tags", [])]
    query_ents = [e.lower() for e in filters.get("entities", [])]

    # Keyword overlap
    for tag in query_tags:
        if tag in tags_str:
            score += 1.0
    for ent in query_ents:
        if ent in entities_str:
            score += 1.5

    # Tone & stance weighting
    tone = filters.get("tone")
    if tone and tone == meta.get("tone"):
        score += 0.5
    stance = filters.get("stance")
    if stance and stance == meta.get("stance"):
        score += 0.5

    return score
