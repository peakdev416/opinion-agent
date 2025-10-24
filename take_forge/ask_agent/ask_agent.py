import json
from take_forge.core.openai_client import client
from take_forge.ask_agent.query_analyzer import analyze_query
from take_forge.ask_agent.tools.query_pipeline import run_query_pipeline
from take_forge.ask_agent.tools.summary_pipeline import run_summary_pipeline


class AskAgent:
    """
    Manual reasoning agent (AgentKit-compatible architecture, no dependency).
    - Uses OpenAI LLM to analyze query intent.
    - Chooses query or summary pipeline dynamically.
    - Optionally summarizes retrieved results using LLM.
    """

    def __init__(self, summary_model: str = "gpt-4.1-mini"):
        self.model = summary_model

    def ask(self, query: str):
        """
        Main entrypoint for answering or summarizing user questions.
        Delegates retrieval and filtering to the correct pipeline.
        """
        # Step 1: Analyze query → determine mode + filters
        analysis = analyze_query(query)
        mode = analysis.get("mode", "query")
        print(f"[AskAgent] Mode detected: {mode}")

        # Step 2: Run appropriate pipeline
        if mode == "summary":
            result = run_summary_pipeline(query, analysis)
        else:
            result = run_query_pipeline(query, analysis)

        takes = result.get("takes", [])
        if not takes:
            return {
                "query": query,
                "mode": mode,
                "filters": analysis,
                "answer": "No relevant takes found.",
                "takes": [],
            }

        # Step 3: Build structured LLM context (no filtering here)
        context_blocks = []
        for t in takes:
            score = t.get("score", 0)
            text = t.get("text", "").strip()
            meta = t.get("meta", {}) or {}
            tags = meta.get("tags", "")
            published = meta.get("published_at", "unknown date")
            if isinstance(tags, list):
                tags = ", ".join(tags)
            context_blocks.append(
                f"[relevance_score={score:.2f}] [tags={tags}] [published_at={published}] {text}"
            )

        text_context = "\n\n".join(context_blocks)
        print(f"[AskAgent] Prepared {len(takes)} takes for LLM context.")

        # Step 4: Generate mode-specific prompt
        try:
            if mode == "summary":
                prompt = f"""
                    You are **TakeForge**, an intelligent opinion summarizer.
                    Your task is to synthesize the main viewpoints, tones, and trends from sports opinion data.

                    **User query:**
                    {query}

                    **Relevant takes (each includes a relevance_score, tags, and publication date):**
                    {text_context[:4000]}

                    Write a neutral, well-structured summary in 3–6 sentences:
                    - Highlight recurring ideas, tone differences, and overall sentiment.
                    - Consider publication dates to reflect any recent trends or shifts.
                    - Avoid repetition or speculation.
                    Return a concise, human-readable overview suitable for a sports analyst briefing.
                    """
            else:  # query mode
                prompt = f"""
                    You are **TakeForge**, an AI analyst that answers user questions about sports opinions.

                    **User query:**
                    {query}

                    **Relevant takes (each includes a relevance_score, tags, and publication date):**
                    {text_context[:4000]}

                    Answer the question clearly and factually in 2–5 sentences:
                    - Use only the information contained in the takes.
                    - Reflect consensus or mention differing opinions if they exist.
                    - Weigh more recent takes slightly higher if they indicate a trend.
                    Be concise, neutral, and focused on evidence from the provided opinions.
                    """

            resp = client.chat.completions.create(
                model=self.model,
                temperature=0.5,
                messages=[{"role": "user", "content": prompt}],
            )
            answer = resp.choices[0].message.content.strip()

        except Exception as e:
            print(f"[AskAgent] Failed to generate answer: {e}")
            answer = None

        # Step 5: Return structured response
        return {
            "query": query,
            "mode": mode,
            "filters": analysis,
            "answer": answer,
            "takes": takes,
            "text_context": text_context,
        }

