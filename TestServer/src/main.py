from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.auth.database import init_db_pool, close_db_pool
from src.auth.router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db_pool()
    yield
    await close_db_pool()

app = FastAPI(
    title="Monolith Application",
    lifespan=lifespan
)

# 1. Bật CORS để React gọi API không bị chặn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc điền chính xác origin của React: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Đồng bộ format lỗi trả về thành { "message": "..." } cho frontend bắt được
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_err = exc.errors()[0]
    msg = f"{first_err.get('loc', [''])[-1]}: {first_err.get('msg', 'Dữ liệu không hợp lệ')}"
    return JSONResponse(
        status_code=400,
        content={"message": msg}
    )

# Đăng ký module Auth
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Monolith Server is running"}