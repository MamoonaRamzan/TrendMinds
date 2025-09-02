from __future__ import annotations
import json, datetime as dt
from pathlib import Path
import argparse
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
    llm = make_llm(model=env("GROQ_MODEL", "llama-3.1-70b-versatile"), temperature=temp)
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
    try:
        selected = json.loads(sel_raw)
    except Exception:
        selected = []
        seen = set()
        for d in ctx_docs:
            u = d.metadata.get("url", "")
            if u in seen:
                continue
            seen.add(u)
            selected.append({
                "title": d.metadata.get("title", "(untitled)"),
                "url": u,
                "why_it_matters": "High-signal development this week."
            })
            if len(selected) >= sections["top_stories"]:
                break

    summarizer = story_summarizer_chain(llm)
    top_stories = []
    for s in selected:
        url = s.get("url", "")
        url_docs = db.similarity_search(url, k=4) + db.similarity_search(s.get("title", ""), k=3)
        merged = "\n\n".join([d.page_content for d in url_docs][:6])
        summary_raw = summarizer.invoke({"title": s["title"], "url": url, "context": merged[:5000]})
        summary = clean_llm_output(summary_raw)
        top_stories.append({
            "title": s["title"],
            "url": url,
            "summary": summary.strip(),
            "why": s.get("why_it_matters", "")
        })

    # TL;DR bullets
    blurbs = "\n\n".join([ts["summary"][:400] for ts in top_stories])
    tldr_raw = tldr_bullets_chain(llm).invoke({"niche": niche, "blurbs": blurbs, "n": sections["tldr_bullets"]})
    tldr = clean_llm_output(tldr_raw)

    # Quick bites
    qb_ctx_docs = retriever.invoke(f"Short updates in {niche} this week, diverse topics.")
    qb_ctx = "\n\n".join([d.page_content[:500] for d in qb_ctx_docs])
    quick_bites = quick_bites_chain(llm).invoke({"niche": niche, "context": qb_ctx, "n": sections["quick_bites"]})

    # Further reading
    further = []
    seen_urls = {ts["url"] for ts in top_stories if ts["url"]}
    for d in ctx_docs:
        u = d.metadata.get("url", "")
        if u and u not in seen_urls:
            further.append({"title": d.metadata.get("title", "(untitled)"), "url": u, "note": "Worth a look"})
            if len(further) >= sections["further_reading"]:
                break

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



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--niche", type=str, default="AI", help="Choose newsletter niche (AI, Crypto, Climate, etc.)")
    args = parser.parse_args()
    run(args.niche)
