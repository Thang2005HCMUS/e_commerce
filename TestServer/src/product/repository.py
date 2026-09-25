from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from src.auth.database import get_pool

async def list_products_offset(limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
    pool = get_pool()
    query = """
        SELECT p.id, p.provider, p.number,
               COALESCE(array_agg(pc.category) FILTER (WHERE pc.category IS NOT NULL), '{}') AS category_ids
        FROM Product p
        LEFT JOIN Product_Categories pc ON p.Id = pc.product
        GROUP BY p.id, p.provider, p.number
        ORDER BY p.id ASC
        LIMIT $1 OFFSET $2
    """
    rows = await pool.fetch(query, limit, offset)
    return [dict(r) for r in rows]

async def list_products_cursor(limit: int = 20, cursor: Optional[UUID] = None) -> List[Dict[str, Any]]:
    pool = get_pool()
    if cursor:
        query = """
            SELECT p.id, p.provider, p.number,
                   COALESCE(array_agg(pc.category) FILTER (WHERE pc.category IS NOT NULL), '{}') AS category_ids
            FROM Product p
            LEFT JOIN Product_Categories pc ON p.Id = pc.product
            WHERE p.Id > $1
            GROUP BY p.id, p.provider, p.number
            ORDER BY p.id ASC
            LIMIT $2
        """
        rows = await pool.fetch(query, cursor, limit)
    else:
        query = """
            SELECT p.id, p.provider, p.number,
                   COALESCE(array_agg(pc.category) FILTER (WHERE pc.category IS NOT NULL), '{}') AS category_ids
            FROM Product p
            LEFT JOIN Product_Categories pc ON p.Id = pc.product
            GROUP BY p.id, p.provider, p.number
            ORDER BY p.id ASC
            LIMIT $1
        """
        rows = await pool.fetch(query, limit)
    return [dict(r) for r in rows]

async def list_products_by_provider_offset(provider_id: UUID, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
    pool = get_pool()
    query = """
        SELECT p.id, p.provider, p.number,
               COALESCE(array_agg(pc.category) FILTER (WHERE pc.category IS NOT NULL), '{}') AS category_ids
        FROM Product p
        LEFT JOIN Product_Categories pc ON p.Id = pc.product
        WHERE p.provider = $1
        GROUP BY p.id, p.provider, p.number
        ORDER BY p.id ASC
        LIMIT $2 OFFSET $3
    """
    rows = await pool.fetch(query, provider_id, limit, offset)
    return [dict(r) for r in rows]

async def list_products_by_provider_cursor(provider_id: UUID, limit: int = 20, cursor: Optional[UUID] = None) -> List[Dict[str, Any]]:
    pool = get_pool()
    if cursor:
        query = """
            SELECT p.id, p.provider, p.number,
                   COALESCE(array_agg(pc.category) FILTER (WHERE pc.category IS NOT NULL), '{}') AS category_ids
            FROM Product p
            LEFT JOIN Product_Categories pc ON p.Id = pc.product
            WHERE p.provider = $1 AND p.Id > $2
            GROUP BY p.id, p.provider, p.number
            ORDER BY p.id ASC
            LIMIT $3
        """
        rows = await pool.fetch(query, provider_id, cursor, limit)
    else:
        query = """
            SELECT p.id, p.provider, p.number,
                   COALESCE(array_agg(pc.category) FILTER (WHERE pc.category IS NOT NULL), '{}') AS category_ids
            FROM Product p
            LEFT JOIN Product_Categories pc ON p.Id = pc.product
            WHERE p.provider = $1
            GROUP BY p.id, p.provider, p.number
            ORDER BY p.id ASC
            LIMIT $2
        """
        rows = await pool.fetch(query, provider_id, limit)
    return [dict(r) for r in rows]

async def create_products_batch(products: list) -> List[Dict[str, Any]]:
    pool = get_pool()
    created_items = []
    
    async with pool.acquire() as conn:
        async with conn.transaction():
            for p in products:
                prod_id = p.id if p.id else uuid4()
                await conn.execute(
                    """
                    INSERT INTO Product (Id, provider, number)
                    VALUES ($1, $2, $3)
                    """,
                    prod_id, p.provider, p.number
                )
                
                if p.category_ids:
                    cat_records = [(prod_id, cat_id) for cat_id in p.category_ids]
                    await conn.executemany(
                        """
                        INSERT INTO Product_Categories (product, category)
                        VALUES ($1, $2)
                        ON CONFLICT DO NOTHING
                        """,
                        cat_records
                    )
                
                created_items.append({
                    "id": prod_id,
                    "provider": p.provider,
                    "number": p.number,
                    "category_ids": p.category_ids or []
                })
    return created_items