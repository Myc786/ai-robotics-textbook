from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class QueryBase(BaseModel):
    query_text: str
    mode: str  # 'global' or 'selected_text'
    selected_text: Optional[str] = None


class QueryCreate(QueryBase):
    pass


class QueryUpdate(BaseModel):
    query_text: Optional[str] = None
    mode: Optional[str] = None
    selected_text: Optional[str] = None


class Query(QueryBase):
    query_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True