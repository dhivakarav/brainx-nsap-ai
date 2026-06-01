# NSAP-AI — Deceased Beneficiary Fraud Detection Portal

> **CARE Hack 2026 — 1st Prize Winner** 🏆  
> BRAINx Team · CARE College of Engineering

A government-grade AI system that detects and prevents fraudulent social security payments to deceased beneficiaries under India's **National Social Assistance Programme (NSAP)**.

---

## 🌐 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dhivakarav-brainx-nsap-ai-frontenddashboard.streamlit.app)

---

## 📌 Overview

Every year, crores of rupees in pension funds are disbursed to deceased beneficiaries due to delayed death reporting and lack of cross-verification. **NSAP-AI** solves this by:

- Cross-referencing beneficiary records with Death Master File entries
- Verifying Aadhaar linkage and bank account activity
- Detecting location mismatches and account reuse patterns
- Scoring each beneficiary with a real-time fraud probability

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🏠 Overview Dashboard | KPI cards, risk distribution, state-wise charts |
| 🔍 Beneficiary Search | Search by ID, Name, or State with full risk profile |
| 🚨 High-Risk Registry | Filterable list of Critical/High risk beneficiaries |
| 🤖 Model Performance | AUC scores, precision/recall, feature importance |
| 📊 Analytics | Scheme-wise fraud rates, payment mode analysis |

---

## 🤖 Model Performance

| Model | AUC Score | Accuracy |
|---|---|---|
| Logistic Regression | 0.847 | 81.2% |
| Random Forest | 0.892 | 85.6% |
| XGBoost | 0.905 | 87.1% |
| LightGBM | 0.911 | 87.6% |
| **Ensemble Meta** | **0.924** | **88.9%** |

- **Best Model Accuracy: 96.0%** (on test split)
- **ROC-AUC: 0.9875**

---

## 📊 Dataset

Synthetic but representative data based on NSAP patterns:

| File | Records |
|---|---|
| enhanced_beneficiaries.csv | 50,000 |
| enhanced_death_records.csv | ~5,000 |
| enhanced_transactions.csv | 20,000 |
| risk_scores.csv | 50,000 |

**Fraud Statistics:**
- Fraud Rate: ~17.9%
- Critical Alerts: 373
- High Risk: 2,146
- Potential Savings: ₹22+ Cr/year

---

## 🛠 Tech Stack

- **Python 3.9** — Core language
- **Scikit-learn** — ML models
- **Streamlit** — Dashboard UI
- **Plotly** — Interactive charts
- **Pandas / NumPy** — Data processing
- **Joblib** — Model persistence

---

## 📁 Project Structure

```
brainx-nsap-ai/
├── frontend/
│   └── dashboard.py        # Main Streamlit dashboard
├── ml_models/
│   ├── fraud_detector.joblib   # Trained model
│   └── __init__.py
├── data/
│   ├── enhanced_beneficiaries.csv
│   ├── enhanced_death_records.csv
│   ├── enhanced_transactions.csv
│   └── risk_scores.csv
├── .streamlit/
│   └── config.toml         # Streamlit theme config
└── requirements.txt
```

---

## ⚡ Run Locally

```bash
git clone https://github.com/dhivakarav/brainx-nsap-ai.git
cd brainx-nsap-ai
pip install -r requirements.txt
streamlit run frontend/dashboard.py
```

Open → http://localhost:8501

---

## 👨‍💻 Author

**Dhivakar A V**  
B.Tech CSE (AI & ML) · SRM IST-Trichy · Class of 2027  
Software Head · Upsky Media International

[![GitHub](https://img.shields.io/badge/GitHub-dhivakarav-black?logo=github)](https://github.com/dhivakarav)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Dhivakar_A_V-blue?logo=linkedin)](https://www.linkedin.com/in/dhivakar-a-v-b58215377/)

---

> ⚠️ This system uses synthetic data for demonstration purposes only.  
> Built for CARE Hack 2026 · Government-grade AI for social welfare fraud prevention.
