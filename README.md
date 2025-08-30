# 📰 AI Newsletter Generator

<div align="center">

![LangChain](https://img.shields.io/badge/LangChain-GenAI-blue?style=for-the-badge&logo=chainlink&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM-red?style=for-the-badge&logo=groq&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776ab?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-RAG-green?style=for-the-badge&logo=databricks&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI/CD-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

**Automated AI-powered weekly newsletter with RAG, LangChain & Groq.  
Generates Markdown + HTML, with optional Streamlit UI & email automation.**

[🚀 Getting Started](#-getting-started) • [📖 Usage](#-usage) • [⚡ Automation](#-automation-with-github-actions) • [🤝 Contributing](#-contributing)

</div>

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Automation with GitHub Actions](#-automation-with-github-actions)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview
**AI Newsletter Generator** is a generative AI project that automatically curates the latest news and research from AI blogs, tech sites, and academic papers into a professional weekly newsletter.  

It demonstrates **RAG (Retrieval-Augmented Generation)**, **LLM summarization**, and **end-to-end automation** skills — perfect for showcasing GenAI expertise.

---

## ✨ Features
- 🔎 **Automated Retrieval** – Fetches latest articles from curated RSS feeds  
- 🧠 **RAG + Summarization** – Uses LangChain + Groq LLM to summarize with context  
- 📰 **Polished Output** – Generates both Markdown (`.md`) and styled HTML (`.html`)  
- 📧 **Email Automation** – Sends the newsletter to configured recipients  
- 🎨 **Streamlit Preview** – Optional UI for browsing top stories interactively  
- ⚡ **GitHub Actions Automation** – Runs weekly on schedule  

---

## 🛠️ Tech Stack
- **Language**: ![Python](https://img.shields.io/badge/Python-3.11-3776ab?logo=python&logoColor=white)  
- **Frameworks**: ![LangChain](https://img.shields.io/badge/LangChain-GenAI-blue), ![Streamlit](https://img.shields.io/badge/Streamlit-UI-ff4b4b)  
- **LLM**: ![Groq](https://img.shields.io/badge/Groq-LLM-red)  
- **Database**: ![ChromaDB](https://img.shields.io/badge/ChromaDB-RAG-green)  
- **Automation**: ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI/CD-2088FF)  

---

## 📂 Project Structure

```
genai-newsletter/
├── src/
│ ├── fetch.py # Fetch RSS feeds & scrape content
│ ├── index.py # Chunking, embeddings, ChromaDB
│ ├── chains.py # LangChain + Groq summarization chains
│ ├── newsletter.py # Render & send newsletters
│ └── run.py # Main pipeline
├── output/ # Generated newsletters (md + html)
├── app_streamlit.py # Optional Streamlit UI
├── config.yml # Config: feeds, branding, output
└── .github/workflows/ # GitHub Actions automation
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/MamoonaRamzan/AI-Newsletter.git
cd AI-Newsletter
```
### 2. Install dependencies
```bash
uv venv
pip install -r requirements.txt
```
### 3. Configure API keys & email
```bash
GROQ_API_KEY=your_groq_key
SENDER_EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
RECEIVER_EMAILS=receiver1@example.com,receiver2@example.com
```

---
## 📖 Usage
### Run the pipeline locally
```bash
python -m src.run
```
Saves newsletter → output/latest.md & output/latest.html

Sends email automatically (if enabled in config)
### Run Streamlit UI
```bash
streamlit run app_streamlit.py
```
---

## ⚡ Automation with GitHub Actions
This project includes a workflow (.github/workflows/weekly.yml) that:

- Runs weekly (Monday 07:00 UTC)

- Fetches articles, generates newsletter

- Sends emails & uploads output artifacts

👉 Set secrets in repo → Settings → Secrets → Actions:

- GROQ_API_KEY

- SENDER_EMAIL

- EMAIL_PASSWORD

- RECEIVER_EMAILS

---

## 🔮 Future Improvements
- Multi-niche newsletter support (AI, Climate, Crypto, etc.)

- Integration with Substack/Mailchimp APIs

- User dashboard for managing subscribers

- Database for long-term newsletter archives

## 🤝 Contributing

Contributions are welcome!

- Fork repo

- Create a feature branch

- Make changes & test

- Submit PR

## 📄 License

This project is licensed under the MIT License.

---
<div align="center">

⭐ **If you find this project helpful, please star the repo!**  

[![GitHub stars](https://img.shields.io/github/stars/MamoonaRamzan/AI-Newsletter?style=social)](https://github.com/MamoonaRamzan/AI-Newsletter/stargazers)  
[![GitHub forks](https://img.shields.io/github/forks/MamoonaRamzan/AI-Newsletter?style=social)](https://github.com/MamoonaRamzan/AI-Newsletter/forks)

<br/>

Made with ❤️ by the **Mamoona**

</div>
