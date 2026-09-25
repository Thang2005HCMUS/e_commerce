import asyncpg
from typing import Optional

DATABASE_URL = "postgresql://dev:123456@localhost:5432/testdev"

pool: Optional[asyncpg.Pool] = None

async def init_db_pool():
    global pool
    pool = await asyncpg.create_pool(dsn=DATABASE_URL, min_size=1, max_size=10)
    
    # Tạo bảng và dữ liệu khởi tạo nếu chưa tồn tại
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id SERIAL PRIMARY KEY,
                name VARCHAR(16) UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
                created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP WITHOUT TIME ZONE
            );

            CREATE TABLE IF NOT EXISTS user_roles (
                user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                role_id INT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
                PRIMARY KEY (user_id, role_id)
            );

            -- Thêm role mặc định nếu chưa có
            INSERT INTO roles (name) 
            VALUES ('ROLE_CUSTOMER'), ('ROLE_ADMIN') 
            ON CONFLICT (name) DO NOTHING;
        """)

async def close_db_pool():
    global pool
    if pool:
        await pool.close()

def get_pool() -> asyncpg.Pool:
    if pool is None:
        raise RuntimeError("Database pool chưa được khởi tạo!")
    return pool