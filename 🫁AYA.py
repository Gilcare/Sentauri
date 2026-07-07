import streamlit as st
import pandas as pd
from database import patient_data

st.set_page_config(
    page_title="Aya",
    page_icon="🫁",
    layout="wide"
)

st.title("🫁 Aya", text_alignment = "center")

records = list(patient_data.find({}, {"_id":0}))

df = pd.DataFrame(records)

col1,col2,col3 = st.columns(3)

col1.metric(
    "Total Patients",
    len(df)
)

if len(df):
    col2.metric(
        "Average Age",
        round(df.age.mean())
    )

    col3.metric(
        "Diagnoses",
        df.diagnosis.nunique()
    )

st.divider()

st.subheader("Recent Patients")

st.dataframe(
    df.tail(10),
    use_container_width=True,
    hide_index=True
)
