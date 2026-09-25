import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from typing import List, Optional

SECRET_KEY = "my_super_secret_key_for_test_auth_service_jwt"
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 60 * 24  # 1 ngày tương đương bản Java

def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(username: str, roles: List[str]) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_MINUTES)
    to_encode = {
        "sub": username,
        "roles": ",".join(roles),
        "iat": datetime.now(timezone.utc),
        "exp": expire
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None