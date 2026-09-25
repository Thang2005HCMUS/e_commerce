 
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from uuid import UUID

class UserProfileCreate(BaseModel):
    auth_user_id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None

class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None

class UserProfileResponse(UserProfileUpdate):
    id: UUID
    auth_user_id: UUID

class UserAddressCreate(BaseModel):
    recipient_name: str = Field(..., max_length=100)
    phone_number: str = Field(..., max_length=20)
    province: str = Field(..., max_length=100)
    district: str = Field(..., max_length=100)
    ward: str = Field(..., max_length=100)
    detailed_address: str = Field(..., max_length=255)
    is_default: bool = False

class UserAddressResponse(UserAddressCreate):
    id: UUID
    profile_id: UUID
