import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="AI-Powered Hydroponic System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Custom CSS for Professional Styling
# ---------------------------
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(0, 255, 170, 0.3);
    }
    .status-normal {
        background: rgba(0, 255, 0, 0.1);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00FF00;
        animation: pulse 2s infinite;
    }
    .status-abnormal {
        background: rgba(255, 0, 0, 0.1);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF0000;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    .sensor-card {
        background: rgba(255, 255, 255, 0.08);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(0, 255, 170, 0.2);
        margin-bottom: 15px;
    }
    h1, h2, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Auto Refresh Every 5 Sec
# ---------------------------
st_autorefresh(interval=5000, key="datarefresh")

# ---------------------------
# Header with Logo
# ---------------------------
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    st.markdown("""
        <h1 style='text-align:center; 
                   background: linear-gradient(90deg, #00FFAA, #00D4FF, #7B2FFF);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   font-size: 3em;
                   font-weight: bold;
                   margin-bottom: 0;'>
            🌱 Smart Hydroponic System
        </h1>
        <p style='text-align:center; color: #00FFAA; font-size: 1.2em; margin-top: 0;'>
            AI-Powered Agriculture Monitoring & Control
        </p>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------
# Session State for History & Alerts
# ---------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "alerts" not in st.session_state:
    st.session_state.alerts = []
if "total_analyses" not in st.session_state:
    st.session_state.total_analyses = 0
if "abnormal_count" not in st.session_state:
    st.session_state.abnormal_count = 0
if "latest_result" not in st.session_state:
    st.session_state.latest_result = None
if "current_sensors" not in st.session_state:
    st.session_state.current_sensors = {
        "pH": 5.7,
        "TDS": 1200.0,
        "water_level": 1.0,
        "DHT_temp": 24.0,
        "DHT_humidity": 75.0,
        "water_temp": 22.0
    }

# ---------------------------
# Sidebar - System Configuration
# ---------------------------
with st.sidebar:
    st.markdown("### ⚙️ System Configuration")
    st.markdown("---")
    
    # Backend Connection Status
    try:
        ping = requests.get("http://127.0.0.1:5000/", timeout=2)
        st.success("🟢 Backend Server: Online")
    except:
        st.error("🔴 Backend Server: Offline")
    
    st.markdown("---")
    st.markdown("### 📡 Sensor Thresholds")
    
    ph_min = st.slider("pH Min", 0.0, 7.0, 5.5, 0.1)
    ph_max = st.slider("pH Max", 7.0, 14.0, 6.5, 0.1)
    
    tds_min = st.slider("TDS Min (ppm)", 0, 2000, 800, 50)
    tds_max = st.slider("TDS Max (ppm)", 1000, 3000, 1500, 50)
    
    temp_min = st.slider("Temp Min (°C)", 0, 30, 18, 1)
    temp_max = st.slider("Temp Max (°C)", 20, 50, 28, 1)
    
    st.markdown("---")
    st.markdown("### 📊 Statistics")
    st.metric("Total Analyses", st.session_state.total_analyses)
    st.metric("Abnormal Events", st.session_state.abnormal_count)
    
    if st.session_state.total_analyses > 0:
        success_rate = ((st.session_state.total_analyses - st.session_state.abnormal_count) / 
                       st.session_state.total_analyses * 100)
        st.metric("System Health", f"{success_rate:.1f}%")
    
    st.markdown("---")
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.history = []
        st.session_state.alerts = []
        st.session_state.total_analyses = 0
        st.session_state.abnormal_count = 0
        st.rerun()

# ---------------------------
# Alert Banner
# ---------------------------
if st.session_state.alerts:
    latest_alert = st.session_state.alerts[-1]
    if latest_alert['type'] == 'ABNORMAL':
        st.error(f"⚠️ ALERT: {latest_alert['message']} | Time: {latest_alert['time']}")

# ---------------------------
# KPI Dashboard
# ---------------------------
st.markdown("### 📈 Real-Time System Metrics")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown("<div class='sensor-card'>", unsafe_allow_html=True)
    st.metric("🌡️ Temperature", "-- °C", delta=None)
    st.markdown("</div>", unsafe_allow_html=True)

with kpi2:
    st.markdown("<div class='sensor-card'>", unsafe_allow_html=True)
    st.metric("💧 pH Level", "--", delta=None)
    st.markdown("</div>", unsafe_allow_html=True)

with kpi3:
    st.markdown("<div class='sensor-card'>", unsafe_allow_html=True)
    st.metric("⚗️ TDS", "-- ppm", delta=None)
    st.markdown("</div>", unsafe_allow_html=True)

with kpi4:
    st.markdown("<div class='sensor-card'>", unsafe_allow_html=True)
    st.metric("💦 Water Level", "--", delta=None)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------
# Main Layout
# ---------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🎛️ Sensor Input Panel")
    st.markdown("<div class='sensor-card'>", unsafe_allow_html=True)
    
    # Organize inputs in tabs
    tab1, tab2, tab3 = st.tabs(["💧 Water Quality", "🌡️ Climate", "📊 Levels"])
    
    with tab1:
        col_ph, col_tds = st.columns(2)
        with col_ph:
            pH = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=5.7, step=0.1,
                                help="Optimal range: 5.5-6.5")
        with col_tds:
            TDS = st.number_input("TDS (ppm)", min_value=0.0, max_value=5000.0, value=1200.0, step=10.0,
                                 help="Total Dissolved Solids")
        
        water_temp = st.number_input("Water Temperature (°C)", min_value=0.0, max_value=50.0, 
                                     value=22.0, step=0.5, help="Optimal: 18-22°C")
    
    with tab2:
        col_temp, col_hum = st.columns(2)
        with col_temp:
            air_temp = st.number_input("Air Temperature (°C)", min_value=0.0, max_value=50.0, 
                                      value=24.0, step=0.5, help="Optimal: 20-25°C")
        with col_hum:
            humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, 
                                      value=75.0, step=1.0, help="Optimal: 60-80%")
    
    with tab3:
        water_level = st.number_input("Water Level", min_value=0.0, max_value=10.0, 
                                      value=1.0, step=0.1, help="Tank water level indicator")
    
    # Update current sensors in session state
    st.session_state.current_sensors = {
        "pH": pH,
        "TDS": TDS,
        "water_level": water_level,
        "DHT_temp": air_temp,
        "DHT_humidity": humidity,
        "water_temp": water_temp
    }
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Analyze Button with Enhanced Styling (Optional Manual Trigger)
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        analyze = st.button("🔍 ANALYZE NOW", use_container_width=True, type="primary")

with col2:
    st.markdown("### 🧠 AI Intelligence Center")
    st.markdown("<div class='sensor-card'>", unsafe_allow_html=True)

    status_box = st.empty()
    prob_box = st.empty()
    relay_box = st.empty()
    reason_box = st.empty()
    source_box = st.empty()
    action_box = st.empty()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Auto Prediction & Analysis (Always Run)
# ---------------------------
# Auto-analyze using current sensor values
data = st.session_state.current_sensors

try:
    # Auto-call API with current sensor values (Always execute)
    response = requests.post("http://127.0.0.1:5000/predict", json=data, timeout=5)
    result = response.json()
    
    # Store latest result in session state
    st.session_state.latest_result = result
    
    # Increment counter only on manual button click
    if analyze:
        st.session_state.total_analyses += 1

    status = result.get("status")
    probability = result.get("abnormal_probability", 0)
    reason = result.get("reason")
    source = result.get("decision_source")
    action = result.get("recommended_action")

    # Update KPI metrics with current sensor values
    kpi1.metric("🌡️ Temperature", f"{data['DHT_temp']:.1f} °C", 
               delta=f"{data['DHT_temp'] - temp_min:.1f}°C" if data['DHT_temp'] > temp_min else None)
    kpi2.metric("💧 pH Level", f"{data['pH']:.1f}", 
               delta="Optimal" if ph_min <= data['pH'] <= ph_max else "⚠️ Out of range",
               delta_color="normal" if ph_min <= data['pH'] <= ph_max else "inverse")
    kpi3.metric("⚗️ TDS", f"{data['TDS']:.0f} ppm",
               delta="Optimal" if tds_min <= data['TDS'] <= tds_max else "⚠️ Out of range",
               delta_color="normal" if tds_min <= data['TDS'] <= tds_max else "inverse")
    kpi4.metric("💦 Water Level", f"{data['water_level']:.1f}",
               delta="Good" if data['water_level'] > 0.5 else "⚠️ Low")

    # Save to history with timestamp (only on button click or every 5 refreshes)
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Add to history (limit updates to avoid too many records)
    if analyze or len(st.session_state.history) == 0 or st.session_state.total_analyses % 5 == 0:
        st.session_state.history.append({
            "Time": current_time,
            "pH": data['pH'],
            "TDS": data['TDS'],
            "Temp": data['DHT_temp'],
            "Humidity": data['DHT_humidity'],
            "Water Temp": data['water_temp'],
            "Probability": probability,
            "Status": status
        })
    
    # Keep only last 100 records
    if len(st.session_state.history) > 100:
        st.session_state.history = st.session_state.history[-100:]

    # Status Display with Enhanced Styling
    if status == "ABNORMAL" and analyze:
        st.session_state.abnormal_count += 1
    
    if status == "ABNORMAL":
        status_box.markdown(f"""
            <div class='status-abnormal'>
                <h2 style='color: #FF4444; text-align: center; margin: 0;'>
                    🚨 SYSTEM STATUS: ABNORMAL
                </h2>
                <p style='text-align: center; color: #FFB6B6; margin-top: 10px;'>
                    Immediate attention required!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Add alert (only on manual click to avoid spam)
        if analyze:
            st.session_state.alerts.append({
                'type': 'ABNORMAL',
                'message': reason,
                'time': current_time
            })
        
    else:
        status_box.markdown(f"""
            <div class='status-normal'>
                <h2 style='color: #00FF88; text-align: center; margin: 0;'>
                    ✅ SYSTEM STATUS: NORMAL
                </h2>
                <p style='text-align: center; color: #B6FFD6; margin-top: 10px;'>
                    All systems operating optimally
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Probability Gauge with Plotly
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=probability * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Abnormality Risk", 'font': {'size': 24, 'color': '#00FFAA'}},
        delta={'reference': 50, 'increasing': {'color': "red"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#00FFAA"},
            'bar': {'color': "#FF4444" if probability > 0.5 else "#00FF88"},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 2,
            'bordercolor': "#00FFAA",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(0, 255, 136, 0.3)'},
                {'range': [30, 70], 'color': 'rgba(255, 255, 0, 0.3)'},
                {'range': [70, 100], 'color': 'rgba(255, 68, 68, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "#00FFAA", 'family': "Arial"},
        height=300
    )
    
    prob_box.plotly_chart(fig_gauge, use_container_width=True)

    # Relay Status with Visual Indicator
    relay_col1, relay_col2 = relay_box.columns(2)
    if action == "ACTIVATE_CORRECTION":
        relay_col1.markdown("""
            <div style='background: rgba(255, 165, 0, 0.2); padding: 15px; 
                       border-radius: 10px; text-align: center; border: 2px solid #FFA500;'>
                <h3 style='color: #FFA500; margin: 0;'>⚙️ RELAY: ON</h3>
                <p style='color: #FFD700; margin: 5px 0 0 0;'>Correction Active</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        relay_col1.markdown("""
            <div style='background: rgba(0, 255, 136, 0.1); padding: 15px; 
                       border-radius: 10px; text-align: center; border: 2px solid #00FF88;'>
                <h3 style='color: #00FF88; margin: 0;'>⚙️ RELAY: OFF</h3>
                <p style='color: #B6FFD6; margin: 5px 0 0 0;'>Standby Mode</p>
            </div>
        """, unsafe_allow_html=True)

    # AI Decision Information
    reason_box.info(f"🔍 **Analysis:** {reason}")
    source_box.success(f"🧩 **Decision Source:** {source}")
    action_box.warning(f"💡 **Recommended Action:** {action.replace('_', ' ').title()}")

except requests.exceptions.ConnectionError:
    status_box.error("⚠️ **Backend Server Not Running**\n\nPlease start the Flask server:\n```bash\ncd backend\npython app.py\n```")
except requests.exceptions.Timeout:
    status_box.error("⏱️ **Request Timeout** - Server is taking too long to respond")
except Exception as e:
    status_box.error(f"❌ **Error:** {str(e)}")

# ---------------------------
# Advanced Visualizations
# ---------------------------
st.markdown("---")
st.markdown("### 📊 Advanced Analytics Dashboard")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    
    # Create tabs for different visualizations
    viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs(
        ["📈 Time Series", "🎯 Parameter Analysis", "📊 Correlation Matrix", "⚠️ Alert History"]
    )
    
    with viz_tab1:
        st.markdown("#### Live Sensor Trends")
        
        # Multi-line chart with Plotly
        fig_trends = go.Figure()
        
        fig_trends.add_trace(go.Scatter(
            x=df["Time"], y=df["pH"],
            mode='lines+markers',
            name='pH Level',
            line=dict(color='#00FFAA', width=2),
            marker=dict(size=6)
        ))
        
        fig_trends.add_trace(go.Scatter(
            x=df["Time"], y=df["TDS"]/100,  # Scale for visibility
            mode='lines+markers',
            name='TDS (x100 ppm)',
            line=dict(color='#FF6B6B', width=2),
            marker=dict(size=6),
            yaxis='y2'
        ))
        
        fig_trends.add_trace(go.Scatter(
            x=df["Time"], y=df["Temp"],
            mode='lines+markers',
            name='Temperature (°C)',
            line=dict(color='#FFD93D', width=2),
            marker=dict(size=6)
        ))
        
        fig_trends.update_layout(
            xaxis_title="Time",
            yaxis_title="pH / Temperature",
            yaxis2=dict(
                title="TDS (x100 ppm)",
                overlaying='y',
                side='right'
            ),
            hovermode='x unified',
            template='plotly_dark',
            paper_bgcolor="rgba(0,0,0,0.3)",
            plot_bgcolor="rgba(0,0,0,0.3)",
            font=dict(color='#00FFAA'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=400
        )
        
        st.plotly_chart(fig_trends, use_container_width=True)
        
        # Individual parameter cards
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            fig_ph = px.line(df, x="Time", y="pH", 
                            title="pH Level Monitoring",
                            markers=True)
            fig_ph.add_hline(y=ph_min, line_dash="dash", line_color="orange", 
                           annotation_text="Min Threshold")
            fig_ph.add_hline(y=ph_max, line_dash="dash", line_color="orange", 
                           annotation_text="Max Threshold")
            fig_ph.update_layout(template='plotly_dark', paper_bgcolor="rgba(0,0,0,0.3)",
                               plot_bgcolor="rgba(0,0,0,0.3)", font=dict(color='#00FFAA'))
            st.plotly_chart(fig_ph, use_container_width=True)
        
        with col_chart2:
            fig_tds = px.line(df, x="Time", y="TDS", 
                             title="TDS Monitoring (ppm)",
                             markers=True)
            fig_tds.add_hline(y=tds_min, line_dash="dash", line_color="orange",
                            annotation_text="Min Threshold")
            fig_tds.add_hline(y=tds_max, line_dash="dash", line_color="orange",
                            annotation_text="Max Threshold")
            fig_tds.update_layout(template='plotly_dark', paper_bgcolor="rgba(0,0,0,0.3)",
                                plot_bgcolor="rgba(0,0,0,0.3)", font=dict(color='#00FFAA'))
            st.plotly_chart(fig_tds, use_container_width=True)
    
    with viz_tab2:
        st.markdown("#### Parameter Distribution Analysis")
        
        param_col1, param_col2 = st.columns(2)
        
        with param_col1:
            # Histogram for pH
            fig_hist_ph = px.histogram(df, x="pH", nbins=20,
                                      title="pH Distribution",
                                      color_discrete_sequence=['#00FFAA'])
            fig_hist_ph.update_layout(template='plotly_dark', 
                                     paper_bgcolor="rgba(0,0,0,0.3)",
                                     plot_bgcolor="rgba(0,0,0,0.3)", 
                                     font=dict(color='#00FFAA'))
            st.plotly_chart(fig_hist_ph, use_container_width=True)
            
            # Box plot for Temperature
            fig_box_temp = px.box(df, y="Temp",
                                 title="Temperature Range",
                                 color_discrete_sequence=['#FFD93D'])
            fig_box_temp.update_layout(template='plotly_dark',
                                      paper_bgcolor="rgba(0,0,0,0.3)",
                                      plot_bgcolor="rgba(0,0,0,0.3)",
                                      font=dict(color='#00FFAA'))
            st.plotly_chart(fig_box_temp, use_container_width=True)
        
        with param_col2:
            # Histogram for TDS
            fig_hist_tds = px.histogram(df, x="TDS", nbins=20,
                                       title="TDS Distribution",
                                       color_discrete_sequence=['#FF6B6B'])
            fig_hist_tds.update_layout(template='plotly_dark',
                                      paper_bgcolor="rgba(0,0,0,0.3)",
                                      plot_bgcolor="rgba(0,0,0,0.3)",
                                      font=dict(color='#00FFAA'))
            st.plotly_chart(fig_hist_tds, use_container_width=True)
            
            # Humidity box plot
            fig_box_hum = px.box(df, y="Humidity",
                                title="Humidity Range",
                                color_discrete_sequence=['#6BCF7F'])
            fig_box_hum.update_layout(template='plotly_dark',
                                     paper_bgcolor="rgba(0,0,0,0.3)",
                                     plot_bgcolor="rgba(0,0,0,0.3)",
                                     font=dict(color='#00FFAA'))
            st.plotly_chart(fig_box_hum, use_container_width=True)
    
    with viz_tab3:
        st.markdown("#### Parameter Correlation Analysis")
        
        # Correlation heatmap
        numeric_df = df[['pH', 'TDS', 'Temp', 'Humidity', 'Water Temp', 'Probability']]
        correlation = numeric_df.corr()
        
        fig_corr = px.imshow(correlation,
                            text_auto=True,
                            aspect="auto",
                            color_continuous_scale='RdYlGn',
                            title="Sensor Parameter Correlations")
        fig_corr.update_layout(template='plotly_dark',
                              paper_bgcolor="rgba(0,0,0,0.3)",
                              plot_bgcolor="rgba(0,0,0,0.3)",
                              font=dict(color='#00FFAA'),
                              height=500)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Scatter matrix
        fig_scatter = px.scatter_matrix(numeric_df,
                                       dimensions=['pH', 'TDS', 'Temp', 'Humidity'],
                                       color='Probability',
                                       title="Multi-Parameter Relationships",
                                       color_continuous_scale='Viridis')
        fig_scatter.update_layout(template='plotly_dark',
                                 paper_bgcolor="rgba(0,0,0,0.3)",
                                 plot_bgcolor="rgba(0,0,0,0.3)",
                                 font=dict(color='#00FFAA'),
                                 height=700)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with viz_tab4:
        st.markdown("#### System Status Timeline")
        
        # Status timeline
        df['Status_Color'] = df['Status'].map({'NORMAL': 'green', 'ABNORMAL': 'red'})
        
        fig_status = px.scatter(df, x="Time", y="Probability",
                               color="Status",
                               size="Probability",
                               color_discrete_map={'NORMAL': '#00FF88', 'ABNORMAL': '#FF4444'},
                               title="Abnormality Detection Timeline",
                               hover_data=['pH', 'TDS', 'Temp'])
        fig_status.add_hline(y=0.5, line_dash="dash", line_color="yellow",
                           annotation_text="Critical Threshold (50%)")
        fig_status.update_layout(template='plotly_dark',
                                paper_bgcolor="rgba(0,0,0,0.3)",
                                plot_bgcolor="rgba(0,0,0,0.3)",
                                font=dict(color='#00FFAA'),
                                height=400)
        st.plotly_chart(fig_status, use_container_width=True)
        
        # Alert Table
        if st.session_state.alerts:
            st.markdown("#### Recent Alerts")
            alerts_df = pd.DataFrame(st.session_state.alerts[-10:])  # Last 10 alerts
            st.dataframe(alerts_df, use_container_width=True, hide_index=True)
        else:
            st.info("No alerts recorded yet")
    
    # Data Export
    st.markdown("---")
    col_export1, col_export2, col_export3 = st.columns([2, 1, 1])
    with col_export2:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f'hydroponic_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
            use_container_width=True
        )
    with col_export3:
        json_data = df.to_json(orient='records', indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f'hydroponic_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
            mime='application/json',
            use_container_width=True
        )

else:
    st.info("📊 No data available yet. Click 'ANALYZE SYSTEM' to start monitoring.")

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px; background: rgba(0,0,0,0.3); border-radius: 10px;'>
        <p style='color: #00FFAA; font-size: 1.1em; margin: 0;'>
            <strong>🌱 AI-Powered Hydroponic Monitoring System</strong>
        </p>
        <p style='color: #888; font-size: 0.9em; margin: 10px 0 0 0;'>
            IoT + Machine Learning | Real-time Analytics | Automated Control
        </p>
        <p style='color: #666; font-size: 0.8em; margin: 10px 0 0 0;'>
            © 2026 Capstone Project | Precision Agriculture Technology
        </p>
    </div>
""", unsafe_allow_html=True)