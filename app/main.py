from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1 import patients, observations, conditions, medications, auth
import logging

# Initialize global logging configuration
setup_logging()
logger = logging.getLogger("medical_wallet_api")

app = FastAPI(
    title="Medical Wallet API",
    description="FHIR-native medical wallet platform for CKD patients",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(patients.router, prefix="/api/v1/patients", tags=["patients"])
app.include_router(observations.router, prefix="/api/v1/observations", tags=["observations"])
app.include_router(conditions.router, prefix="/api/v1/conditions", tags=["conditions"])
app.include_router(medications.router, prefix="/api/v1/medications", tags=["medications"])

@app.on_event("startup")
async def startup_event():
    logger.info("Medical Wallet API startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Medical Wallet API shutdown initiated.")

@app.get("/")
async def root():
    logger.info("Root endpoint accessed.")
    return {"message": "Medical Wallet API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed.")
    return {"status": "healthy", "fhir_server": settings.FHIR_SERVER_URL}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error at {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error. Please contact support."}
    )

