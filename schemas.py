from pydantic import BaseModel, Field
from typing import List, Literal

class EmotionalFeedback(BaseModel):
    sentiment: Literal["Positive", "Neutral", "Negative"] = Field(
        description="Overall tone of the user's message"
    )
    primary_emotion: str = Field(
        description="The main emotion expressed (e.g., Frustrated, Stressed, Excited, Lonely)"
    )
    key_points: List[str] = Field(
        description="List of key points or concerns mentioned by the user"
    )
    urgency_score: int = Field(
        description="Urgency level from 1 (very calm/casual) to 5 (critical/distressed)",
        ge=1,
        le=5
    )
    suggested_action: str = Field(
        description="A brief, empathetic recommendation on how to assist this user"
    )