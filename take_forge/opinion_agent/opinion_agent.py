# take_forge/opinion_agent/opinion_agent.py
import os, json
from typing import List
from take_forge.core.openai_client import client, DEFAULT_MODEL
from ..models import Article, OpinionTake, TakeBundle
from .prompt_utiles import build_take_prompt


class OpinionAgent:
    def __init__(self):
        self.client = client

    def extract_takes(self, article: Article) -> TakeBundle:
        prompt = build_take_prompt(article.model_dump())
        # JSON mode if available; otherwise enforce via system+user and validate
        resp = self.client.chat.completions.create(
            model=DEFAULT_MODEL,
            temperature=0.4,
            messages=[{"role": "user", "content": prompt}],
            response_format={
                "type": "json_object"
            },  # returns a JSON object; see prompt below
        )

        raw = resp.choices[0].message.content or "{}"
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # one retry with a stricter instruction helps a lot
            retry = self.client.chat.completions.create(
                model=DEFAULT_MODEL,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": prompt + "\nReturn VALID minified JSON only.",
                    }
                ],
                response_format={"type": "json_object"},
            )
            data = json.loads(retry.choices[0].message.content or "{}")

        # Expect shape: {"takes": [{headline, explanation, ...}, ...]}
        takes = [OpinionTake(**t) for t in data.get("takes", [])][:3]
        return TakeBundle(article_id=article.id, takes=takes)

    def generate_metadata(self, bundle: TakeBundle) -> dict:
        """
        Generate descriptive metadata for a bundle of takes.
        Returns JSON with tags, tone, and entities.
        """
        joined = "\n".join(
            f"{t.headline}. {t.explanation}" for t in bundle.takes
        )

        prompt = f"""
        Analyze these opinion takes and return concise metadata.

        Return JSON only with:
        - tags: 3–5 short lowercase keywords
        - tone: one of ['positive', 'neutral', 'negative']
        - entities: list of relevant people, teams, or organizations

        Example:
        {{
          "tags": ["nba", "mavericks", "injury"],
          "tone": "positive",
          "entities": ["Kyrie Irving", "Dallas Mavericks"]
        }}

        Takes:
        {joined}
        """

        try:
            resp = self.client.chat.completions.create(
                model=DEFAULT_MODEL,
                temperature=0,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
            )
            return json.loads(resp.choices[0].message.content or "{}")
        except Exception as e:
            print("Metadata generation failed:", e)
            # fallback heuristic
            return {
                "tags": ["basketball", "analysis"],
                "tone": "neutral",
                "entities": []
            }