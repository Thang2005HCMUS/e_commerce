from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Query, HTTPException, status
from asyncpg.exceptions import ForeignKeyViolationError

from src.product.schemas import (
    ProductCreateItem,
    ProductResponse,
    CursorPageProductResponse,
)
from src.product import repository

router = APIRouter(prefix="/products", tags=["Product"])

# 1. Liệt kê tất cả mặt hàng (Không cursor - dùng offset)
@router.get("", response_model=List[ProductResponse])
async def list_products(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return await repository.list_products_offset(limit=limit, offset=offset)

# 2. Liệt kê tất cả mặt hàng (Có cursor phân trang)
@router.get("/cursor", response_model=CursorPageProductResponse)
async def list_products_cursor(
    limit: int = Query(20, ge=1, le=100),
    cursor: Optional[UUID] = Query(None)
):
    items = await repository.list_products_cursor(limit=limit, cursor=cursor)
    next_cursor = items[-1]["id"] if len(items) == limit else None
    return CursorPageProductResponse(items=items, next_cursor=next_cursor)

# 3. Liệt kê mặt hàng theo nhà cung cấp (Không cursor - dùng offset)
@router.get("/provider/{provider_id}", response_model=List[ProductResponse])
async def list_products_by_provider(
    provider_id: UUID,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return await repository.list_products_by_provider_offset(
        provider_id=provider_id, limit=limit, offset=offset
    )

# 4. Liệt kê mặt hàng theo nhà cung cấp (Có cursor phân trang)
@router.get("/provider/{provider_id}/cursor", response_model=CursorPageProductResponse)
async def list_products_by_provider_cursor(
    provider_id: UUID,
    limit: int = Query(20, ge=1, le=100),
    cursor: Optional[UUID] = Query(None)
):
    items = await repository.list_products_by_provider_cursor(
        provider_id=provider_id, limit=limit, cursor=cursor
    )
    next_cursor = items[-1]["id"] if len(items) == limit else None
    return CursorPageProductResponse(items=items, next_cursor=next_cursor)

# 5. API thêm nhiều mặt hàng / hàng hóa cùng lúc
@router.post("/batch", response_model=List[ProductResponse], status_code=status.HTTP_201_CREATED)
async def create_products_batch(products: List[ProductCreateItem]):
    if not products:
        raise HTTPException(status_code=400, detail="Danh sách mặt hàng không được trống!")
    try:
        return await repository.create_products_batch(products)
    except ForeignKeyViolationError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Provider hoặc Category không tồn tại: {str(e)}"
        )