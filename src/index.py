from __future__ import annotations
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def build_vectorstore(articles, persist_dir="data/chroma", chunk_size=1000, chunk_overlap=150):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs: List[Document] = []
    for a in articles:
        if not a.text: 
            continue
        metadata = {
            "source": a.source,
            "url": a.url,
            "title": a.title,
        }
        for chunk in splitter.split_text(a.text):
            docs.append(Document(page_content=chunk, metadata=metadata))

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persist_dir)
    db.persist()
    return db
