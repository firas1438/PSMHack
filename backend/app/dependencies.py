import joblib
import pickle
import json
import os
from fastapi import HTTPException

MODEL_PATH = "artifacts/xgb_water_quality_model.joblib"
SCALER_PATH = "artifacts/scaler_minmax.pkl"
METADATA_PATH = "artifacts/model_metadata.json"

model = None
scaler = None
metadata = None

def load_artifacts():
    """
    Load ML model, scaler, and metadata from the artifacts directory.
    """
    global model, scaler, metadata
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
            
        model = joblib.load(MODEL_PATH)
        
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
            
        with open(METADATA_PATH, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
            
        print("Success: Model, scaler, and metadata loaded.")
    except Exception as e:
        print(f"Error loading artifacts: {e}")
        raise HTTPException(status_code=500, detail="Machine Learning models are not currently available.")

def get_model():
    if model is None:
        load_artifacts()
    return model

def get_scaler():
    if scaler is None:
        load_artifacts()
    return scaler

def get_metadata():
    if metadata is None:
        load_artifacts()
    return metadata

def get_feature_names():
    meta = get_metadata()
    return meta.get('features_finales', [])