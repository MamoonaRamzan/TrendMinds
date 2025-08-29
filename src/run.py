from __future__ import annotations
import json, datetime as dt, random
from pathlib import Path
from tqdm import tqdm
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document
from .utils import clean_llm_output
from .newsletter import render_newsletter, save_outputs, send_email

from .utils import load_config, ensure_dir, env, today_iso
from .fetch import fetch_rss_articles, scrape_article_text
from .index import build_vectorstore
from .chains import make_llm, retriever_for, top_story_selector_chain, story_summarizer_chain, tldr_bullets_chain, quick_bites_chain
from .newsletter import render_newsletter, save_outputs

def run():
    cfg = load_config()
    niche = cfg["niche"]
    rss = cfg["rss_feeds"]
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

    print(f"Fetching RSS ({len(rss)} feeds)…")
    arts = fetch_rss_articles(rss, days=days, max_articles=max_articles)
    print(f"Found {len(arts)} candidates.")

    print("Scraping…")
    for i, a in enumerate(tqdm(arts)):
        arts[i] = scrape_article_text(a)

    # Filter empty
    arts = [a for a in arts if a.text and len(a.text.split()) > 120]

    print(f"Indexing {len(arts)} articles…")
    db = build_vectorstore(arts, persist_dir="data/chroma", chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    # RAG: pick top stories
    llm = make_llm(model=env("GROQ_MODEL", "llama-3.1-70b-versatile"), temperature=temp)
    retriever = retriever_for(db, k=k)

    # Build a synthetic query that represents the week
    synthetic_query = f"Most important {niche} developments this week; prefer original research, major product launches, policy, safety, evals, benchmarks."

    ctx_docs = retriever.invoke(synthetic_query)
    ctx_joined = "\n\n---\n\n".join([d.page_content[:1200] + f"\n(URL: {d.metadata.get('url','')}; Title: {d.metadata.get('title','')})" for d in ctx_docs])

    selector = top_story_selector_chain(llm)
    sel_raw = selector.invoke({"niche": niche, "context": ctx_joined, "n": sections["top_stories"]})
    try:
        selected = json.loads(sel_raw)
    except Exception:
        # extremely robust fallback: take top-k doc titles/urls
        selected = []
        seen = set()
        for d in ctx_docs:
            u = d.metadata.get("url","")
            if u in seen: continue
            seen.add(u)
            selected.append({"title": d.metadata.get("title","(untitled)"), "url": u, "why_it_matters": "High-signal development this week."})
            if len(selected) >= sections["top_stories"]: break

    # Summarize each story with RAG
    summarizer = story_summarizer_chain(llm)
    top_stories = []
    for s in selected:
        url = s.get("url","")
        # pull more specific context per URL
        url_docs = db.similarity_search(url, k=4) + db.similarity_search(s.get("title",""), k=3)
        merged = "\n\n".join([d.page_content for d in url_docs][:6])
        summary_raw = summarizer.invoke({"title": s["title"], "url": url, "context": merged[:5000]})
        summary = clean_llm_output(summary_raw)
        top_stories.append({
            "title": s["title"],
            "url": url,
            "summary": summary.strip(),
            "why": s.get("why_it_matters","")
        })

    # TL;DR bullets
    blurbs = "\n\n".join([ts["summary"][:400] for ts in top_stories])
    tldr_raw = tldr_bullets_chain(llm).invoke({"niche": niche, "blurbs": blurbs, "n": sections["tldr_bullets"]})
    tldr = clean_llm_output(tldr_raw)


    # Quick bites: sample a bunch of chunks and compress
    qb_ctx_docs = retriever.invoke(f"Short updates in {niche} this week, diverse topics.")
    qb_ctx = "\n\n".join([d.page_content[:500] for d in qb_ctx_docs])
    quick_bites = quick_bites_chain(llm).invoke({"niche": niche, "context": qb_ctx, "n": sections["quick_bites"]})

    # Further reading: pull additional URLs
    further = []
    seen_urls = {ts["url"] for ts in top_stories if ts["url"]}
    for d in ctx_docs:
        u = d.metadata.get("url","")
        if u and u not in seen_urls:
            further.append({"title": d.metadata.get("title","(untitled)"), "url": u, "note": "Worth a look"})
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
    md_path, html_path = save_outputs(
        md, out_dir=outcfg["folder"], file_md=outcfg["filename_md"], file_html=outcfg["filename_html"]
    )
    print(f"✅ Newsletter written:\n- {md_path}\n- {html_path}")

    send_email(html_path, cfg)
    print("Email send sucessfully !")

if __name__ == "__main__":
    run()
