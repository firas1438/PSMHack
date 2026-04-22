from pydantic import BaseModel, Field, validator
from typing import Optional, Dict

class WaterQualityInput(BaseModel):
    salinity: float = Field(..., ge=0, le=45, description="Salinity (ppt)")
    ph: float = Field(..., ge=0, le=14, description="pH level")
    secchi_depth: float = Field(..., ge=0, description="Secchi Depth (m) - water clarity")
    water_depth: float = Field(..., gt=0, description="Total Water Depth (m)")
    water_temp: float = Field(..., ge=-5, le=45, description="Water Temperature (°C)")
    air_temp: float = Field(..., ge=-20, le=60, description="Air Temperature (°C)")
    dissolved_oxygen: Optional[float] = Field(None, ge=0, le=20, description="Dissolved Oxygen (mg/L)")

    @validator('secchi_depth')
    def secchi_le_water_depth(cls, v, values):
        if 'water_depth' in values and v > values['water_depth']:
            raise ValueError('SecchiDepth cannot exceed WaterDepth')
        return v

class PredictionResponse(BaseModel):
    class_id: int
    label: str
    confidence: float
    probabilities: Dict[str, float]