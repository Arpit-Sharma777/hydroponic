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

## 🔧 Technical Stack

- **Frontend Framework**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas
- **HTTP Requests**: Requests library
- **Auto-Refresh**: streamlit-autorefresh

## 📝 Notes

- Dashboard maintains last 100 sensor readings
- Data can be exported in CSV or JSON format
- Backend must be running for predictions
- System statistics persist during session


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

## key Features

### Real-Time Monitoring
- **Live Sensor Data**: Monitor pH, TDS, water level, temperature, humidity in real-time
- **Auto-Refresh**: Dashboard automatically updates every 5 seconds
- **KPI Metrics**: Quick overview of critical parameters at a glance

### AI-Powered Intelligence
- **Abnormality Detection**: Machine learning model analyzes system status
- **Risk Assessment**: Visual gauge showing abnormality probability
- **Automated Alerts**: Instant notifications for abnormal conditions
- **Smart Recommendations**: AI-driven corrective action suggestions
- **Grace Period Protection**: Requires 2 consecutive critical readings before emergency shutdown (prevents false alarms)

### Advanced Analytics
- **Time Series Visualization**: Track parameter trends over time
- **Distribution Analysis**: Statistical analysis of sensor readings
- **Correlation Matrix**: Understand relationships between parameters
- **Alert History**: Complete log of all system events

### Customizable Thresholds
- Configure optimal ranges for all parameters
- Real-time threshold violation detection
- Color-coded status indicators

### Data Management
- **Export Capabilities**: Download data in CSV or JSON format
- **Historical Records**: Maintains up to 100 recent readings
- **Statistics Tracking**: System health metrics and performance indicators

## Tech Stack

- Python
- Flask + Flask-CORS (backend API)
- Streamlit + Plotly (dashboard)
- scikit-learn, imbalanced-learn, TensorFlow (modeling experiments)
- pandas, numpy, matplotlib, seaborn (data analysis)
- joblib (model persistence)

## Notebook Training and Analysis

The notebook was used to train multiple ML models, evaluate them, and select the final deployment model.

### Training and Evaluation Workflow

1. Data preprocessing and feature scaling
2. Class imbalance handling using SMOTE
3. Multi-model training and comparison
4. Evaluation with accuracy, precision, recall, F1-score, and confusion matrix
5. Threshold experimentation for improved abnormal-class detection
6. Final model export with joblib

### Models Evaluated

- Random Forest
- Random Forest with SMOTE
- Tuned Random Forest
- SVM
- SVM with adjusted threshold
- KNN (including multiple k values)
- ANN (TensorFlow/Keras)

### Analysis Graphs Included in the Notebook

- Class Distribution (countplot)
- Correlation Matrix (heatmap)
- Confusion Matrix - Random Forest
- Feature Importance - Random Forest
- Confusion Matrix - Random Forest (SMOTE)
- Confusion Matrix - Tuned RF
- Confusion Matrix - Adjusted Threshold
- Confusion Matrix - SVM
- Confusion Matrix - SVM (Adjusted Threshold 0.6)
- Confusion Matrix - KNN
- Confusion Matrix - ANN

### Final Model Selection

The final production model selected for backend inference is Random Forest.

Notebook experiments showed that imbalance handling (SMOTE) and threshold adjustment improved abnormal-class detection behavior. A key notebook observation states that abnormal-class recall improved from 0% to 27% after applying SMOTE and threshold adjustment.

### Exported Artifacts from Notebook

- models/hydroponic_rf_model.pkl
- models/scaler.pkl

These files are required by the backend application at startup.

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

## 📊 Dashboard Sections

### 1. Sensor Input Panel
- **Water Quality Tab**: pH, TDS, Water Temperature
- **Climate Tab**: Air Temperature, Humidity
- **Levels Tab**: Water Level monitoring

### 2. AI Intelligence Center
- Real-time status display
- Abnormality risk gauge
- Relay control status
- AI decision reasoning

### 3. Analytics Dashboard
- **Time Series**: Multi-parameter trend analysis
- **Parameter Analysis**: Distribution and range visualization
- **Correlation Matrix**: Heat map and scatter plots
- **Alert History**: Timeline of system events

### 4. Configuration Sidebar
- Backend connection status
- Adjustable sensor thresholds
- System statistics
- Data management controls

## 🎨 UI Enhancements

- **Gradient Styling**: Modern dark theme with vibrant accents
- **Interactive Charts**: Powered by Plotly for rich visualizations
- **Responsive Layout**: Optimized for different screen sizes
- **Status Animations**: Pulsing alerts for better visibility
- **Professional Cards**: Clean, organized information presentation

## 📈 Data Visualization

The dashboard includes multiple visualization types:
- Line charts for trend analysis
- Gauge charts for risk assessment
- Histograms for distribution analysis
- Box plots for range visualization
- Heat maps for correlation analysis
- Scatter plots for multi-parameter relationships

## ⚙️ Configuration

### Threshold Settings (Sidebar)
- **pH Range**: 5.5 - 6.5 (adjustable)
- **TDS Range**: 800 - 1500 ppm (adjustable)
- **Temperature Range**: 18 - 28°C (adjustable)

### Auto-Refresh
- Default: 5 seconds
- Can be modified in the code (st_autorefresh interval)

## 🛡️ Safety Features - Grace Period System

### How It Works
The backend implements an intelligent **grace period** mechanism to prevent false emergency shutdowns:

**Critical Reading Detection:**
1. **First Critical Reading** → System activates **CORRECTION MODE** (first warning)
2. **Second Consecutive Critical Reading** → System triggers **EMERGENCY SHUTDOWN** (confirmed hazard)
3. **Non-Critical Reading at Any Point** → Grace counter resets to 0 (false alarm avoided)

### Example Scenario
```
Reading 1: pH = 2.7 (CRITICAL) → ACTIVATE_CORRECTION (1/2 threshold)
Reading 2: pH = 2.8 (CRITICAL) → EMERGENCY_SHUTDOWN (confirmed)

OR

Reading 1: pH = 2.7 (CRITICAL) → ACTIVATE_CORRECTION (1/2 threshold)
Reading 2: pH = 5.7 (NORMAL)  → System recovers, counter resets to 0
```

### Benefits
- 🛡️ Eliminates false shutdowns from sensor noise
- ⚡ Gives system time to auto-correct minor fluctuations
- 🎯 Maintains safety with confirmed hazard detection
- 📊 Tracks grace state in AI Intelligence Center

## 🔧 Technical Stack

- **Frontend Framework**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas
- **HTTP Requests**: Requests library
- **Auto-Refresh**: streamlit-autorefresh

## 📝 Notes

- Dashboard maintains last 100 sensor readings
- Data can be exported in CSV or JSON format
- Backend must be running for predictions
- System statistics persist during session


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

## 💡 Tips

1. Use the sidebar to monitor backend connection status
2. Adjust thresholds based on your crop requirements
3. Export data regularly for historical analysis
4. Monitor the Alert History tab for patterns
5. Use correlation analysis to optimize parameters


## 🎯 Capstone Project Features

This dashboard demonstrates:
- ✅ IoT Integration
- ✅ Real-time Data Processing
- ✅ Machine Learning Integration
- ✅ Advanced Data Visualization
- ✅ User-Friendly Interface
- ✅ Automated Monitoring & Control
- ✅ Intelligent Grace Period Safety System
- ✅ Data Export & Analysis
- ✅ Professional UI/UX Design

## Project Goal

Deliver an explainable, practical monitoring system for precision hydroponics that combines rule-based safeguards with machine learning intelligence.
