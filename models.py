from pydantic import BaseModel
from typing import Literal
from enum import Enum

intents = ["analyze", "unknown", "record", "stats"]


class IntentResponse(BaseModel):
    intent: Literal[intents]

class IntentRequest(BaseModel):
    intent: Literal[intents]

class RecordResponse(BaseModel):
    amount: float
    category: str