from fastapi import APIRouter, HTTPException, status, Depends, Header
from typing import Optional

from src.auth.schemas import RegisterRequest, LoginRequest, AuthResponse
from src.auth.security import hash_password, verify_password, create_access_token, decode_token
from src.auth import repository

router = APIRouter(prefix="/auth", tags=["Auth"])

# --- Dependencies xác thực / phân quyền ---
def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token hop le hoac da het han!"
        )
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token hop le hoac da het han!"
        )
    return payload

def require_role(required_role: str):
    def role_checker(user: dict = Depends(get_current_user)):
        roles = user.get("roles", "").split(",")
        if required_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Khong co quyen truy cap!"
            )
        return user
    return role_checker

# --- Endpoints ---
@router.get("/test")
async def test_auth_service():
    return "auth service is ready"

@router.post("/register")
async def register(request: RegisterRequest):
    if await repository.exists_by_username(request.username):
        raise HTTPException(status_code=400, detail="Username đã tồn tại!")
    if await repository.exists_by_email(request.email):
        raise HTTPException(status_code=400, detail="Email đã tồn tại!")
        
    hashed_pwd = hash_password(request.password)
    await repository.create_user_with_role(request.username, request.email, hashed_pwd)
    return "Đăng ký tài khoản thành công!"

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    user = await repository.get_user_by_username(request.username)
    if not user or not verify_password(request.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai username hoặc password!"
        )
    
    roles = await repository.get_user_roles(user["id"])
    token = create_access_token(username=user["username"], roles=roles)
    return AuthResponse(accessToken=token, tokenType="Bearer")

@router.get("/any-user")
async def any_user(current_user: dict = Depends(get_current_user)):
    return "Bạn đã đăng nhập thành công! Bất kỳ user nào cũng thấy được thông báo này."

@router.get("/customer-only")
async def customer_only(current_user: dict = Depends(require_role("ROLE_CUSTOMER"))):
    return "Chào mừng quý khách! Đây là tính năng dành riêng cho CUSTOMER."

@router.get("/admin-only")
async def admin_only(current_user: dict = Depends(require_role("ROLE_ADMIN"))):
    return "Khu vực quản trị! Đây là tính năng dành riêng cho ADMIN."