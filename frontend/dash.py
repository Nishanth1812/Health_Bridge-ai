import streamlit as st
import requests

# Set consistent backend URL from secrets
backend_url = st.secrets.get("BACKEND_URL", "http://localhost:5000")

st.title("System Metrics Dashboard")

# Add metrics visualization
st.header("System Performance")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Response Time", value="1.2s", delta="-0.3s")
    st.metric(label="Daily Active Users", value="328", delta="12")

with col2:
    st.metric(label="Query Success Rate", value="96.8%", delta="0.2%")
    st.metric(label="Average Rating", value="4.7", delta="0.1")

# Add daily request chart
st.header("Daily Requests")
chart_data = {
    "Date": ["2023-05-12", "2023-05-13", "2023-05-14", "2023-05-15", "2023-05-16", "2023-05-17", "2023-05-18", "2023-05-19"],
    "Requests": [132, 145, 158, 187, 139, 166, 152, 143]
}

st.bar_chart(chart_data, x="Date", y="Requests")

# Add detailed metrics section
st.header("Detailed Metrics")
st.info("Metrics endpoint integration coming soon. The dashboard currently displays placeholder data.")

if st.button("Refresh Metrics"):
    try:
        resp = requests.get(f"{backend_url}/metrics/")
        if resp.status_code == 200:
            metrics = resp.json()
            st.success("Metrics refreshed successfully!")
            st.json(metrics)
        else:
            st.error(f"Failed to fetch metrics. Status code: {resp.status_code}")
    except Exception as e:
        st.error(f"Error fetching metrics: {e}")
