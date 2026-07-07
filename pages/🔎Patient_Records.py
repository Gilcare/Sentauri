import streamlit as st
import pandas as pd
from database import patient_data

st.title("👥 Patient Records")

records = list(patient_data.find({}, {"_id":0}))

df = pd.DataFrame(records)

search = st.text_input("Search Name or Hospital Number")

if search:

    df = df[
        df["name"].str.contains(search, case=False)
        |
        df["hospital_number"].str.contains(search)
    ]

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)
