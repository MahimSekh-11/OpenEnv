from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Action(BaseModel):
    action_type: str = Field(..., description="Type of action: 'categorize', 'respond', or 'close'")
    category: Optional[str] = Field(None, description="Category for the ticket (e.g., 'billing', 'technical', 'account')")
    message: Optional[str] = Field(None, description="The response message to the customer")

class Observation(BaseModel):
    ticket_id: str
    content: str
    history: List[Dict[str, str]]
    available_categories: List[str]
    status: str

class Reward(BaseModel):
    value: float = Field(..., ge=0.0, le=1.0)
    explanation: str

class State(BaseModel):
    current_ticket_index: int
    tickets: List[Dict[str, Any]]
    history: List[Dict[str, str]]
    is_done: bool
    score: float
