from __future__ import annotations
import time
from dataclasses import dataclass
from typing import List, Dict
import feedparser, trafilatura
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime, timezone, timedelta
from .utils import ensure_dir, sha1

@dataclass
class Article:
    url: str
    title: str
    published: datetime | None
    source: str
    text: str | None = None

def _to_dt(entry):
    try:
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        if hasattr(entry, "updated_parsed") and entry.updated_parsed:
            return datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
    except Exception:
        pass
    return None

def fetch_rss_articles(rss_urls: List[str], days: int, max_articles: int) -> List[Article]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    pool: List[Article] = []
    for url in rss_urls:
        feed = feedparser.parse(url)
        for e in feed.entries:
            dt_e = _to_dt(e)
            if dt_e and dt_e < cutoff:
                continue
            pool.append(Article(
                url=e.link,
                title=e.title if hasattr(e, "title") else e.link,
                published=dt_e,
                source=feed.feed.title if hasattr(feed, "feed") and hasattr(feed.feed, "title") else url
            ))
    # uniqueness by URL
    uniq: Dict[str, Article] = {}
    for a in pool:
        uniq[a.url] = a
        if len(uniq) >= max_articles: break
    return list(uniq.values())

def scrape_article_text(art: Article, cache_dir: str = "data/raw") -> Article:
    ensure_dir(cache_dir)
    key = sha1(art.url)
    html_path = Path(cache_dir) / f"{key}.html"
    txt_path  = Path(cache_dir) / f"{key}.txt"

    if txt_path.exists():
        art.text = txt_path.read_text(encoding="utf-8", errors="ignore")
        return art

    downloaded = trafilatura.fetch_url(art.url, no_ssl=True)
    time.sleep(0.5)  # polite delay
    if downloaded:
        html_path.write_text(downloaded, encoding="utf-8", errors="ignore")
        extracted = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
        if not extracted:
            # very basic fallback: strip tags
            soup = BeautifulSoup(downloaded, "html.parser")
            extracted = soup.get_text(separator="\n")
        if extracted:
            txt_path.write_text(extracted, encoding="utf-8", errors="ignore")
            art.text = extracted
    return art
