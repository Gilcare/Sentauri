import streamlit as st
import pandas as pd
from scraper import run_scraper

st.set_page_config(page_title="Hospital Price Scraper MVP", layout="wide")

st.title("🏥 US Hospital Procedure Price Scraper (MVP)")

st.markdown("""
Test hospital transparency scrapers for high-demand global procedures.
Only extracts relevant rows (no full dataset downloads).
""")

