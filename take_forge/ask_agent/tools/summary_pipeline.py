from take_forge.vector_store.chroma_store import ChromaStore
from take_forge.ask_agent.tools.re_ranker import score_metadata

_chroma = ChromaStore()

def run_summary_pipeline(query: str, filters: dict):
    """Retrieve broad set of takes for summarization and trend analysis."""
    print(f"[SummaryPipeline] Running vector search for: {query}")

    try:
        res = _chroma.collection.query(query_texts=[query], n_results=25)
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        if not docs:
            return {"mode": "summary", "takes": []}

        combined = [{"text": d, "meta": m} for d, m in zip(docs, metas)]
        for item in combined:
            item["score"] = score_metadata(item["meta"], filters)

        # For summary mode: keep *all* ranked takes (don’t filter)
        ranked = sorted(combined, key=lambda x: x["score"], reverse=True)

        print(f"[SummaryPipeline] Returning {len(ranked)} ranked takes.")
        return {"mode": "summary", "takes": ranked}

    except Exception as e:
        print(f"[SummaryPipeline] ⚠️ Error: {e}")
        return {"mode": "summary", "takes": []}
