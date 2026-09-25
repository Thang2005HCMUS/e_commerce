 
import asyncpg
from src.auth.database import get_pool

async def init_user_db():
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE SCHEMA IF NOT EXISTS user_service;

            CREATE TABLE IF NOT EXISTS user_service.user_profiles (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                auth_user_id UUID NOT NULL UNIQUE,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                phone VARCHAR(20) UNIQUE,
                avatar_url VARCHAR(500),
                gender VARCHAR(10),
                date_of_birth DATE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS user_service.user_addresses (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                profile_id UUID NOT NULL,
                recipient_name VARCHAR(100) NOT NULL,
                phone_number VARCHAR(20) NOT NULL,
                province VARCHAR(100) NOT NULL,
                district VARCHAR(100) NOT NULL,
                ward VARCHAR(100) NOT NULL,
                detailed_address VARCHAR(255) NOT NULL,
                is_default BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_address_profile FOREIGN KEY (profile_id) 
                    REFERENCES user_service.user_profiles(id) ON DELETE CASCADE
            );
            
            CREATE INDEX IF NOT EXISTS idx_user_addresses_profile_id ON user_service.user_addresses(profile_id);
        """)
