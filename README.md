![AquaLog Poster](/frontend/public/aqualogposter.png)

AquaLog is an AI-driven platform designed to monitor and assess coastal health by combining visual satellite analysis with physical-chemical water metrics. Our mission is to provide environmentalists and researchers with the tools needed to detect marine hazards and ensure the sustainability of coastal ecosystems.



## Context

Coastal regions face significant environmental pressure from industrial activities and climate change. Sudden shifts in water parameters can trigger harmful algal blooms, leading to biodiversity loss and the collapse of local fishing zones.

AquaLog addresses this challenge through two specialized AI modules that transform raw data into actionable insights for researchers, biologists, and environmental agencies. By enabling early detection and precise scoring, we help mitigate the impact of pollution and protect marine life globally.


## Architecture

```
                    ┌──────────────────────────────┐
                    │           AquaLog            │
                    └──────────────┬───────────────┘
                                   │
               ┌───────────────────┴────────────────────┐
               │                                        │
    ┌──────────▼──────────┐               ┌─────────────▼────────────┐
    │  Module 1           │               │  Module 2                │
    │  Visual Detection   │               │  WQI Prediction          │
    │  (Otsu + OpenCV)    │               │  (XGBoost)               │
    └──────────┬──────────┘               └──────────────┬───────────┘
               │                                         │
               └───────────────────┬─────────────────────┘
                                   │
                        ┌──────────▼──────────┐
                        │   Global Diagnosis  │
                        │   + Early Warning   │
                        └─────────────────────┘
```


## Module 1. Visual Algae Detection (Otsu Thresholding)

This module analyzes field or satellite imagery to **locate and quantify algal bloom proliferation**.

**Pipeline:**
```
Color Image → Grayscale → Otsu Thresholding → Morphological Cleaning → Contours → Statistics
```

| Step | Technique |
|-------|-----------|
| Segmentation | Otsu's Thresholding: automatically calculates the optimal threshold without manual tuning |
| Denoising | Morphological opening & closing operations |
| Extraction | Contour detection + false positive filtering by area size |
| Output | Binary mask, Annotated image, Affected surface area (%), Bloom zone count |

> Otsu's method is highly effective for marine imagery where the histogram naturally presents a bimodal distribution between healthy water and bloom zones.


## Module 2. Water Quality & Livability Prediction

Classifies water status into **5 quality levels** based on physical-chemical field measurements.

### Data Overview

- **Source:** [Kaggle - Water Quality Dataset](https://www.kaggle.com/datasets/supriyoain/water-quality-data)

- **2,371 observations:** 8 physical-chemical variables, Multi-decade dataset.
Variables: `pH`, `Salinity`, `Dissolved Oxygen`, `Transparency (Secchi)`, `Water Depth`, `Water & Air Temperature`.

- **Preprocessing:** Anomaly detection and **KNN Imputer** (k = 5) were used to ensure a clean, zero-missing-value dataset.

### Water Quality Index (WQI)
Calculated according to international standards (**WHO & EPA**):
`WQI = 0.30 × SI_DO + 0.25 × SI_pH + 0.20 × SI_Sal + 0.15 × SI_Temp + 0.10 × SI_Secchi`

| Class | Label | WQI Range |
|--------|-------|-----------|
| 0 | Excellent | ≥ 80 |
| 1 | Good | [65 – 80[ |
| 2 | Acceptable | [50 – 65[ |
| 3 | Poor | [30 – 50[ |
| 4 | Hazardous | < 30 |

### Machine Learning & Feature Engineering
**29 features** were engineered from the 7 raw variables, including physical ratios, log-transforms, rolling averages (7 and 14-day windows), and cyclic seasonal encodings. Class imbalance was addressed using **SMOTE** (k = 3).

The final model is an **XGBoost** classifier, optimized via **GridSearchCV** over 144 hyperparameter combinations.

## Results

- Accuracy: 91.7%
- F1-Score (Macro): 92.3%
- ROC-AUC (OvR): 99.1%

Critical classes (**Poor** and **Hazardous**) achieve an F1-Score > **0.89**, confirming the model's high reliability in detecting high-risk scenarios.

> **Note:** If you would like to explore the notebook responsible for the model training, you can find it [here](https://www.kaggle.com/code/kassemabbassi/notebook-pr-diction-qualit-eau-mer)


## Contributions
- Islem Chammakhi 
- Mohamed Kassem Abbassi
- Firas Ben Ali 

---

*"Artificial intelligence should not just understand the world, but actively contribute to its preservation."*