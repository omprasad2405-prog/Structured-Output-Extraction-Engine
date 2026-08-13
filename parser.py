<<<<<<< HEAD
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
    
    # Extract expected JSON schema directly from Pydantic
    schema_json = EmotionalFeedback.model_json_schema()
    
    # 3. Pass schema explicitly in system prompt
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

# Sample Input
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
=======
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schemas import EmotionalFeedback

print("1. Starting script execution...")

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file!")
    sys.exit(1)
else:
    print("2. Gemini API Key loaded successfully from .env!")

# Initialize the official Gemini client
client = genai.Client(api_key=api_key)

def analyze_user_text(text_input: str) -> EmotionalFeedback:
    print("3. Sending text to Gemini API... (please wait a few seconds)")
    
    # List of models to attempt in order
    candidate_models = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]
    
    for model_name in candidate_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=text_input,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are an empathetic feedback analyst. "
                        "Analyze the user text and fill out the required schema accurately."
                    ),
                    response_mime_type="application/json",
                    response_schema=EmotionalFeedback,  # Enforces Pydantic schema
                    temperature=0.2,
                ),
            )
            print(f"4. API response received using model: {model_name}!")
            # Validate raw JSON response into Pydantic model instance
            return EmotionalFeedback.model_validate_json(response.text)
        except Exception as e:
            if "404" in str(e) or "NOT_FOUND" in str(e):
                print(f"⚠️ Model {model_name} unavailable, trying next model...")
                continue
            else:
                print(f"❌ API Error: {e}")
                sys.exit(1)
                
    print("❌ All candidate models failed.")
    sys.exit(1)

sample_text = (
    "I've been working on my college submission all night, but my code keeps crashing! "
    "I feel completely drained, stressed, and annoyed because no one is replying on Discord."
)

print("\n--- BEGINNING EXTRACTION TEST ---")
result = analyze_user_text(sample_text)

print("\n--- EXTRACTED STRUCTURED DATA ---")
print(f"Sentiment:        {result.sentiment}")
print(f"Primary Emotion:  {result.primary_emotion}")
print(f"Urgency Score:    {result.urgency_score} / 5")
print(f"Key Points:       {result.key_points}")
print(f"Suggested Action: {result.suggested_action}")
>>>>>>> f1cd7c228d80068c1824fcbf16ac569a9fafd4ea
