import pandas as pd
import numpy as np

def build_features_with_metadata(input_df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
    """
    Construit les features exactes utilisées lors de l'entraînement,
    en s'assurant que toutes les colonnes attendues sont présentes,
    avec les bons noms (ceux des métadonnées).
    """
    ds = input_df.copy()
    feature_cols = metadata['features_finales']  # Liste exacte

    # Valeur par défaut pour l'oxygène dissous s'il n'est pas fourni
    if 'DissolvedOxygen (mg/L)' not in ds.columns:
        ds['DissolvedOxygen (mg/L)'] = 7.0

    # --- 1. Features dérivées (les mêmes que lors de l'entraînement) ---
    ds['DO_Temp_Ratio'] = (ds['DissolvedOxygen (mg/L)'] /
                            (ds['WaterTemp (C)'] + 0.1)).clip(0.073, 4.594)
    ds['Secchi_Depth_Ratio'] = (ds['SecchiDepth (m)'] /
                                 (ds['WaterDepth (m)'] + 0.01)).clip(0, 1)
    ds['pH_Deviation'] = abs(ds['pH'] - 8.1)
    ds['Thermal_Stress'] = ds['WaterTemp (C)'].apply(
        lambda t: max(0, t-25) + max(0, 15-t))
    ds['AirWater_TempDiff'] = ds['AirTemp (C)'] - ds['WaterTemp (C)']

    # --- 2. Log-transforms ---
    ds['Log_Salinity'] = np.log1p(ds['Salinity (ppt)'])
    ds['Log_Secchi'] = np.log1p(ds['SecchiDepth (m)'])
    ds['Log_WaterDepth'] = np.log1p(ds['WaterDepth (m)'])

    # --- 3. Zone ---
    ds['Zone'] = ds['WaterDepth (m)'].apply(
        lambda d: 'Zone_Cotiere' if d <= 1.0 else ('Zone_Lagon' if d <= 3.0 else 'Zone_Large'))

    # --- 4. Saison via température ---
    ds['Season'] = ds['WaterTemp (C)'].apply(
        lambda t: 'Été' if t >= 23 else ('Automne' if t >= 18 else ('Printemps' if t >= 14 else 'Hiver')))

    # --- 5. One-hot encodings (noms exacts sans erreur d'accent) ---
    # On crée un dictionnaire avec les noms exacts tels que dans feature_cols
    # Pour éviter les problèmes d'accent, on utilise les chaînes brutes.
    for col in feature_cols:
        if col.startswith('Saison_'):
            saison = col.split('_')[1]  # ex: "Automne", "Hiver", "Printemps", "Été"
            ds[col] = (ds['Season'] == saison).astype(int)
        elif col.startswith('Zone_enc_'):
            zone = col.replace('Zone_enc_', '')
            ds[col] = (ds['Zone'] == zone).astype(int)

    # --- 6. Rolling (valeurs constantes pour prédiction ponctuelle) ---
    for col, short in [('DissolvedOxygen (mg/L)', 'DO'), ('WaterTemp (C)', 'Temp'),
                       ('pH', 'pH'), ('Salinity (ppt)', 'Sal')]:
        ds[f'Roll7_{short}'] = ds[col]
        ds[f'Roll14_{short}'] = ds[col]
        ds[f'Trend_{short}'] = 0.0

    ds['Month_Sin'] = 0.0
    ds['Month_Cos'] = 1.0

    # --- 7. Forcer la présence de toutes les colonnes attendues ---
    for col in feature_cols:
        if col not in ds.columns:
            ds[col] = 0

    # --- 8. Retourner dans l'ordre exact des métadonnées ---
    return ds[feature_cols]