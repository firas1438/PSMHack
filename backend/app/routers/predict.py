from fastapi import APIRouter, HTTPException, Depends
from app.schemas import WaterQualityInput, PredictionResponse
from app.dependencies import get_model, get_scaler, get_metadata
from app.services.livability_service import run_prediction

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict_water_quality(
    data: WaterQualityInput,
    model=Depends(get_model),
    scaler=Depends(get_scaler),
    metadata=Depends(get_metadata)
):
    """
    Endpoint to predict seawater livability class based on physical-chemical parameters.
    """
    try:
        response = run_prediction(data, model, scaler, metadata)
        return response
    except Exception as e:
        # Log error in a real production app
        raise HTTPException(status_code=400, detail=str(e))