# take_forge/api/deps.py
import threading, time, hashlib, traceback
from take_forge.opinion_agent import OpinionAgent, normalize_metadata, flatten_metadata_for_chroma
from take_forge.scraper_service import Scraper
from take_forge.models import Article
from take_forge.vector_store import ChromaStore, make_take_id

_opinion_agent: OpinionAgent | None = None
_scraper: Scraper | None = None
_chroma: ChromaStore | None = None
_stop = False
_done = set()

def _content_hash(text: str) -> str:
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def _take_takes():
    while not _stop:
        try:
            art_dict = _scraper.next_article()
            if not art_dict:
                time.sleep(2); continue

            article = Article(**art_dict)
            key = (article.id, _content_hash(article.content))
            if key in _done:
                time.sleep(1); continue

            bundle = _opinion_agent.extract_takes(article)
            meta = _opinion_agent.generate_metadata(bundle)

            # 🔹 Common article-level context
            base_info = {
                "article_id": article.id,
                "article_title": article.title,
                "source_url": article.source_url,
                "published_at": article.published_at,
                "scraped_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

            for i, take in enumerate(bundle.takes, start=1):
                text = f"{take.headline}. {take.explanation}"
                metadata = {
                    **base_info,  # merge shared info
                    "tags": meta.get("tags", []),
                    "tone": meta.get("tone"),
                    "entities": meta.get("entities", []),
                    "stance": take.stance,
                    "confidence": take.confidence,
                }
                metadata = normalize_metadata(metadata)
                metadata = flatten_metadata_for_chroma(metadata)

                # Generate a stable vector ID
                print(f"metadata: {metadata}")
                vector_id = make_take_id(metadata["source_url"], i)

                _chroma.add_take(vector_id, take.headline, text, metadata)

            print(f"[TakeForge] Stored {len(bundle.takes)} takes for {article.id}")
            _done.add(key)
            time.sleep(2)

        except Exception:
            traceback.print_exc()
            time.sleep(5)

def initialize():
    global _opinion_agent, _scraper, _chroma
    _opinion_agent = OpinionAgent()
    _scraper = Scraper()
    _chroma = ChromaStore()
    t = threading.Thread(target=_take_takes, daemon=True)
    t.start()
