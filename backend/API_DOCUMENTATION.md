# Smart Hydroponic AI Backend - API Documentation

## 🚀 Overview

Enhanced Flask backend with hybrid AI decision-making system combining rule-based safety checks and machine learning predictions.

## 📋 API Endpoints

### 1. Health Check
**GET** `/`

Check if the backend server is running and models are loaded.

**Response:**
```json
{
  "status": "online",
  "service": "Smart Hydroponic AI Backend",
  "model_loaded": true,
  "timestamp": "2026-03-02T10:30:00",
  "version": "2.0"
}
```

---

### 2. Predict System Status
**POST** `/predict`

Analyze sensor data and predict system status using hybrid AI.

**Request Body:**
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

**Response:**
```json
{
  "prediction": 0,
  "status": "NORMAL",
  "abnormal_probability": 0.23,
  "confidence": 0.77,
  "decision_source": "SYSTEM_NORMAL",
  "reason": "All parameters within safe limits",
  "recommended_action": "NONE",
  "severity": "NORMAL",
  "consecutive_critical_count": 0,
  "grace_threshold": 2,
  "action_status": "NORMAL",
  "timestamp": "2026-03-02T10:30:15",
  "sensor_data": { ... }
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid input data
- `500` - Internal server error

**Decision Sources:**
- `RULE_ENGINE` - Safety rules triggered
- `ML_MODEL` - AI pattern detection
- `SYSTEM_NORMAL` - All systems normal

**Actions:**
- `NONE` - No action required, all systems normal
- `ACTIVATE_CORRECTION` - Activate relay correction for parameter adjustment or first critical reading (grace period active)
- `EMERGENCY_SHUTDOWN` - Critical condition confirmed (2+ consecutive critical readings)

**Grace Period Rule:**
- **Consecutive Critical Count**: Tracks how many consecutive critical readings occurred
- **Grace Threshold**: Set to 2 readings
- **Behavior**: Emergency shutdown only triggers after 2 consecutive critical readings (prevents false alarms)
- **Reset**: Counter resets to 0 immediately when a non-critical reading occurs
- **Action Status**: Shows current grace state (e.g., "CRITICAL_ALERT_1/2" means first of two required readings)

**Severity Levels:**
- `NORMAL` - All parameters safe
- `WARNING` - Parameters outside optimal range
- `CRITICAL` - Immediate action required

---

### 3. Get Prediction History
**GET** `/history?limit=50`

Retrieve historical predictions for analytics.

**Query Parameters:**
- `limit` (optional) - Number of records to return (default: 50, max: 100)

**Response:**
```json
{
  "total_records": 87,
  "returned_records": 50,
  "history": [
    {
      "prediction": 0,
      "status": "NORMAL",
      "abnormal_probability": 0.23,
      "timestamp": "2026-03-02T10:30:15",
      ...
    }
  ]
}
```

---

### 4. Get System Statistics
**GET** `/stats`

Get aggregate statistics about system performance.

**Response:**
```json
{
  "total_predictions": 150,
  "abnormal_count": 12,
  "normal_count": 138,
  "abnormal_percentage": 8.0,
  "average_abnormal_probability": 0.2156,
  "decision_sources": {
    "SYSTEM_NORMAL": 138,
    "ML_MODEL": 8,
    "RULE_ENGINE": 4
  },
  "latest_prediction": { ... }
}
```

---

### 5. Clear History
**POST** `/clear`

Clear all stored prediction history.

**Response:**
```json
{
  "message": "History cleared successfully"
}
```

---

## 🛡️ Safety Rule Engine with Grace Period

The system uses multi-level safety checks with a **smart grace period** to prevent false alarms:

### How Grace Period Works
1. **First Critical Reading**: `consecutive_critical_count` = 1 → `ACTIVATE_CORRECTION` (warning mode)
2. **Second Consecutive Critical**: `consecutive_critical_count` = 2 → `EMERGENCY_SHUTDOWN` (confirmed critical)
3. **Non-Critical Reading at Any Point**: Counter resets to 0, system returns to normal operations

### Critical Conditions (Grace Period = 2 Readings)
| Parameter | Critical Range | 1st Reading | 2nd Reading |
|-----------|---------------|-------------|-------------|
| pH | < 4.5 or > 7.5 | Correction Mode | SHUTDOWN |
| TDS | < 500 or > 2000 ppm | Correction Mode | SHUTDOWN |
| Water Level | ≤ 0 | Correction Mode | SHUTDOWN |
| Air Temp | < 10°C or > 40°C | Correction Mode | SHUTDOWN |
| Humidity | < 40% or > 90% | Correction Mode | SHUTDOWN |
| Water Temp | < 15°C or > 35°C | Correction Mode | SHUTDOWN |

**Benefits:**
- Prevents false emergency shutdowns from temporary sensor readings
- Gives system time to correct minor fluctuations
- Still protects system with confirmed hazard detection
- Automatic reset on safe readings

### Warning Conditions (Immediate Correction - No Grace Period)
| Parameter | Warning Range | Action |
|-----------|--------------|---------|
| pH | < 5.0 or > 7.0 | ACTIVATE_CORRECTION |
| TDS | < 700 or > 1800 ppm | ACTIVATE_CORRECTION |
| Water Level | < 0.3 | ACTIVATE_CORRECTION |
| Air Temp | < 15°C or > 30°C | ACTIVATE_CORRECTION |
| Humidity | < 50% or > 85% | ACTIVATE_CORRECTION |
| Water Temp | < 18°C or > 28°C | ACTIVATE_CORRECTION |

---

## 🤖 Machine Learning Model

- **Algorithm**: Random Forest Classifier
- **Features**: 6 sensor parameters (pH, TDS, water_level, DHT_temp, DHT_humidity, water_temp)
- **Threshold**: 0.30 (30% probability)
- **Preprocessing**: StandardScaler normalization

---

## 📊 Input Validation

All inputs are validated against physical sensor limits:

```python
{
  "pH": (0, 14),           # Standard pH scale
  "TDS": (0, 5000),        # Parts per million
  "water_level": (0, 10),  # Tank level units
  "DHT_temp": (-20, 60),   # Celsius
  "DHT_humidity": (0, 100), # Percentage
  "water_temp": (0, 50)    # Celsius
}
```

---

## 🔧 Configuration

### Environment Variables (Optional)
```bash
FLASK_ENV=production
THRESHOLD=0.30
MAX_HISTORY=100
```

### Model Files Required
- `../models/hydroponic_rf_model.pkl` - Trained Random Forest model
- `../models/scaler.pkl` - Feature scaler

---

## 📝 Logging

The backend logs all activities:

```
2026-03-02 10:30:00 - INFO - ✅ ML Models loaded successfully
2026-03-02 10:30:15 - INFO - Prediction: NORMAL | Prob: 0.23 | Source: SYSTEM_NORMAL
2026-03-02 10:35:20 - WARNING - Invalid input: pH value 15 outside valid range [0, 14]
2026-03-02 10:40:00 - INFO - Prediction: ABNORMAL | Prob: 0.87 | Source: RULE_ENGINE
```

---

## 🚨 Error Handling

### Error Response Format
```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

