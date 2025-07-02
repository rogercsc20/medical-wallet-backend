from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Medical Wallet API",
    version="0.1.0",
    description="HIPAA-compliant, FHIR-native backend for patient-controlled health data (CKD MVP)",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint for uptime monitoring and orchestration.
    """
    return {"status": "ok", "version": app.version}

@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to the Medical Wallet API (CKD MVP)"}
