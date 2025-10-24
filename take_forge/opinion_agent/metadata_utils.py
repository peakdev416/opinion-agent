from typing import Dict, Any

CANON_MAP = {
    "coach mazzulla": "joe mazzulla",
    "coach popovich": "gregg popovich",
}

def normalize_metadata(md: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize tags, tone, and entity names from LLM metadata output."""

    # --- Tags ---
    tags = md.get("tags") or []
    if not isinstance(tags, list):
        tags = [str(tags)]
    tags = [t.strip().lower() for t in tags if isinstance(t, str) and t.strip()]
    tags = sorted(set(tags))[:5]

    # --- Tone ---
    tone = (md.get("tone") or "neutral").strip().lower()
    if tone not in {"positive", "neutral", "negative"}:
        tone = "neutral"

    # --- Entities ---
    entities = md.get("entities") or []
    if not isinstance(entities, list):
        entities = [str(entities)]
    normalized_entities = []
    for e in entities:
        if not isinstance(e, str):
            continue
        key = e.strip().lower()
        if key and key not in {"n/a", "-", "none"}:
            canonical = CANON_MAP.get(key, key)  # use lowercased canonical
            normalized_entities.append(canonical)

    return {
        **md,
        "tags": tags,
        "tone": tone,
        "entities": sorted(set(normalized_entities))[:10],  # limit & dedupe
    }

def flatten_metadata_for_chroma(md: dict) -> dict:
    """Convert lists in metadata to comma-separated strings for Chroma."""
    result = {}
    for k, v in md.items():
        if isinstance(v, list):
            result[k] = ", ".join(str(x) for x in v)
        else:
            result[k] = v
    return result
