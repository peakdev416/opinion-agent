# take_forge/api/deps.py
import threading, time, hashlib, traceback
from typing import Optional
from take_forge.opinion_agent.opinion_agent import OpinionAgent
from take_forge.scraper_service.scraper import Scraper
from take_forge.models import Article

_opinion_agent: Optional[OpinionAgent] = None
_scraper: Optional[Scraper] = None
_stop = False


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# naive in-memory "done" set for demo
_done = set()


def _take_takes():
    backoff = 1
    while not _stop:
        try:
            art_dict = _scraper.next_article()
            if not art_dict:
                time.sleep(5)
                continue

            article = Article(**art_dict)
            key = (article.id, _content_hash(article.content))
            if key in _done:
                time.sleep(1)
                continue

            bundle = _opinion_agent.extract_takes(article)
            print(f"[TakeForge] {article.id}: {len(bundle.takes)} takes")
            for t in bundle.takes:
                print(f" - {t.headline} :: {t.explanation[:80]}")

            _done.add(key)
            backoff = 1  # reset
            time.sleep(2)  # small idle between items

        except Exception as e:
            traceback.print_exc()
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)  # capped backoff


def initialize():
    global _opinion_agent, _scraper
    _opinion_agent = OpinionAgent()
    _scraper = Scraper()
    t = threading.Thread(target=_take_takes, daemon=True)
    t.start()