### Common Errors
- `400` - Missing required fields, invalid values
- `404` - Endpoint not found
- `500` - Model loading error, prediction failure

---

## 🔄 CORS Configuration

CORS is enabled for all origins to allow frontend communication.

---

## 📈 New Features (v2.0+)

✅ **Input Validation** - Comprehensive data validation  
✅ **Enhanced Safety Rules** - Multi-level severity detection  
✅ **Grace Period System** - 2-reading confirmation before emergency shutdown  
✅ **History Tracking** - Store up to 100 predictions  
✅ **Statistics API** - Analytics and performance metrics  
✅ **Confidence Scoring** - Decision confidence levels  
✅ **Detailed Logging** - Complete audit trail with grace state tracking  
✅ **Error Handling** - Robust error management  
✅ **CORS Support** - Cross-origin requests enabled  
✅ **Health Check** - Service monitoring endpoint  
✅ **Action Status Tracking** - Real-time grace period state visibility  

---

## 🧪 Testing the API

### Using cURL

**Health Check:**
```bash
curl http://localhost:5000/
```

**Prediction:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pH": 5.7,
    "TDS": 1200,
    "water_level": 1.0,
    "DHT_temp": 24.0,
    "DHT_humidity": 75.0,
    "water_temp": 22.0
  }'
```

**Get Statistics:**
```bash
curl http://localhost:5000/stats
```

### Using Python

```python
import requests

# Health check
response = requests.get("http://localhost:5000/")
print(response.json())

# Prediction
data = {
    "pH": 5.7,
    "TDS": 1200,
    "water_level": 1.0,
    "DHT_temp": 24.0,
    "DHT_humidity": 75.0,
    "water_temp": 22.0
}
response = requests.post("http://localhost:5000/predict", json=data)
print(response.json())
```

---

## 🔐 Security Considerations

For production deployment:
- Disable debug mode (`debug=False`)
- Add authentication/authorization
- Implement rate limiting
- Use HTTPS
- Validate CORS origins
- Add request logging

---

## 📦 Installation

```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Server will start on:** `http://0.0.0.0:5000`

---

**Version:** 2.0  
**Last Updated:** March 2, 2026  
**Author:** Capstone Project Team
