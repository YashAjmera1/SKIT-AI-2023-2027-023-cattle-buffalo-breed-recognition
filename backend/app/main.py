from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import models  # noqa: F401  (registers tables)
from app.database import Base, engine
from app.routers import breeds, predict
from app.services.model_service import get_model

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Indian Cattle & Buffalo Breed Recognition API",
    description="Enterprise REST API for AI-powered livestock biometrics and breed recognition. Supports UN SDG 2 (Zero Hunger) & ICAR-NBAGR standards.",
    version="1.1.0",
)

# Secure Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=*, microphone=()"
    return response


app.include_router(predict.router)
app.include_router(breeds.router)


# Consistent structured error responses
@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"error": "Invalid request parameters", "details": exc.errors()})


@app.exception_handler(Exception)
async def unhandled_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "Internal server processing error"})


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Indian Cattle & Buffalo Breed Recognition API is running",
        "system": "Indian Cattle & Buffalo Breed Recognition API",
        "institution": "Swami Keshvanand Institute of Technology (SKIT), Jaipur",
        "project_id": "SKIT/AI/2023-2027/023",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
def health():
    model = get_model()
    return {
        "status": "ok",
        "model_mode": model.mode,
        "classes_supported": len(model.class_names),
        "security_gatekeeper": "active"
    }
