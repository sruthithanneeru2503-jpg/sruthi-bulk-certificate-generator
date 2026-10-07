from pydantic import BaseModel, EmailStr, Field
from typing import List


class RecipientCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr


class JobCreate(BaseModel):
    event_name: str = Field(..., min_length=1)
    event_date: str = Field(..., min_length=1)
    recipients: List[RecipientCreate] = Field(..., min_length=1)