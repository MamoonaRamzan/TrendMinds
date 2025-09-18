from __future__ import annotations
import json, datetime as dt
from pathlib import Path
import argparse
import re
from tqdm import tqdm
from langchain_community.vectorstores import Chroma
from .utils import clean_llm_output, load_config, ensure_dir, env
from .fetch import fetch_rss_articles, scrape_article_text
from .index import build_vectorstore
from .chains import (
    make_llm,
    retriever_for,
    top_story_selector_chain,
    story_summarizer_chain,
    tldr_bullets_chain,
    quick_bites_chain,
    why_it_matters_chain
)
from .newsletter import render_newsletter, save_outputs, send_email


def run(niche: str):
    cfg = load_config()
    niches = cfg.get("niches", {})

    if niche not in niches:
        raise ValueError(f"❌ Niche '{niche}' not found in config.yml. Available: {list(niches.keys())}")

    rss = niches[niche]
    days = cfg["timespan_days"]
    max_articles = cfg["max_articles"]
    k = cfg["top_k_per_query"]
    chunk_size = cfg["chunk_size"]
    chunk_overlap = cfg["chunk_overlap"]
    temp = cfg["temperature"]
    sections = cfg["sections"]
    outcfg = cfg["output"]
    brand = cfg["branding"]

    ensure_dir("data/raw")
    ensure_dir("data/chroma")

    print(f"📡 Fetching RSS for niche {niche} ({len(rss)} feeds)…")
    arts = fetch_rss_articles(rss, days=days, max_articles=max_articles)
    print(f"Found {len(arts)} candidates.")

    print("🕸️ Scraping articles…")
    for i, a in enumerate(tqdm(arts)):
        arts[i] = scrape_article_text(a)

    # Filter empty
    arts = [a for a in arts if a.text and len(a.text.split()) > 120]
    print(f"📑 Keeping {len(arts)} valid articles.")

    print("📦 Indexing articles…")
    db = build_vectorstore(
        arts, persist_dir=f"data/chroma/{niche.lower()}",
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    # RAG: pick top stories
    llm = make_llm(model=env("GROQ_MODEL", "llama-3.1-8b-instant"), temperature=temp)
    retriever = retriever_for(db, k=k)

    synthetic_query = (
        f"Most important {niche} developments this week; prefer original research, "
        f"major product launches, policy, safety, evals, benchmarks."
    )

    ctx_docs = retriever.invoke(synthetic_query)
    ctx_joined = "\n\n---\n\n".join([
        d.page_content[:1200] + f"\n(URL: {d.metadata.get('url','')}; Title: {d.metadata.get('title','')})"
        for d in ctx_docs
    ])

    selector = top_story_selector_chain(llm)
    sel_raw = selector.invoke({"niche": niche, "context": ctx_joined, "n": sections["top_stories"]})

    # try to parse selector output as JSON (with salvage attempt)
    def safe_parse_json(text):
        try:
            return json.loads(text)
        except Exception:
            m = re.search(r"(\[.*\])", text, flags=re.DOTALL)
            if m:
                try:
                    return json.loads(m.group(1))
                except Exception:
                    return None
            return None

    selected = safe_parse_json(sel_raw)
    if not selected:
        # build a clean fallback list with title+url only
        selected = []
        seen = set()
        for d in ctx_docs:
            u = d.metadata.get("url","")
            if not u or u in seen:
                continue
            seen.add(u)
            selected.append({"title": d.metadata.get("title","(untitled)"), "url": u})
            if len(selected) >= sections["top_stories"]:
                break

    # Summarize + generate 'why' per story (works for normal and fallback)
    summarizer = story_summarizer_chain(llm)
    why_chain = why_it_matters_chain(llm)

    top_stories = []
    for s in selected:
        url = s.get("url","")
        url_docs = db.similarity_search(url, k=4) + db.similarity_search(s.get("title",""), k=3)
        merged = "\n\n".join([d.page_content for d in url_docs][:6])

        # summary
        summary_raw = summarizer.invoke({"title": s["title"], "url": url, "context": merged[:5000]})
        summary = clean_llm_output(summary_raw).strip()

        # why it matters
        try:
            why_raw = why_chain.invoke({"title": s["title"], "url": url, "context": merged[:3000]})
            why = clean_llm_output(why_raw).strip()
        except Exception:
            why = ""  # safe fallback, don't hard-code a generic string

        top_stories.append({
            "title": s["title"],
            "url": url,
            "summary": summary,
            "why": why
        })
  
    # TL;DR bullets
    blurbs = "\n\n".join([ts["summary"][:400] for ts in top_stories])
    tldr_raw = tldr_bullets_chain(llm).invoke({"niche": niche, "blurbs": blurbs, "n": sections["tldr_bullets"]})
    tldr = clean_llm_output(tldr_raw)

    # Quick bites
    qb_ctx_docs = retriever.invoke(f"Short updates in {niche} this week, diverse topics.")
    qb_ctx = "\n\n".join([d.page_content[:500] for d in qb_ctx_docs])
    quick_bites_raw = quick_bites_chain(llm).invoke({"niche": niche, "context": qb_ctx, "n": sections["quick_bites"]})
    quick_bites = clean_llm_output(quick_bites_raw) 

    # Further reading: broaden scope
    further = []
    seen_urls = {ts["url"] for ts in top_stories if ts["url"]}

    # Use all retrieved docs + a few randoms
    candidates = ctx_docs[:20]  # top 20 retrieved docs
    for d in candidates:
        u = d.metadata.get("url", "")
        t = d.metadata.get("title", "").strip()
        if u and u not in seen_urls:
            further.append({
                "title": t if t else "(untitled)",
                "url": u,
                "note": "Worth a look"
            })
            seen_urls.add(u)
        if len(further) >= sections["further_reading"]:
            break

    # ✅ Fallback if still empty
    if not further:
        further.append({
            "title": "No extra links this week — you’re fully caught up! 🚀",
            "url": "",
            "note": ""
        })

    payload = {
        "title": brand["title"],
        "subtitle": brand["subtitle"],
        "author": brand["author"],
        "week": dt.date.today().isoformat(),
        "tldr": tldr.strip(),
        "stories": top_stories,
        "top_n": len(top_stories),
        "quick_bites": quick_bites.strip(),
        "further": further,
    }

    md = render_newsletter(payload)
    md_file = f"{niche.lower()}_{outcfg['filename_md']}"
    html_file = f"{niche.lower()}_{outcfg['filename_html']}"
    md_path, html_path = save_outputs(md, out_dir=outcfg["folder"], file_md=md_file, file_html=html_file)
    print(f"✅ Newsletter written for {niche}:\n- {md_path}\n- {html_path}")

    send_email(html_path, cfg, niche)
    print(f"📧 Email sent for {niche}!")

    # Save top stories in JSON for frontend
    stories_data = {
        "stories": top_stories  # already contains title, url, summary, why
    }

    # Create output directory if it doesn't exist
    headlines_file = Path("output/latest.json")
    headlines_file.parent.mkdir(parents=True, exist_ok=True)

    # Load existing file to keep other niches
    existing = {}
    if headlines_file.exists():
        try:
            # Try reading with UTF-8 first, then fallback encodings
            content = None
            for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
                try:
                    content = headlines_file.read_text(encoding=encoding)
                    print(f"✅ Read existing file with encoding: {encoding}")
                    break
                except UnicodeDecodeError:
                    continue
        
            if content:
                existing = json.loads(content)
            else:
                print("⚠️ Could not read existing file, starting fresh")
                existing = {}
            
        except json.JSONDecodeError as e:
            print(f"⚠️ Existing JSON file corrupted: {e}")
            existing = {}

    # Update with new niche data
    existing[niche] = stories_data

    # Write with explicit UTF-8 encoding
    with open(headlines_file, 'w', encoding='utf-8', newline='') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False, sort_keys=True)

    print(f"📰 Saved structured stories for {niche} in output/latest.json")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--niche", type=str, required=True, help="Newsletter niche (AI, Crypto, Climate, etc.)")
    parser.add_argument("--receivers", type=str, help="Comma-separated list of emails")
    args = parser.parse_args()

    cfg = load_config()

    # Override config values dynamically
    cfg["niche"] = args.niche
    if args.receivers:
        cfg.setdefault("email", {})["receivers"] = args.receivers.split(",")

    run(cfg["niche"])
