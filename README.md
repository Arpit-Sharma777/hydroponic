# Smart Hydroponic AI Monitoring System

End-to-end capstone project for hydroponics monitoring using IoT-style sensor inputs, machine learning risk detection, hard safety rules, and a real-time Streamlit dashboard.

## Project Overview

This repository contains three connected parts:

1. Data Science Notebook (`Hydroponics.ipynb`)
Trains and evaluates models for abnormal-condition detection from sensor signals.

2. Backend API (`backend/app.py`)
Serves predictions, applies safety rules, tracks history/statistics, and returns recommended actions.

3. Frontend Dashboard (`frontend/dashboard.py`)
Provides real-time monitoring, anomaly visualization, and operational controls.

## Repository Structure

```text
.
|-- Hydroponics.ipynb
|-- README.md
|-- requirements.txt
|-- backend/
|   |-- app.py
|   `-- API_DOCUMENTATION.md
|-- frontend/
|   `-- dashboard.py
|-- data/
|-- models/
`-- hardware/
		`-- esp32_code.ino
```

## Key Features

- Hybrid decision system: rule engine + ML probability scoring.
- Grace-period safety logic: emergency shutdown only after repeated critical readings.
- Real-time API-backed Streamlit dashboard with auto-refresh.
- Prediction history, analytics, and export support.
- Notebook workflow for training/evaluation and model artifact generation.

## Tech Stack

- Python
- Flask + Flask-CORS (backend API)
- Streamlit + Plotly (dashboard)
- scikit-learn, imbalanced-learn, TensorFlow (modeling experiments)
- pandas, numpy, matplotlib, seaborn (data analysis)
- joblib (model persistence)

## Installation

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the System

Open two terminals from the project root.

1. Start backend API:

```bash
cd backend
python app.py
```

2. Start Streamlit dashboard:

```bash
cd frontend
streamlit run dashboard.py
```

3. Open dashboard in browser:
- `http://localhost:8501`

## API Quick Reference

Base URL:
- `http://127.0.0.1:5000`

Main endpoints:
- `GET /` health check
- `POST /predict` run hybrid prediction
- `GET /history` prediction history
- `GET /stats` aggregate statistics
- `POST /clear` clear stored history

Full API details are documented in `backend/API_DOCUMENTATION.md`.

## Notebook Workflow

`Hydroponics.ipynb` includes:

- Data preprocessing and exploratory analysis
- Multiple model experiments (Random Forest, SVM, KNN, neural network)
- Balancing via SMOTE
- Evaluation metrics and visualization
- Model export using `joblib`

Expected output artifacts:
- `models/hydroponic_rf_model.pkl`
- `models/scaler.pkl`

These files are required by the backend at startup.

## Configuration Notes

- The backend currently runs with `debug=True` in `backend/app.py`; set to `False` for production.
- Notifications use `plyer` and may depend on host OS support.
- CORS is enabled for development convenience.

## Typical Data Payload

```json
{
	"pH": 5.7,
	"TDS": 1200,
	"water_level": 1.0,
	"DHT_temp": 24.0,
	"DHT_humidity": 75.0,
	"water_temp": 22.0
}
```

## Troubleshooting

- Backend says model files are missing:
Check that `.pkl` artifacts exist in `models/`.

- Dashboard cannot connect to backend:
Ensure `backend/app.py` is running on port `5000`.

- Package installation errors:
Use Python `3.10` or `3.11` for better compatibility with scientific stack versions.

## Project Goal

Deliver an explainable, practical monitoring system for precision hydroponics that combines rule-based safeguards with machine learning intelligence.
