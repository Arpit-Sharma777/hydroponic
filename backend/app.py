from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from datetime import datetime
import logging
from plyer import notification
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load model and scaler
try:
    model = joblib.load("../models/hydroponic_rf_model.pkl")
    scaler = joblib.load("../models/scaler.pkl")
    logger.info("✅ ML Models loaded successfully")
except Exception as e:
    logger.error(f"❌ Error loading models: {e}")
    model = None
    scaler = None

# ML decision threshold
THRESHOLD = 0.30

# Store recent predictions for analytics
prediction_history = []
MAX_HISTORY = 100

# Grace rule: Track consecutive critical readings
consecutive_critical_count = 0
CRITICAL_GRACE_THRESHOLD = 2  # Require 2 consecutive critical readings before emergency shutdown
latest_data = None
last_status = None


def safety_rule_engine(data):
    """
    Hard safety rules for extreme dangerous conditions.
    Returns (is_abnormal, reason, severity_level)
    """
    issues = []
    
    # Critical checks with severity levels
    if data["pH"] < 4.5 or data["pH"] > 7.5:
        issues.append(("Critical pH Level - Plant damage imminent", "CRITICAL"))
    elif data["pH"] < 5.0 or data["pH"] > 7.0:
        issues.append(("pH approaching dangerous levels", "WARNING"))

    if data["TDS"] > 2000:
        issues.append(("Critical Nutrient Level - Too high, toxicity risk", "CRITICAL"))
    elif data["TDS"] < 500:
        issues.append(("Critical Nutrient Level - Too low, deficiency risk", "CRITICAL"))
    elif data["TDS"] < 700 or data["TDS"] > 1800:
        issues.append(("Nutrient level outside optimal range", "WARNING"))

    if data["water_level"] <= 0:
        issues.append(("Water Tank Empty - Immediate refill required", "CRITICAL"))
    elif data["water_level"] < 0.3:
        issues.append(("Water level critically low", "WARNING"))

    if data["DHT_temp"] > 40:
        issues.append(("Air Temperature Critical - Heat stress risk", "CRITICAL"))
    elif data["DHT_temp"] < 10:
        issues.append(("Air Temperature Critical - Cold damage risk", "CRITICAL"))
    elif data["DHT_temp"] > 30 or data["DHT_temp"] < 15:
        issues.append(("Temperature outside optimal range", "WARNING"))

    if data["DHT_humidity"] > 90:
        issues.append(("Humidity Critical - Fungal disease risk", "CRITICAL"))
    elif data["DHT_humidity"] < 40:
        issues.append(("Humidity Critical - Water stress risk", "CRITICAL"))
    elif data["DHT_humidity"] > 85 or data["DHT_humidity"] < 50:
        issues.append(("Humidity outside optimal range", "WARNING"))

    if data["water_temp"] > 35:
        issues.append(("Water Temperature Critical - Root damage risk", "CRITICAL"))
    elif data["water_temp"] < 15:
        issues.append(("Water Temperature Critical - Nutrient uptake reduced", "CRITICAL"))
    elif data["water_temp"] > 28 or data["water_temp"] < 18:
        issues.append(("Water temperature outside optimal range", "WARNING"))

    if issues:
        # Return most severe issue
        critical_issues = [i for i in issues if i[1] == "CRITICAL"]
        if critical_issues:
            return True, critical_issues[0][0], "CRITICAL"
        else:
            return True, issues[0][0], "WARNING"
    
    return False, None, None


def validate_input(data):
    """
    Validate incoming sensor data
    Returns (is_valid, error_message)
    """
    required_fields = ["pH", "TDS", "water_level", "DHT_temp", "DHT_humidity", "water_temp"]
    
    # Check all required fields present
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate ranges (physical sensor limits)
    validations = {
        "pH": (0, 14),
        "TDS": (0, 5000),
        "water_level": (0, 10),
        "DHT_temp": (-20, 60),
        "DHT_humidity": (0, 100),
        "water_temp": (0, 50)
    }
    
    for field, (min_val, max_val) in validations.items():
        try:
            value = float(data[field])
            if not (min_val <= value <= max_val):
                return False, f"{field} value {value} outside valid range [{min_val}, {max_val}]"
        except (ValueError, TypeError):
            return False, f"{field} must be a number"
    
    return True, None

