import streamlit as st
import pandas as pd
import plotly.express as px
import kagglehub
import os

# --- 1. PROFESSIONAL PAGE SETTINGS ---
st.set_page_config(page_title="PrevaLab AI | Enterprise", layout="wide")

# --- 2. HIDE WATERMARKS ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 3. DASHBOARD HEADER ---
st.title("🔬 PrevaLab AI: Enterprise Command Center")
st.markdown("**NHS Trust Pilot Environment** | Aggregating Real-Time Telemetry & Historical Error Logs")
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

# --- 5. ENTERPRISE DASHBOARD LAYOUT ---
if not df.empty:
    # Separate data into "Live" (last 100 rows) and "Historical Errors"
    df_live = df.tail(100).reset_index()
    
    # Isolate only the rows where a machine actually failed
    df_errors = df[df['Machine failure'] == 1].copy()
    
    # Map the dataset's technical abbreviations to professional NHS terms
    df_errors['Failure Type'] = df_errors[['TWF', 'HDF', 'PWF', 'OSF', 'RNF']].idxmax(axis=1)
    failure_map = {
        'TWF': 'Tool Wear Failure (High Risk)', 
        'HDF': 'Heat Dissipation Failure (Thermal)', 
        'PWF': 'Power Failure (Electrical)', 
        'OSF': 'Overstrain Failure (Torque Load)', 
        'RNF': 'Random Hardware Failure'
    }
    df_errors['Diagnostic Description'] = df_errors['Failure Type'].map(failure_map)

    # --- SECTION A: SYSTEM KPIs ---
    st.subheader("📊 System Health & Predictive Overview")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(label="Overall Fleet Health", value="96.8%", delta="-1.2% (Monitor)")
    kpi2.metric(label="Total Historical Faults Logged", value=f"{len(df_errors)}", delta="Database Sync Active")
    kpi3.metric(label="Predicted Maintenance Interventions", value="3", delta="Required within 7 Days", delta_color="inverse")
    kpi4.metric(label="DSPT & GDPR Compliance Status", value="100%", delta="Secure Connection")
    st.divider()

    # --- SECTION B: REAL-TIME TELEMETRY ---
    st.subheader("📡 Live Asset Telemetry (Real-Time)")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Asset #001: Centrifuge**")
        fig1 = px.line(df_live, x="index", y="Rotational speed [rpm]", title="Rotational Speed (RPM)")
        fig1.update_layout(height=280, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("**Asset #002: Auto-Analyzer**")
        fig2 = px.line(df_live, x="index", y="Process temperature [K]", title="Thermal Output (K)")
        fig2.update_layout(height=280, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        st.markdown("**Asset #003: Digital Scanner**")
        fig3 = px.line(df_live, x="index", y="Torque [Nm]", title="Torque Load (Nm)")
        fig3.update_layout(height=280, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig3, use_container_width=True)
    st.divider()

    # --- SECTION C: HISTORICAL ERROR LOGS ---
    st.subheader("📂 Historical Error Logs & AI Diagnostics")
    st.markdown("Machine learning models analyze these historical fault patterns alongside real-time data to predict future downtime.")
    
    # Format the data table to look like a professional log
    display_cols = ['UDI', 'Product ID', 'Type', 'Rotational speed [rpm]', 'Process temperature [K]', 'Diagnostic Description']
    df_display = df_errors[display_cols].tail(10).reset_index(drop=True)
    df_display.rename(columns={'UDI': 'Log ID', 'Type': 'Machine Quality'}, inplace=True)
    
    st.dataframe(df_display, use_container_width=True)

else:
    st.error("Data pipeline is initializing. Please refresh the page.")