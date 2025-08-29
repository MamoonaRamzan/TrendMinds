import streamlit as st
from src.run import run

st.set_page_config(page_title="AI Newsletter Generator", page_icon="🗞️", layout="centered")
st.title("🗞️ AI Newsletter Generator (RAG + Groq)")

st.write("Generates a weekly niche newsletter using LangChain, Chroma, and Groq.")
if st.button("Build newsletter now"):
    with st.spinner("Running end-to-end…"):
        run()
    st.success("Done! Check the /output folder for latest.md and latest.html")
