from take_forge.vector_store.chroma_store import ChromaStore
from take_forge.ask_agent.tools.re_ranker import score_metadata

_chroma = ChromaStore()

def run_query_pipeline(query: str, filters: dict):
    """Retrieve a small number of focused takes for question answering."""
    print(f"[QueryPipeline] Running vector search for: {query}")

    try:
        res = _chroma.collection.query(query_texts=[query], n_results=10)
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        if not docs:
            return {"mode": "query", "takes": []}

        combined = [{"text": d, "meta": m} for d, m in zip(docs, metas)]
        for item in combined:
            item["score"] = score_metadata(item["meta"], filters)

        # Only keep relevant ones (≥ 0.4), fallback to top 3
        filtered = [t for t in combined if t["score"] >= 0.4]
        if not filtered:
            filtered = sorted(combined, key=lambda x: x["score"], reverse=True)[:3]

        print(f"[QueryPipeline] Returning {len(filtered)} filtered takes.")
        return {"mode": "query", "takes": filtered}

    except Exception as e:
        print(f"[QueryPipeline] ⚠️ Error: {e}")
        return {"mode": "query", "takes": []}
