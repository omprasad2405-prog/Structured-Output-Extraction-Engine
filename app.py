import os
from pathlib import Path
import streamlit as st
from groq import Groq
from schemas import EmotionalFeedback

# Page Configuration
st.set_page_config(
    page_title="Feedback Emotion Analyzer",
    page_icon="⚡",
    layout="centered"
)

# 1. Retrieve API Key (Supports Streamlit Cloud Secrets and local .env)
api_key = None
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).resolve().parent / ".env"
        load_dotenv(dotenv_path=env_path, override=True)
        api_key = os.getenv("GROQ_API_KEY")
    except ImportError:
        pass

st.title("⚡ Structured Feedback Analyzer")
st.caption("Extract typed JSON schema analytics from raw text using Groq & Pydantic")

if not api_key:
    st.error("❌ GROQ_API_KEY not found! Configure it in Streamlit Secrets or .env file.")
    st.stop()

# 2. Initialize Groq Client
client = Groq(api_key=api_key.strip())

def analyze_user_text(text_input: str) -> EmotionalFeedback:
    schema_json = EmotionalFeedback.model_json_schema()
    
    # Use the active model available on your Groq tier
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an empathetic feedback analyst. "
                    "Analyze the text and return JSON matching this EXACT JSON Schema:\n"
                    f"{schema_json}"
                )
            },
            {"role": "user", "content": text_input}
        ],
        response_format={"type": "json_object"},
        temperature=0.2
    )
    raw_json = completion.choices[0].message.content
    return EmotionalFeedback.model_validate_json(raw_json)

# User Interface
user_text = st.text_area(
    "Enter customer/user feedback text:",
    height=120,
    placeholder="e.g., I've been waiting for my order updates for three days without any email notification..."
)

if st.button("Analyze Feedback", type="primary"):
    if not user_text.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing text with Groq AI..."):
            try:
                result = analyze_user_text(user_text)

                st.success("Analysis Complete!")
                st.divider()

                # Metric Cards
                col1, col2, col3 = st.columns(3)
                col1.metric("Sentiment", result.sentiment)
                col2.metric("Primary Emotion", result.primary_emotion)
                col3.metric("Urgency Score", f"{result.urgency_score} / 5")

                # Key Points
                st.subheader("📌 Key Points Identified")
                for point in result.key_points:
                    st.markdown(f"- {point}")

                # Suggested Action
                st.subheader("💡 Suggested Action")
                st.info(result.suggested_action)

            except Exception as e:
                st.error(f"Error processing request: {e}")