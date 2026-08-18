import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from schemas import EmotionalFeedback

# Page Configuration
st.set_page_config(
    page_title="Feedback Emotion Analyzer",
    page_icon="⚡",
    layout="centered"
)

# Load Environment Variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

st.title("⚡ Structured Feedback Analyzer")
st.caption("Extract typed JSON schema analytics from raw text using Groq & Pydantic")

if not api_key:
    st.error("❌ GROQ_API_KEY not found in .env file!")
    st.stop()

# Initialize Client
client = Groq(api_key=api_key)

def analyze_user_text(text_input: str) -> EmotionalFeedback:
    schema_json = EmotionalFeedback.model_json_schema()
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
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

# User Input
user_text = st.text_area(
    "Enter customer/user feedback text:",
    height=120,
    placeholder="e.g., I've been trying to log in for two hours, but the submit button is unresponsive..."
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

                # Top Metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Sentiment", result.sentiment)
                col2.metric("Primary Emotion", result.primary_emotion)
                col3.metric("Urgency Score", f"{result.urgency_score} / 5")

                # Key Points
                st.subheader("📌 Key Points Identified")
                for point in result.key_points:
                    st.markdown(f"- {point}")

                # Recommended Action
                st.subheader("💡 Suggested Action")
                st.info(result.suggested_action)

            except Exception as e:
                st.error(f"Error processing request: {e}")