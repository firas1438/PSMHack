from fastapi import FastAPI
from app.routers import predict

app = FastAPI(
    title="Water Quality API",
    description="Prédiction de la qualité de l'eau à partir de mesures terrain",
    version="1.0.0"
)

app.include_router(predict.router, prefix="/api/v1", tags=["prediction"])

@app.get("/")
async def root():
    return {"message": "Water Quality API - Bienvenue"}