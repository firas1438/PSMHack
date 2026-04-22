import pandas as pd
from app.schemas import WaterQualityInput, PredictionResponse
from app.utils.feature_engineering import build_features_with_metadata

def run_prediction(data: WaterQualityInput, model, scaler, metadata) -> PredictionResponse:
    """
    Handle feature engineering, normalization, and model inference for water livability.
    """
    # 1. Prepare raw input dictionary
    input_dict = {
        'Salinity (ppt)': data.salinity,
        'pH': data.ph,
        'SecchiDepth (m)': data.secchi_depth,
        'WaterDepth (m)': data.water_depth,
        'WaterTemp (C)': data.water_temp,
        'AirTemp (C)': data.air_temp,
    }
    
    if data.dissolved_oxygen is not None:
        input_dict['DissolvedOxygen (mg/L)'] = data.dissolved_oxygen
    else:
        input_dict['DissolvedOxygen (mg/L)'] = 7.0 # Default value

    df_input = pd.DataFrame([input_dict])

    # 2. Build features based on model metadata
    X_df = build_features_with_metadata(df_input, metadata)
    X = X_df.values

    # 3. Normalization
    X_scaled = scaler.transform(X)

    # 4. Model Inference
    class_id = int(model.predict(X_scaled)[0])
    proba = model.predict_proba(X_scaled)[0]
    confidence = float(proba[class_id])

    # 5. Label Mapping
    # Fallback to standard labels if metadata mapping is missing
    metadata_mapping = metadata.get('class_mapping', {})
    
    # Ensure keys are integers (json sometimes loads them as strings)
    class_mapping = {int(k): v for k, v in metadata_mapping.items()} if metadata_mapping else {
        0: "Excellent", 
        1: "Good", 
        2: "Acceptable", 
        3: "Poor", 
        4: "Hazardous"
    }

    label = class_mapping.get(class_id, f"Class {class_id}")

    # Build probabilities dictionary for all classes
    probabilities = {}
    for i, p in enumerate(proba):
        lbl = class_mapping.get(i, f"Class {i}")
        probabilities[lbl] = float(p)

    return PredictionResponse(
        class_id=class_id,
        label=label,
        confidence=confidence,
        probabilities=probabilities
    )
