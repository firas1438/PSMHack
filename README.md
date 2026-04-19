<div align="center">

<br/>

```
 █████╗  ██████╗ ██╗   ██╗ █████╗ ██╗      ██████╗  ██████╗
██╔══██╗██╔═══██╗██║   ██║██╔══██╗██║     ██╔═══██╗██╔════╝
███████║██║   ██║██║   ██║███████║██║     ██║   ██║██║  ███╗
██╔══██║██║▄▄ ██║██║   ██║██╔══██║██║     ██║   ██║██║   ██║
██║  ██║╚██████╔╝╚██████╔╝██║  ██║███████╗╚██████╔╝╚██████╔╝
╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝
```



<br/>

*Hackathon Intra-Universitaire IA & Environnement — Université de Monastir*

</div>

---

## 🌊 Contexte

Les gouvernorats de **Monastir et Mahdia** subissent une pression croissante sur leurs eaux côtières due aux activités industrielles et portuaires. La localité de **Ksibet El Mediouni** en est l'exemple concret : épisodes récurrents de marée rouge, mort de la faune marine, contamination des zones de pêche.

AquaLog répond à cette urgence avec deux modules d'IA complémentaires destinés aux experts environnementaux, biologistes et organismes locaux.

---

## 🏗️ Architecture

```
                    ┌─────────────────────────────┐
                    │         AquaLog             │
                    └──────────────┬──────────────┘
                                   │
              ┌────────────────────┴────────────────────┐
              │                                         │
   ┌──────────▼──────────┐               ┌─────────────▼────────────┐
   │  Module 1           │               │  Module 2                │
   │  Détection Visuelle │               │  Prédiction WQI          │
   │  (Otsu + OpenCV)    │               │  (XGBoost)               │
   └──────────┬──────────┘               └─────────────┬────────────┘
              │                                         │
              └──────────────┬──────────────────────────┘
                             │
                  ┌──────────▼──────────┐
                  │   Diagnostic global │
                  │   + Système alerte  │
                  └─────────────────────┘
```

---

## 🔴 Module 1 — Détection Visuelle par Seuillage d'Otsu

Analyse d'images (terrain ou satellite) pour **localiser et quantifier les zones de prolifération algale**.

**Pipeline :**

```
Image couleur → Niveaux de gris → Seuillage Otsu → Nettoyage morphologique → Contours → Statistiques
```

| Étape | Technique |
|-------|-----------|
| Segmentation | Seuillage d'Otsu — calcul automatique du seuil optimal sans paramétrage |
| Débruitage | Ouverture & fermeture morphologique |
| Extraction | Détection de contours + filtrage des faux positifs par surface |
| Sortie | Masque binaire · image annotée · surface affectée (%) · nombre de zones |

> La méthode d'Otsu est particulièrement adaptée aux images marines dont l'histogramme présente une distribution naturellement bimodale entre eaux saines et zones algales.

---

## 📊 Module 2 — Prédiction de la Qualité de l'Eau

Classification de l'état de l'eau en **5 niveaux de qualité** à partir de mesures physicochimiques de terrain.

### Données

**2 371 observations** · 8 variables physicochimiques · collectées entre 1989 et 2019

`pH` · `Salinité` · `Oxygène dissous` · `Transparence (Secchi)` · `Profondeur` · `Température eau & air`

Preprocessing : détection d'anomalies, imputation par **KNN Imputer** (k = 5), dataset final : 2 366 observations sans valeur manquante.

### Indice WQI (variable cible)

Construit selon les normes **OMS & EPA** :

```
WQI = 0.30 × SI_DO  +  0.25 × SI_pH  +  0.20 × SI_Sal  +  0.15 × SI_Temp  +  0.10 × SI_Secchi
```

| Classe | Label | Plage WQI |
|--------|-------|-----------|
| 0 | 🟢 Excellente | ≥ 80 |
| 1 | 🔵 Bonne | [65 – 80[ |
| 2 | 🟡 Acceptable | [50 – 65[ |
| 3 | 🟠 Mauvaise | [30 – 50[ |
| 4 | 🔴 Dangereuse | < 30 |

### Feature Engineering

**29 features** construites depuis les 7 variables brutes : ratios physiques, log-transforms, rolling features (fenêtres 7 et 14 obs.), encodages saisonniers cycliques.

Le fort déséquilibre des classes critiques est corrigé par **SMOTE** (k = 3) → 2 806 observations après rééchantillonnage.

### Modélisation

Un **Random Forest** (baseline) a révélé un surapprentissage significatif (99.8% train vs 87.6% val). Le modèle final retenu est un **XGBoost** optimisé par **GridSearchCV** sur 144 combinaisons d'hyperparamètres.

---

## 📈 Résultats

| Métrique | Score |
|----------|-------|
| **Accuracy** | **91.7 %** |
| **F1-Score macro** | **92.3 %** |
| **ROC-AUC (OvR)** | **99.1 %** |


Les classes critiques **Mauvaise** et **Dangereuse** atteignent un F1-Score > **0.89**, confirmant l'efficacité du rééchantillonnage sur les classes minoritaires.

---

## 🔭 Perspectives

- Intégration d'images satellites **Sentinel-2** pour une couverture spatiale étendue
- Application mobile dédiée aux biologistes et pêcheurs
- Corrélation automatique image ↔ mesures physicochimiques
- Extension à d'autres zones côtières tunisiennes
- Monitoring temps réel via capteurs **IoT**

---

## 👥 Équipe

| Membre | |
|--------|-|
| Islem Chammakhi | Université de Monastir |
| Firas Ben Ali | Université de Monastir |
| Mohamed Kassem Abbassi | Université de Monastir |

---

<div align="center">

*« L'intelligence artificielle ne doit pas seulement comprendre le monde,*
*mais contribuer activement à sa préservation. »*

**🌊 AquaLog · Monastir & Mahdia, Tunisie**

</div>