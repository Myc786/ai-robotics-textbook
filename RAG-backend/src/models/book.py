from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime
import uuid


class BookBase(BaseModel):
    title: str
    author: Optional[str] = None
    isbn: Optional[str] = None
    metadata: Optional[dict] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    metadata: Optional[dict] = None


class Book(BookBase):
    book_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChapterBase(BaseModel):
    book_id: uuid.UUID
    title: str
    chapter_number: Optional[int] = None
    content: Optional[str] = None


class ChapterCreate(ChapterBase):
    pass


class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    chapter_number: Optional[int] = None
    content: Optional[str] = None


class Chapter(ChapterBase):
    chapter_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SectionBase(BaseModel):
    chapter_id: uuid.UUID
    title: str
    section_number: Optional[int] = None
    content: Optional[str] = None


class SectionCreate(SectionBase):
    pass


class SectionUpdate(BaseModel):
    title: Optional[str] = None
    section_number: Optional[int] = None
    content: Optional[str] = None


class Section(SectionBase):
    section_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True