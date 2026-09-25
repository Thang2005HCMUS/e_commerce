 
from typing import Optional, List, Dict, Any
from uuid import UUID
from src.auth.database import get_pool

async def create_profile(profile_data: dict) -> dict:
    pool = get_pool()
    query = """
        INSERT INTO user_service.user_profiles 
        (auth_user_id, first_name, last_name, phone, avatar_url, gender, date_of_birth)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING *
    """
    row = await pool.fetchrow(query, profile_data['auth_user_id'], profile_data.get('first_name'),
                              profile_data.get('last_name'), profile_data.get('phone'),
                              profile_data.get('avatar_url'), profile_data.get('gender'),
                              profile_data.get('date_of_birth'))
    return dict(row)

async def get_profile_by_auth_id(auth_user_id: UUID) -> Optional[dict]:
    pool = get_pool()
    query = "SELECT * FROM user_service.user_profiles WHERE auth_user_id = $1"
    row = await pool.fetchrow(query, auth_user_id)
    return dict(row) if row else None

async def update_profile(auth_user_id: UUID, profile_data: dict) -> Optional[dict]:
    pool = get_pool()
    query = """
        UPDATE user_service.user_profiles
        SET first_name = COALESCE($1, first_name),
            last_name = COALESCE($2, last_name),
            phone = COALESCE($3, phone),
            avatar_url = COALESCE($4, avatar_url),
            gender = COALESCE($5, gender),
            date_of_birth = COALESCE($6, date_of_birth),
            updated_at = CURRENT_TIMESTAMP
        WHERE auth_user_id = $7
        RETURNING *
    """
    row = await pool.fetchrow(query, profile_data.get('first_name'), profile_data.get('last_name'),
                              profile_data.get('phone'), profile_data.get('avatar_url'),
                              profile_data.get('gender'), profile_data.get('date_of_birth'),
                              auth_user_id)
    return dict(row) if row else None

async def create_address(profile_id: UUID, address_data: dict) -> dict:
    pool = get_pool()
    query = """
        INSERT INTO user_service.user_addresses 
        (profile_id, recipient_name, phone_number, province, district, ward, detailed_address, is_default)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        RETURNING *
    """
    row = await pool.fetchrow(query, profile_id, address_data['recipient_name'], 
                              address_data['phone_number'], address_data['province'], 
                              address_data['district'], address_data['ward'], 
                              address_data['detailed_address'], address_data.get('is_default', False))
    return dict(row)

async def get_addresses(profile_id: UUID) -> List[dict]:
    pool = get_pool()
    query = "SELECT * FROM user_service.user_addresses WHERE profile_id = $1 ORDER BY is_default DESC, created_at DESC"
    rows = await pool.fetch(query, profile_id)
    return [dict(r) for r in rows]
