# frontend/app.py

import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Market Insights Analyst",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Market Insights Analyst")
st.markdown("Ask a complex financial question, and the multi-agent system will provide a synthesized report.")

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/analyze")

query = st.text_input(
    "Enter your financial query:",
    placeholder="e.g., How has the recent AI chip demand impacted Nvidia's stock and strategy?"
)

if st.button("Analyze"):
    if query:
        with st.spinner("Analyzing... The agents are at work! This might take a moment..."):
            try:
                response = requests.post(API_URL, json={"query": query})
                response.raise_for_status()

                result = response.json()
                st.subheader("Generated Report")
                st.markdown(result['report'])

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the backend: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a query.")