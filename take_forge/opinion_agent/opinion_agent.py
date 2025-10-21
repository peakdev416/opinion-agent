# take_forge/opinion_agent/opinion_agent.py
import os, json
from typing import List
from openai import OpenAI
from ..models import Article, OpinionTake, TakeBundle
from .prompt_utiles import build_take_prompt


class OpinionAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def extract_takes(self, article: Article) -> TakeBundle:
        prompt = build_take_prompt(article.model_dump())
        # JSON mode if available; otherwise enforce via system+user and validate
        resp = self.client.chat.completions.create(
            model="gpt-4.1-mini",
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
                model="gpt-4.1-mini",
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
