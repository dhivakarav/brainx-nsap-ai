"""
AI14 - Comprehensive Fraud Detection ML/DL Models
==================================================
Government-Grade Social Security Fraud Detection System

This module contains all ML and DL models for detecting fraudulent beneficiaries
including deceased individuals still receiving benefits.

Model Categories:
- Anomaly Detection (Isolation Forest, One-Class SVM, LOF, Autoencoder)
- Supervised Models (Logistic Regression, Random Forest, XGBoost, LightGBM, Neural Networks)
- Clustering Models (K-Means, DBSCAN)
- Graph-Based Models (Fraud cluster detection)
- Time-Series Models (ARIMA, LSTM)
- NLP Models (TF-IDF, Fuzzy Matching, BERT)
- Risk Scoring System
- Ensemble Models

Data Sources:
- Open Government Data Platform India (data.gov.in)
- National Social Assistance Programme (NSAP)
- State government pension portals
- Census 2011 datasets
- Simulated Death Master File (for demonstration)
"""

try:
    from .comprehensive_model_suite import (
        FraudDetectionPipeline,
        AnomalyDetectionModels,
        SupervisedModels,
        ClusteringModels,
        GraphBasedModels,
        TimeSeriesModels,
        NLPModels,
        RiskScoringSystem,
        EnsembleModels
    )
except Exception:
    pass

__version__ = '1.0.0'
__author__ = 'AI14 Hackathon Team'
