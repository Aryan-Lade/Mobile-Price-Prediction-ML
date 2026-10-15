# SmartPrice — Smartphone Price Category Prediction & ML Model Benchmarking System

An end-to-end Machine Learning system for predicting smartphone price categories and benchmarking 4 classification models (**Random Forest**, **Support Vector Machine**, **K-Nearest Neighbors**, and **Multinomial Logistic Regression**).

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.8.0-F7931E.svg)](https://scikit-learn.org/)
[![React](https://img.shields.io/badge/React-19.2-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-6.0-3178C6.svg)](https://www.typescriptlang.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.3-38B2AC.svg)](https://tailwindcss.com/)

---
## Live Preview Link
https://mobile-price-prediction-ml-sandy.vercel.app/

## 📌 Project Overview

- **Problem Type:** Multi-Class Classification (4 Price Tiers: *Budget*, *Mid-Range*, *Premium*, *Flagship*)
- **Dataset:** 980 validated smartphone records with 25 technical and hardware specifications
- **Models Benchmarked:** Random Forest (Champion: **82.65% Acc, 0.9613 ROC-AUC**), SVM, KNN, Logistic Regression
- **Validation:** 5-Fold Stratified Cross-Validation & Grid Search Optimization (Zero Data Leakage)
- **Explainability:** Model-Agnostic Permutation Importance on Test Partition & Tree Gini Impurity (MDI)
- **Full Stack:** FastAPI Backend (10 verified REST endpoints) + React TypeScript Tailwind Interactive Web Dashboard

---

## 📊 Final Model Benchmarking Summary

| Model Architecture | Test Accuracy | 5-Fold CV Accuracy | Macro F1-Score | Weighted F1-Score | Multi-Class ROC-AUC (OvR) | Status |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Random Forest Classifier** 🏆 | **82.65%** | **78.06%** | **79.96%** | **82.39%** | **0.9613** | **Production Champion** |
| **Support Vector Machine (RBF)** | **80.10%** | 75.28% | **78.07%** | 80.05% | **0.9591** | Tuned Baseline |
| **K-Nearest Neighbors (KNN)** | **79.59%** | 74.68% | **76.38%** | 79.50% | **0.9517** | Tuned Baseline |
| **Multinomial Logistic Regression** | **78.57%** | 74.22% | **76.39%** | 78.57% | **0.9451** | Tuned Baseline |

---

## 🚀 Quickstart Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

### 2. Run Backend API Server
```bash
python backend/run.py
```
*API interactive documentation: `http://localhost:8000/docs`*

### 3. Run Frontend Web Application
```bash
cd frontend
npm run dev
```
*Web dashboard: `http://localhost:3000`*

### 4. Run System Verification Tests
```bash
python scripts/verify_system.py
```

---

## 📁 Repository Architecture

```text
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── main.py           # Application Entrypoint & CORS
│   │   ├── predictor.py      # Preprocessing Pipeline & Real-Time Inference
│   │   ├── schemas.py        # Pydantic Request/Response Models
│   │   └── routes/           # Predict, Models, Analytics, Health Routers
│   ├── tests/                # TestClient Integration Suite (10/10 Tests Passing)
│   └── run.py                # Standalone Server Launcher
├── data/
│   ├── raw/                  # smartphone_cleaned_v5.csv
│   └── processed/            # Cleaned data, train/test splits, numpy arrays
├── frontend/                 # React 19 + TypeScript + Tailwind Application
│   ├── src/
│   │   ├── components/       # Predictor, Benchmarking, Explainability, Analytics, About
│   │   ├── api.ts            # Typed Backend API Client & Device Presets
│   │   └── App.tsx           # Main Shell
│   └── vite.config.ts        # Vite + Tailwind + Proxy Configuration
├── ml/
│   ├── src/                  # Automated pipeline scripts (01 to 07)
│   ├── models/               # Serialized pipelines & champion models (.joblib)
│   └── outputs/              # Evaluation reports, JSONs, and publication figures
├── reports/
│   └── academic_project_report.md # Complete 10-page academic report & Viva guide
├── scripts/
│   └── verify_system.py      # Automated end-to-end health validation
├── requirements.txt
└── README.md
```

---

## 📄 Academic Project Report & Viva Voce
The complete 10-page academic lab report with mathematical derivations, confusion matrix breakdowns, and top 10 Viva Voce questions is available in [`reports/academic_project_report.md`](file:///c:/Users/wwa90/OneDrive/Desktop/MLProject/reports/academic_project_report.md).
