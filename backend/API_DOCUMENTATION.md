# Smart Hydroponic AI Backend

Comprehensive API documentation for the Flask backend used by the Smart Hydroponic AI Monitoring System.

## 1. Overview

The backend combines:

- Rule-based safety validation for immediate hazard detection
- Machine learning probability scoring for anomaly detection
- Grace-period emergency logic to reduce false shutdowns
- Prediction history and system statistics endpoints

Base URL:
- `http://127.0.0.1:5000`

## 2. API Summary

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Service health and model availability |
| POST | `/predict` | Hybrid AI prediction and recommended action |
| GET | `/history` | Retrieve recent prediction records |
| GET | `/stats` | Get aggregate monitoring metrics |
| POST | `/clear` | Clear in-memory prediction history |

## 3. Data Contract

### 3.1 Required Sensor Fields

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

### 3.2 Input Validation Ranges

```python
{
  "pH": (0, 14),
  "TDS": (0, 5000),
  "water_level": (0, 10),
  "DHT_temp": (-20, 60),
  "DHT_humidity": (0, 100),
  "water_temp": (0, 50)
}
```

If a field is missing or out of range, the API returns `400`.

## 4. Endpoint Details

### 4.1 Health Check

`GET /`

Use this endpoint to verify the service is online and model artifacts are loaded.

Example response:

```json
{
  "status": "online",
  "service": "Smart Hydroponic AI Backend",
  "model_loaded": true,
  "timestamp": "2026-03-30T10:30:00",
  "version": "2.0"
}
```

### 4.2 Predict System Status

`POST /predict`

Executes hybrid inference flow:

1. Validate incoming sensor payload
2. Apply safety rule engine
3. Run scaled ML prediction
4. Resolve final status/action via decision logic
5. Update history and grace-period tracking

Example response:

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
  "timestamp": "2026-03-30T10:30:15",
  "sensor_data": {
    "pH": 5.7,
    "TDS": 1200,
    "water_level": 1.0,
    "DHT_temp": 24.0,
    "DHT_humidity": 75.0,
    "water_temp": 22.0
  }
}
```

### 4.3 Prediction History

`GET /history?limit=50`

Returns recent predictions from in-memory history (`MAX_HISTORY = 100`).

Query parameters:

- `limit` (optional, integer): number of records to return, capped at 100.

### 4.4 System Statistics

`GET /stats`

Returns aggregate metrics such as total predictions, normal vs abnormal counts, average risk score, and decision source distribution.

### 4.5 Clear History

`POST /clear`

Clears in-memory prediction history and resets returned history dataset.

## 5. Decision Logic Reference

### 5.1 Decision Source Values

- `RULE_ENGINE`: hard safety rule triggered
- `ML_MODEL`: ML detected anomaly above threshold
- `SYSTEM_NORMAL`: no anomaly detected

### 5.2 Severity Values

- `NORMAL`
- `WARNING`
- `CRITICAL`

### 5.3 Recommended Action Values

- `NONE`
- `ACTIVATE_CORRECTION`
- `EMERGENCY_SHUTDOWN`

## 6. Grace-Period Safety Mechanism

The backend uses a consecutive-critical counter to avoid false emergency shutdowns.

Behavior:

1. First critical reading: counter = 1, action = `ACTIVATE_CORRECTION`
2. Second consecutive critical reading: counter = 2, action = `EMERGENCY_SHUTDOWN`
3. Any non-critical reading: counter resets to `0`

Grace threshold:

- `CRITICAL_GRACE_THRESHOLD = 2`

### 6.1 Critical Conditions

| Parameter | Critical Range |
|---|---|
| pH | `< 4.5` or `> 7.5` |
| TDS | `< 500` or `> 2000` |
| water_level | `<= 0` |
| DHT_temp | `< 10` or `> 40` |
| DHT_humidity | `< 40` or `> 90` |
| water_temp | `< 15` or `> 35` |

### 6.2 Warning Conditions

| Parameter | Warning Range |
|---|---|
| pH | `< 5.0` or `> 7.0` |
| TDS | `< 700` or `> 1800` |
| water_level | `< 0.3` |
| DHT_temp | `< 15` or `> 30` |
| DHT_humidity | `< 50` or `> 85` |
| water_temp | `< 18` or `> 28` |

## 7. ML Configuration

- Model: Random Forest classifier
- Features: `pH`, `TDS`, `water_level`, `DHT_temp`, `DHT_humidity`, `water_temp`
- Probability threshold: `0.30`
- Preprocessing: `StandardScaler`
- Required files:
  - `../models/hydroponic_rf_model.pkl`
  - `../models/scaler.pkl`

## 8. Error Handling

Standard error payload:

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

Common status codes:

- `200`: success
- `400`: validation or request payload error
- `404`: endpoint not found
- `500`: internal server/model/prediction failure

## 9. Logging and Runtime Notes

- Request outcomes and warnings are logged using Python `logging`.
- CORS is enabled for frontend integration.
- Desktop notifications are sent on status transitions (`NORMAL` <-> `ABNORMAL`) using `plyer`.

## 10. Example Requests

### 10.1 cURL

Health check:

```bash
curl http://localhost:5000/
```

Prediction:

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

Statistics:

```bash
curl http://localhost:5000/stats
```

### 10.2 Python

```python
import requests

payload = {
    "pH": 5.7,
    "TDS": 1200,
    "water_level": 1.0,
    "DHT_temp": 24.0,
    "DHT_humidity": 75.0,
    "water_temp": 22.0,
}

health = requests.get("http://localhost:5000/")
print(health.status_code, health.json())

prediction = requests.post("http://localhost:5000/predict", json=payload)
print(prediction.status_code, prediction.json())
```

## 11. Production Recommendations

- Set `debug=False`
- Restrict CORS origins
- Add authentication/authorization
- Add rate limiting
- Run behind HTTPS/reverse proxy

---

Version: 2.0
