from pydantic import BaseModel, Field, validator
from typing import Optional, Dict

class WaterQualityInput(BaseModel):
    salinity: float = Field(..., ge=0, le=45, description="Salinité (ppt)")
    ph: float = Field(..., ge=0, le=14, description="pH")
    secchi_depth: float = Field(..., ge=0, description="Profondeur Secchi (m)")
    water_depth: float = Field(..., gt=0, description="Profondeur d'eau (m)")
    water_temp: float = Field(..., ge=-5, le=45, description="Température eau (°C)")
    air_temp: float = Field(..., ge=-20, le=60, description="Température air (°C)")
    dissolved_oxygen: Optional[float] = Field(None, ge=0, le=20, description="Oxygène dissous (mg/L)")

    @validator('secchi_depth')
    def secchi_le_water_depth(cls, v, values):
        if 'water_depth' in values and v > values['water_depth']:
            raise ValueError('SecchiDepth ne peut pas dépasser WaterDepth')
        return v

class PredictionResponse(BaseModel):
    class_id: int
    label: str
    confidence: float
    probabilities: Dict[str, float]