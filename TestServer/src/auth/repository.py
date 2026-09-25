from typing import Optional, List, Dict, Any
import asyncpg
from src.auth.database import get_pool

async def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    pool = get_pool()
    query = """
        SELECT id, username, email, password, status 
        FROM users 
        WHERE username = $1
    """
    row = await pool.fetchrow(query, username)
    return dict(row) if row else None

async def exists_by_username(username: str) -> bool:
    pool = get_pool()
    query = "SELECT 1 FROM users WHERE username = $1 LIMIT 1"
    row = await pool.fetchrow(query, username)
    return row is not None

async def exists_by_email(email: str) -> bool:
    pool = get_pool()
    query = "SELECT 1 FROM users WHERE email = $1 LIMIT 1"
    row = await pool.fetchrow(query, email)
    return row is not None

async def get_user_roles(user_id) -> List[str]:
    pool = get_pool()
    query = """
        SELECT r.name 
        FROM roles r
        JOIN user_roles ur ON r.id = ur.role_id
        WHERE ur.user_id = $1
    """
    rows = await pool.fetch(query, user_id)
    return [r["name"] for r in rows]

async def create_user_with_role(username: str, email: str, hashed_pwd: str, role_name: str = "ROLE_CUSTOMER"):
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            # Lấy role_id
            role_row = await conn.fetchrow("SELECT id FROM roles WHERE name = $1", role_name)
            if not role_row:
                raise ValueError(f"Quyền {role_name} không tồn tại trong hệ thống!")
            role_id = role_row["id"]

            # Insert user
            insert_user_query = """
                INSERT INTO users (username, email, password)
                VALUES ($1, $2, $3)
                RETURNING id
            """
            user_row = await conn.fetchrow(insert_user_query, username, email, hashed_pwd)
            user_id = user_row["id"]

            # Map user - role
            await conn.execute(
                "INSERT INTO user_roles (user_id, role_id) VALUES ($1, $2)",
                user_id, role_id
            )