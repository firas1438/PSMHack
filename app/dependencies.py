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
    global model, scaler, metadata
    try:
        model = joblib.load(MODEL_PATH)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        with open(METADATA_PATH, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        print("✅ Modèle, scaler et métadonnées chargés")
    except Exception as e:
        print(f"❌ Erreur de chargement: {e}")
        raise HTTPException(status_code=500, detail="Modèle non disponible")

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



# Ajoutez cette fonction
def get_feature_names():
    metadata = get_metadata()
    return metadata.get('features_finales', [])