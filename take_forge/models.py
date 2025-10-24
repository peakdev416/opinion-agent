from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Article(BaseModel):
    id: str
    title: str
    published_at: Optional[datetime | str] = None
    source_url: Optional[str] = None
    content: str


class OpinionTake(BaseModel):
    headline: str = Field(..., max_length=160)
    explanation: str
    stance: Optional[str] = Field(None, description="pro|contra|neutral")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)


class TakeBundle(BaseModel):
    article_id: str
    takes: List[OpinionTake]
