from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field

class ProductCreateItem(BaseModel):
    id: Optional[UUID] = None
    provider: UUID
    number: Optional[int] = 0
    category_ids: Optional[List[UUID]] = Field(default_factory=list)

class ProductResponse(BaseModel):
    id: UUID
    provider: UUID
    number: Optional[int]
    category_ids: List[UUID] = Field(default_factory=list)

class CursorPageProductResponse(BaseModel):
    items: List[ProductResponse]
    next_cursor: Optional[UUID] = None