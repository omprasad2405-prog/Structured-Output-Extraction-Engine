import os
import sys
from dotenv import load_dotenv
from groq import Groq
from schemas import EmotionalFeedback

# 1. Load Environment Variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ ERROR: GROQ_API_KEY not found in .env file!")
    sys.exit(1)

# 2. Initialize Groq Client
client = Groq(api_key=api_key)

def analyze_user_text(text_input: str) -> EmotionalFeedback:
    print("Sending text to Groq cloud API...")
    
    # Extract JSON schema directly from Pydantic model
    schema_json = EmotionalFeedback.model_json_schema()
    
    # 3. Request structured JSON from Groq
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
            {
                "role": "user",
                "content": text_input
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.2
    )
    
    # 4. Parse raw JSON into typed Pydantic object
    raw_json = completion.choices[0].message.content
    return EmotionalFeedback.model_validate_json(raw_json)

# Sample Input for testing
sample_text = (
    "I've been working on my college submission all night, but my code keeps crashing! "
    "I feel completely drained, stressed, and annoyed because no one is replying on Discord."
)

if __name__ == "__main__":
    print("--- STARTING EXTRACTION TEST ---")
    result = analyze_user_text(sample_text)

    print("\n--- EXTRACTED STRUCTURED DATA ---")
    print(f"Sentiment:        {result.sentiment}")
    print(f"Primary Emotion:  {result.primary_emotion}")
    print(f"Urgency Score:    {result.urgency_score} / 5")
    print(f"Key Points:       {result.key_points}")
    print(f"Suggested Action: {result.suggested_action}")