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
    sys = """You are a precise summarizer. 
Write a clean, factual 120-150 word summary of the article. 
Do NOT include 'Why it matters', bullet points, sources, or reasoning traces. 
Output only the final summary text."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys),
        ("human", "Title: {title}\nURL: {url}\nContext:\n{context}")
    ])
    return prompt | llm | StrOutputParser()

def why_it_matters_chain(llm):
    sys = """Explain in 1-2 plain sentences why this article matters. 
Be direct, no fluff, no reasoning traces. 
Do not include 'Source' or context description."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys),
        ("human", "Title: {title}\nURL: {url}\n\nArticle snippet:\n{context}")
    ])
    return prompt | llm | StrOutputParser()


def tldr_bullets_chain(llm):
    sys = """Summarize the week's niche news into {n} ultra-concise bullets (<=18 words each).
Output ONLY raw bullet points starting with "- ". No intros, no explanations, no titles."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys),
        ("human", "Niche: {niche}\nTop story blurbs:\n{blurbs}")
    ])
    return prompt | llm | StrOutputParser()

def quick_bites_chain(llm):
    sys = """Generate {n} very short one-line news updates in bullet list format.
Each should start with "- " and be <=15 words. 
Output ONLY the bullet list. No intros, no explanations, no titles."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys),
        ("human", "Niche: {niche}\nContext:\n{context}")
    ])
    return prompt | llm | StrOutputParser()
