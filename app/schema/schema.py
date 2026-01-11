
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List, Optional

class Message(BaseModel):
    role: str    # "user" or "assistant"
    content: str
    
    @validator('role')
    def validate_role(cls, v):
        if v not in ["user", "assistant"]:
            raise ValueError('role must be "user" or "assistant"')
        return v
    
    @validator('content')
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError('content cannot be empty')
        return v

class AIRequest(BaseModel):
    messages: List[Message]
    user_id: str
    
    @validator('messages')
    def validate_messages(cls, v):
        if not v:
            raise ValueError('messages list cannot be empty')
        return v
    
    @validator('user_id')
    def validate_user_id(cls, v):
        if not v or not v.strip():
            raise ValueError('user_id cannot be empty')
        return v

class AIResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None
