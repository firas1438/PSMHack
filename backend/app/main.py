from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import predict, segment

app = FastAPI(
    title="Aqualog API",
    description="Coastal water quality assessment and algae bloom detection API",
    version="1.0.0",
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(predict.router, prefix="/api/v1", tags=["prediction"])
app.include_router(segment.router, prefix="/api/v1", tags=["segmentation"])

@app.get("/")
async def root():
    return {"message": "Aqualog API - Welcome"}
