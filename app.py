import streamlit as st
import time
import json
import matplotlib.pyplot as plt
from streamlit_lottie import st_lottie

from data_loader import load_workflow_data
from process_analysis import detect_bottleneck

st.set_page_config(
    page_title="Workflow Bottleneck Detector",
    layout="wide"
)

st.title("🔧 Workflow Bottleneck Detection Dashboard")

# -------- LOTTIE ANIMATION --------
import requests
from streamlit_lottie import st_lottie

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

lottie_animation = load_lottie_url(
    "https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json"
)

st_lottie(lottie_animation, height=280, key="workflow")


# -------- SPINNER --------
with st.spinner("Initializing workflow analysis..."):
    time.sleep(1.5)

# -------- PIPELINE PROGRESS --------
st.subheader("⚙️ Process Execution Status")

progress = st.progress(0)
status = st.empty()

steps = [
    "Loading workflow logs...",
    "Parsing timestamps...",
    "Calculating stage durations...",
    "Analyzing process flow...",
    "Detecting bottlenecks..."
]

for i, step in enumerate(steps):
    status.text(step)
    progress.progress((i + 1) * 20)
    time.sleep(0.6)

status.success("Process analysis completed")

# -------- LOAD & ANALYZE --------
df = load_workflow_data("data/workflow_logs.csv")
stats, bottleneck = detect_bottleneck(df)

# -------- KPIs (ANIMATED) --------
time.sleep(0.3)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Tasks", df["task_id"].nunique())

time.sleep(0.3)
with col2:
    st.metric("Avg Duration (min)", round(stats["duration_minutes"].mean(), 2))

time.sleep(0.3)
with col3:
    st.metric("Bottleneck Stage", bottleneck["stage"], "⚠ Delay")

# -------- CHART --------
st.subheader("📊 Stage-wise Average Delay")

fig, ax = plt.subplots()
ax.bar(stats["stage"], stats["duration_minutes"])
ax.set_ylabel("Minutes")
st.pyplot(fig)

# -------- INSIGHT --------
st.warning(
    f"⚠ Bottleneck detected at **{bottleneck['stage']}** stage. "
    "Process optimization recommended."
)

# -------- RAW DATA --------
with st.expander("🔍 View Workflow Logs"):
    st.dataframe(df)
