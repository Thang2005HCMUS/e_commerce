 
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID

from src.user.schemas import UserProfileUpdate, UserProfileResponse, UserAddressCreate, UserAddressResponse, UserProfileCreate
from src.user import repository
from src.auth.router import get_current_user

router = APIRouter(prefix="/users", tags=["User Profile"])

@router.post("/profile", response_model=UserProfileResponse)
async def create_profile(profile_data: UserProfileCreate, current_user: dict = Depends(get_current_user)):
    existing = await repository.get_profile_by_auth_id(profile_data.auth_user_id)
    if existing:
        raise HTTPException(status_code=400, detail="Profile đã tồn tại!")
    profile = await repository.create_profile(profile_data.model_dump())
    return profile

@router.get("/profile/{auth_user_id}", response_model=UserProfileResponse)
async def get_profile(auth_user_id: UUID, current_user: dict = Depends(get_current_user)):
    profile = await repository.get_profile_by_auth_id(auth_user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Không tìm thấy profile!")
    return profile

@router.put("/profile/{auth_user_id}", response_model=UserProfileResponse)
async def update_profile(auth_user_id: UUID, profile_data: UserProfileUpdate, current_user: dict = Depends(get_current_user)):
    profile = await repository.update_profile(auth_user_id, profile_data.model_dump(exclude_unset=True))
    if not profile:
        raise HTTPException(status_code=404, detail="Không tìm thấy profile!")
    return profile
    
@router.post("/profile/{profile_id}/addresses", response_model=UserAddressResponse)
async def add_address(profile_id: UUID, address_data: UserAddressCreate, current_user: dict = Depends(get_current_user)):
    address = await repository.create_address(profile_id, address_data.model_dump())
    return address

@router.get("/profile/{profile_id}/addresses", response_model=List[UserAddressResponse])
async def get_addresses(profile_id: UUID, current_user: dict = Depends(get_current_user)):
    addresses = await repository.get_addresses(profile_id)
    return addresses
