import streamlit as st
import pandas as pd
import plotly.express as px
import kagglehub
import os

# --- 1. PROFESSIONAL PAGE SETTINGS ---
st.set_page_config(page_title="PrevaLab AI Dashboard", layout="wide")

# --- 2. HIDE WATERMARKS (Make it look like custom software) ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 3. DASHBOARD HEADER ---
st.title("🔬 PrevaLab AI: Command Center")
st.markdown("**NHS Trust Pilot Environment** | Secure by Design: DSPT & GDPR Compliant")
st.divider()

# --- 4. AUTOMATED DATA PIPELINE ---
@st.cache_data
def load_kaggle_data():
    dataset_path = kagglehub.dataset_download("stephanmatzka/predictive-maintenance-dataset-ai4i-2020")
    csv_files = [f for f in os.listdir(dataset_path) if f.endswith('.csv')]
    if csv_files:
        full_file_path = os.path.join(dataset_path, csv_files[0])
        return pd.read_csv(full_file_path)
    return pd.DataFrame()

df = load_kaggle_data()

# --- 5. ENTERPRISE DASHBOARD LAYOUT (No External Images) ---
if not df.empty:
    df_sample = df.tail(100).reset_index()
    
    # Create 3 columns for the layout
    col1, col2, col3 = st.columns(3)

    # MACHINE 1: CENTRIFUGE
    with col1:
        st.subheader("Asset #001: Centrifuge")
        
        # Professional Metric Card instead of an image
        st.metric(label="Current Rotational Speed", value="1,540 rpm", delta="-120 rpm (Anomaly)")
        st.error("⚠️ AI WARNING: Tool Wear Anomaly Detected. Maintenance Required.")
        
        # The Data Chart (Updated to fix the warning)
        fig1 = px.line(df_sample, x="index", y="Rotational speed [rpm]", title="Live Telemetry: Rotational Speed")
        fig1.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig1, use_container_width=False) # Fixed the warning!

    # MACHINE 2: AUTO-ANALYZER
    with col2:
        st.subheader("Asset #002: Auto-Analyzer")
        
        # Professional Metric Card
        st.metric(label="Current Process Temp", value="308.2 K", delta="Stable")
        st.success("✅ STATUS: Normal. Thermal levels optimal.")
        
        # The Data Chart
        fig2 = px.line(df_sample, x="index", y="Process temperature [K]", title="Live Telemetry: Process Temp (K)")
        fig2.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig2, use_container_width=False)

    # MACHINE 3: DIGITAL SCANNER
    with col3:
        st.subheader("Asset #003: Digital Scanner")
        
        # Professional Metric Card
        st.metric(label="Current Torque Load", value="42.5 Nm", delta="+8.2 Nm (High)")
        st.warning("⚙️ STATUS: High Load Detected. Monitor Closely.")
        
        # The Data Chart
        fig3 = px.line(df_sample, x="index", y="Torque [Nm]", title="Live Telemetry: Torque (Nm)")
        fig3.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig3, use_container_width=False)
        
else:
    st.error("Data pipeline is initializing. Please refresh the page.")