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
    description="Backend for AI-powered breed recognition (EfficientNet-B0). Supports UN SDG 2.",
    version="1.0.0",
)

# Allow the React frontend (Vite default port + CRA port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router)
app.include_router(breeds.router)


# Sprint 4: consistent error responses
@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"error": "Invalid request", "details": exc.errors()})


@app.exception_handler(Exception)
async def unhandled_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "Internal server error"})


@app.get("/", tags=["Health"])
def root():
    return {"message": "Breed Recognition API is running", "docs": "/docs"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "model_mode": "mock" if get_model().mock else "trained-model"}
