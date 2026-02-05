import streamlit as st
import pandas as pd
from scraper import run_scraper

st.set_page_config(page_title="Hospital Price Scraper MVP", layout="wide")

st.title("🏥 US Hospital Procedure Price Scraper (MVP)")

st.markdown("""
Test hospital transparency scrapers for high-demand global procedures.
Only extracts relevant rows (no full dataset downloads).
""")

# -----------------------------------------
# Hospital Input
# -----------------------------------------
st.sidebar.header("Hospital Input")

hospital_name = st.sidebar.text_input(
    "Hospital Name",
    value="Cleveland Clinic"
)

hospital_url = st.sidebar.text_input(
    "Hospital Website",
    value="https://my.clevelandclinic.org"
)

run_button = st.sidebar.button("Run Scraper")


# -----------------------------------------
# Run Scraper
# -----------------------------------------
if run_button:

    with st.spinner("Searching transparency file + extracting relevant data..."):

        df, file_link = run_scraper(hospital_name, hospital_url)

    if isinstance(df, pd.DataFrame):

        st.success("Scraper completed")

        st.subheader("Transparency File Found")
        st.write(file_link)

        st.subheader("Extracted Procedure Data (Filtered)")

        if "error" in df.columns:
            st.error(df.iloc[0]["error"])
        else:
            st.dataframe(df.head(50), use_container_width=True)

            st.metric("Rows Extracted", len(df))

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "Download Extracted Data CSV",
                csv,
                "procedure_prices_filtered.csv",
                "text/csv"
            )

    else:
        st.error("Scraper failed")
