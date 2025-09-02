from __future__ import annotations
from typing import List, Dict
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

def make_llm(model:str, temperature:float=0.2):
    return ChatGroq(model_name=model, temperature=temperature)

def retriever_for(db, k:int=6):
    return db.as_retriever(search_kwargs={"k": k})

# Select top stories (titles + URLs) given niche and recency
def top_story_selector_chain(llm):
    sys = """You are an expert curator. Given retrieved article snippets about a niche, select the most newsworthy,
non-duplicative items. Prioritize original reports, technical depth, and broad impact. Return a JSON list with
fields: title, url, why_it_matters (1-2 lines). Limit to {n} items."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys),
        ("human", "Niche: {niche}\nRetrieved context:\n{context}\nReturn JSON list of {n} items.")
    ])
    return prompt | llm | StrOutputParser()

def story_summarizer_chain(llm):
    sys = """You are a precise technical summarizer. Using ONLY the provided context (do not fabricate),
write a 120-180 word summary with a factual tone, a 'Why it matters' 1-liner,
and 3 bullet key points. Add a 'Source:' line with the canonical URL.,Do not describe your thought process, Do not explain what you are doing, Do not mention "context", "I need to", or "the user",Output only the final clean summary."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys),
        ("human", "Title: {title}\nURL: {url}\nContext:\n{context}")
    ])
    return prompt | llm | StrOutputParser()

def tldr_bullets_chain(llm):
    sys = """Summarize the week's niche news into {n} ultra-concise bullets (<=18 words each), no fluff, high-signal."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys),
        ("human", "Niche: {niche}\nTop story blurbs:\n{blurbs}")
    ])
    return prompt | llm | StrOutputParser()

def quick_bites_chain(llm):
    sys = """Create {n} one-line 'quick bites'—tiny updates with a noun-verb-object structure.
No marketing language, keep it crisp. Return as markdown bullet list."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys),
        ("human", "Niche: {niche}\nContext snippets:\n{context}")
    ])
    return prompt | llm | StrOutputParser()
