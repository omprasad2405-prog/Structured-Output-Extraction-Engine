# ⚡ GenAI Lab 1: Structured Output Extraction Engine

A lightweight, high-performance Python application and interactive web dashboard that transforms unstructured user feedback into strictly typed, schema-validated JSON analytics using **Pydantic**, **Groq Cloud API** (`llama-3.3-70b-versatile`), and **Streamlit**.

---

## 🎯 The Problem Solved

Standard Large Language Models (LLMs) return unpredictable, conversational prose. Parsing unstructured text in production software pipelines is fragile and error-prone. 

This project enforces a strict **data contract** using Pydantic JSON schemas, guaranteeing:
- **Type Safety**: Native Python types (`int`, `List[str]`, `Literal`) instead of raw strings.
- **Strict Validation**: Categorical constraints (`Positive`, `Neutral`, `Negative`) enforced at inference time.
- **Sub-second Cloud Inference**: Fast extraction via Groq without storing multi-gigabyte models locally.

---

## 🏗️ Architecture & Data Flow

```text
[ Unstructured Text / Streamlit Input ]
                  │
                  ▼
[ Pydantic Schema (schemas.py) ] ──> Generates OpenAPI-compliant JSON Schema
                  │
                  ▼
[ Groq Cloud API (llama-3.3-70b) ] ──> Enforces JSON response matching schema
                  │
                  ▼
[ Pydantic Validation ] ──> Validates & maps raw JSON to typed Python object
                  │
                  ▼
[ Typed Output / Streamlit Dashboard (result.sentiment, result.urgency_score, etc.) ]


🛠️ Project Structure

Plaintext
GenAI_lab1/
├── .env.example        # Environment variable template
├── .gitignore          # Security shield for secrets and virtual environments
├── schemas.py          # Pydantic data schema definition
├── parser.py           # CLI extraction engine logic
├── app.py              # Interactive Streamlit web application
├── requirements.txt    # Project dependencies
└── README.md           # Documentation


🚀 Quickstart Guide
1. Prerequisites
Python 3.10+ installed

Free Groq API key from console.groq.com

2. Installation & Setup
Clone the repository:

Bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
Create and activate a virtual environment:

PowerShell
python -m venv venv
.\venv\Scripts\activate
Install dependencies:

PowerShell
pip install -r requirements.txt


3. Environment Configuration
Create a .env file in the root directory (or copy .env.example):

Code snippet
GROQ_API_KEY=gsk_your_groq_api_key_here

4. Running the Engine
Run via Terminal (CLI Mode):

PowerShell
python parser.py
Run via Web Dashboard (Streamlit UI):

PowerShell
streamlit run app.py
