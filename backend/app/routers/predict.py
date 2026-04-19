from fastapi import APIRouter, HTTPException, Depends
import pandas as pd
import numpy as np
from app.schemas import WaterQualityInput, PredictionResponse
from app.dependencies import get_model, get_scaler, get_metadata

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict(
    data: WaterQualityInput,
    model=Depends(get_model),
    scaler=Depends(get_scaler),
    metadata=Depends(get_metadata)
):
    try:
        # 1. Préparer le DataFrame d'entrée
        input_dict = {
            'Salinity (ppt)': data.salinity,
            'pH': data.ph,
            'SecchiDepth (m)': data.secchi_depth,
            'WaterDepth (m)': data.water_depth,
            'WaterTemp (C)': data.water_temp,
            'AirTemp (C)': data.air_temp,
        }
        # Oxygène dissous optionnel
        if data.dissolved_oxygen is not None:
            input_dict['DissolvedOxygen (mg/L)'] = data.dissolved_oxygen
        else:
            input_dict['DissolvedOxygen (mg/L)'] = 7.0  # valeur par défaut

        df_input = pd.DataFrame([input_dict])

        # 2. Récupérer la liste exacte des features depuis les métadonnées
        feature_cols = metadata['features_finales']
        ds = df_input.copy()

        # ---- Features dérivées (identiques à l'entraînement) ----
        ds['DO_Temp_Ratio'] = (ds['DissolvedOxygen (mg/L)'] /
                               (ds['WaterTemp (C)'] + 0.1)).clip(0.073, 4.594)
        ds['Secchi_Depth_Ratio'] = (ds['SecchiDepth (m)'] /
                                    (ds['WaterDepth (m)'] + 0.01)).clip(0, 1)
        ds['pH_Deviation'] = abs(ds['pH'] - 8.1)
        ds['Thermal_Stress'] = ds['WaterTemp (C)'].apply(
            lambda t: max(0, t-25) + max(0, 15-t))
        ds['AirWater_TempDiff'] = ds['AirTemp (C)'] - ds['WaterTemp (C)']

        # ---- Log transforms ----
        ds['Log_Salinity'] = np.log1p(ds['Salinity (ppt)'])
        ds['Log_Secchi'] = np.log1p(ds['SecchiDepth (m)'])
        ds['Log_WaterDepth'] = np.log1p(ds['WaterDepth (m)'])

        # ---- Zone géographique (proxy) ----
        ds['Zone'] = ds['WaterDepth (m)'].apply(
            lambda d: 'Zone_Cotiere' if d <= 1.0 else ('Zone_Lagon' if d <= 3.0 else 'Zone_Large'))

        # ---- Saison à partir de la température ----
        ds['Season'] = ds['WaterTemp (C)'].apply(
            lambda t: 'Été' if t >= 23 else ('Automne' if t >= 18 else ('Printemps' if t >= 14 else 'Hiver')))

        # ---- One-hot encodages (noms exacts depuis feature_cols) ----
        for col in feature_cols:
            if col.startswith('Saison_'):
                saison = col.split('_')[1]   # ex: Automne, Hiver, Printemps, Été
                ds[col] = (ds['Season'] == saison).astype(int)
            elif col.startswith('Zone_enc_'):
                zone = col.replace('Zone_enc_', '')
                ds[col] = (ds['Zone'] == zone).astype(int)

        # ---- Rolling features (pour une seule ligne, valeur = elle-même) ----
        rolling_pairs = [
            ('DissolvedOxygen (mg/L)', 'DO'),
            ('WaterTemp (C)', 'Temp'),
            ('pH', 'pH'),
            ('Salinity (ppt)', 'Sal')
        ]
        for col, short in rolling_pairs:
            ds[f'Roll7_{short}'] = ds[col]
            ds[f'Roll14_{short}'] = ds[col]
            ds[f'Trend_{short}'] = 0.0

        ds['Month_Sin'] = 0.0
        ds['Month_Cos'] = 1.0

        # ---- Forcer la présence de toutes les colonnes attendues ----
        for col in feature_cols:
            if col not in ds.columns:
                ds[col] = 0

        # ---- Extraire dans l'ordre exact ----
        X = ds[feature_cols].values

        # 3. Normalisation
        X_scaled = scaler.transform(X)

        # 4. Prédiction
        class_id = int(model.predict(X_scaled)[0])
        proba = model.predict_proba(X_scaled)[0]
        confidence = float(proba[class_id])

        # 5. Mapping des labels
        class_mapping = metadata.get('class_mapping', {})
        # Convertir les clés (string) en int si nécessaire
        if class_mapping and all(isinstance(k, str) for k in class_mapping.keys()):
            class_mapping = {int(k): v for k, v in class_mapping.items()}
        if not class_mapping:
            class_mapping = {0: "Excellente", 1: "Bonne", 2: "Acceptable", 3: "Mauvaise", 4: "Dangereuse"}

        label = class_mapping.get(class_id, f"Classe {class_id}")

        # Probabilités pour toutes les classes
        probabilities = {}
        for i, p in enumerate(proba):
            lbl = class_mapping.get(i, f"Classe {i}")
            probabilities[lbl] = float(p)

        return PredictionResponse(
            class_id=class_id,
            label=label,
            confidence=confidence,
            probabilities=probabilities
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))