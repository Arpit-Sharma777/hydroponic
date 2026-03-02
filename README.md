# Smart Hydroponic System - Enhanced Dashboard

## 🌟 Features

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

## 🚀 Getting Started

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Dashboard

1. Make sure the backend server is running:
```bash
cd ../backend
python app.py
```

2. Start the dashboard:
```bash
cd frontend
streamlit run dashboard.py
```

3. Access the dashboard at: http://localhost:8501

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

## 🌐 Backend Integration

The dashboard communicates with Flask backend at:
- **URL**: http://127.0.0.1:5000
- **Endpoint**: /predict
- **Method**: POST
- **Data Format**: JSON

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

---

**Built for Precision Agriculture** | AI + IoT Hybrid System