def send_notification(title, message):
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=5
        )
    except:
        logger.warning("Notification failed")

@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint for frontend monitoring"""
    return jsonify({
        "status": "online",
        "service": "Smart Hydroponic AI Backend",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat(),
        "version": "2.0"
    }), 200


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        global latest_data
        latest_data = data
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # 1️⃣ Input Validation
        is_valid, error_msg = validate_input(data)
        if not is_valid:
            logger.warning(f"Invalid input: {error_msg}")
            return jsonify({"error": error_msg}), 400
        
        # 2️⃣ Safety Rule Check
        rule_triggered, rule_reason, severity = safety_rule_engine(data)

        # 3️⃣ Prepare feature array
        features = np.array([[
            data["pH"],
            data["TDS"],
            data["water_level"],
            data["DHT_temp"],
            data["DHT_humidity"],
            data["water_temp"]
        ]])

        features_scaled = scaler.transform(features)

        # 4️⃣ ML Prediction
        prob = model.predict_proba(features_scaled)[0][1]
        ml_prediction = int(prob > THRESHOLD)

        # 5️⃣ Final Decision Logic (Hybrid AI)
        if rule_triggered:
            final_prediction = 1
            decision_source = "RULE_ENGINE"
            reason = rule_reason
            confidence = 1.0 if severity == "CRITICAL" else 0.85
        elif ml_prediction == 1:
            final_prediction = 1
            decision_source = "ML_MODEL"
            reason = "AI detected anomalous pattern in sensor data"
            confidence = float(prob)
        else:
            final_prediction = 0
            decision_source = "SYSTEM_NORMAL"
            reason = "All parameters within safe limits"
            confidence = float(1 - prob)

        # 6️⃣ Automation Action (with Grace Rule)
        global consecutive_critical_count
        
        if severity == "CRITICAL":
            consecutive_critical_count += 1
            # Only trigger emergency after meeting grace threshold
            if consecutive_critical_count >= CRITICAL_GRACE_THRESHOLD:
                action = "EMERGENCY_SHUTDOWN"
                action_status = "SHUTDOWN_TRIGGERED"
            else:
                action = "ACTIVATE_CORRECTION"
                action_status = f"CRITICAL_ALERT_{consecutive_critical_count}/{CRITICAL_GRACE_THRESHOLD}"
        else:
            # Reset counter on non-critical reading
            if consecutive_critical_count > 0:
                logger.warning(f"⚠️ Critical condition cleared - Grace counter reset (was at {consecutive_critical_count})")
            consecutive_critical_count = 0
            if final_prediction == 1:
                action = "ACTIVATE_CORRECTION"
                action_status = "WARNING_MODE"
            else:
                action = "NONE"
                action_status = "NORMAL_OPERATION"

        # 7️⃣ Build response
        response = {
            "prediction": final_prediction,
            "status": "ABNORMAL" if final_prediction == 1 else "NORMAL",
            "abnormal_probability": float(prob),
            "confidence": confidence,
            "decision_source": decision_source,
            "reason": reason,
            "recommended_action": action,
            "severity": severity if rule_triggered else "NORMAL",
            "consecutive_critical_count": consecutive_critical_count,
            "grace_threshold": CRITICAL_GRACE_THRESHOLD,
            "action_status": action_status if severity == "CRITICAL" else "NORMAL",
            "timestamp": datetime.now().isoformat(),
            "sensor_data": data
        }
        
        
        # 8️⃣ Store in history
        prediction_history.append(response)
        if len(prediction_history) > MAX_HISTORY:
            prediction_history.pop(0)
        
        # Log the prediction
        logger.info(f"Prediction: {response['status']} | Prob: {prob:.2f} | Source: {decision_source}")
        
        global last_status

        current_status = "ABNORMAL" if final_prediction == 1 else "NORMAL"

        if current_status != last_status:
            if current_status == "ABNORMAL":
                send_notification("🚨 Hydroponic Alert", reason)
            else:
                send_notification("✅ System Normal", "All parameters OK")

            last_status = current_status
 

        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


@app.route("/history", methods=["GET"])
def get_history():
    """Get prediction history for analytics"""
    try:
        limit = request.args.get('limit', 50, type=int)
        limit = min(limit, MAX_HISTORY)  # Cap at max history
        
        return jsonify({
            "total_records": len(prediction_history),
            "returned_records": min(limit, len(prediction_history)),
            "history": prediction_history[-limit:]
        }), 200
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/stats", methods=["GET"])
def get_statistics():
    """Get system statistics"""
    try:
        if not prediction_history:
            return jsonify({
                "message": "No predictions yet",
                "total_predictions": 0
            }), 200
        
        total = len(prediction_history)
        abnormal = sum(1 for p in prediction_history if p['status'] == 'ABNORMAL')
        normal = total - abnormal
        
        avg_prob = sum(p['abnormal_probability'] for p in prediction_history) / total
        
        decision_sources = {}
        for p in prediction_history:
            source = p['decision_source']
            decision_sources[source] = decision_sources.get(source, 0) + 1
        
        return jsonify({
            "total_predictions": total,
            "abnormal_count": abnormal,
            "normal_count": normal,
            "abnormal_percentage": round((abnormal / total) * 100, 2),
            "average_abnormal_probability": round(avg_prob, 4),
            "decision_sources": decision_sources,
            "latest_prediction": prediction_history[-1] if prediction_history else None
        }), 200
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/clear", methods=["POST"])
def clear_history():
    """Clear prediction history"""
    try:
        global prediction_history
        prediction_history = []
        logger.info("Prediction history cleared")
        return jsonify({"message": "History cleared successfully"}), 200
    except Exception as e:
        logger.error(f"Error clearing history: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500


def monitor_loop():
    global latest_data, last_status

    while True:
        if latest_data:
            try:
                rule_triggered, rule_reason, severity = safety_rule_engine(latest_data)

                features = np.array([[
                    latest_data["pH"],
                    latest_data["TDS"],
                    latest_data["water_level"],
                    latest_data["DHT_temp"],
                    latest_data["DHT_humidity"],
                    latest_data["water_temp"]
                ]])

                features_scaled = scaler.transform(features)
                prob = model.predict_proba(features_scaled)[0][1]

                ml_prediction = int(prob > THRESHOLD)

                if rule_triggered or ml_prediction == 1:
                    current_status = "ABNORMAL"
                    reason = rule_reason if rule_triggered else "ML anomaly detected"
                else:
                    current_status = "NORMAL"
                    reason = "System Normal"

                if current_status != last_status:
                    if current_status == "ABNORMAL":
                        send_notification("🚨 Hydroponic Alert", reason)
                    else:
                        send_notification("✅ System Normal", "All parameters OK")

                    last_status = current_status

            except Exception as e:
                logger.error(f"Monitoring error: {e}")

        time.sleep(5)

if __name__ == "__main__":
    logger.info("🌱 Starting Smart Hydroponic AI Backend Server...")
    logger.info(f"📊 ML Threshold: {THRESHOLD}")
    logger.info(f"📚 Max History Records: {MAX_HISTORY}")
    
    if model is None or scaler is None:
        logger.warning("⚠️ Models not loaded - predictions will fail!")
    
    thread = threading.Thread(target=monitor_loop)
    thread.daemon = True
    thread.start()
    app.run(host="0.0.0.0", port=5000, debug=True)