from datetime import datetime
from pydantic import BaseModel
from typing import Literal, Optional
from enum import Enum

intents = ["analyze", "unknown", "record", "stats"]


class Intent(str, Enum):
    ANALYZE = "analyze"
    UNKNOWN = "unknown"
    RECORD = "record"
    STATS = "stats"


class IntentResponse(BaseModel):
    intent: Intent


class RecordType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class RecordResponse(BaseModel):
    amount: float
    category: str
    type: RecordType


class StatsResponse(BaseModel):
    start_date: str
    end_date: str
    categories: Optional[list[str]] = None


class AnalyzeResponse(BaseModel):
    start_date: str
    end_date: str
