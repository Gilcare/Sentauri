import pandas as pd
import streamlit as st
from database import patient_data

records = list(patient_data.find({}, {"_id": 0}))

df = pd.DataFrame(records)

if df.empty:
    st.warning("No patient records available.")
    st.stop()

df["visit_date"] = pd.to_datetime(df["visit_date"])


today = pd.Timestamp.today().normalize()

today_count = len(df[df["visit_date"] == today])

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Patients",
    len(df)
)

col2.metric(
    "Today's Visits",
    today_count
)

col3.metric(
    "Average Age",
    round(df["age"].mean())
)

col4.metric(
    "Unique Diagnoses",
    df["diagnosis"].nunique()
)


# DIAGNOSIS DISTRIBUTION
st.subheader("Diagnosis Distribution")

diagnosis_counts = (
    df["diagnosis"]
    .value_counts()
)

st.bar_chart(diagnosis_counts)

# CLINIC VISITS OVER TIME
st.subheader("Daily Patient Volume")

daily = (
    df.groupby("visit_date")
      .size()
)

st.line_chart(daily)


# GENDER DISTRIUTION
st.subheader("Gender")

gender = df["gender"].value_counts()

st.bar_chart(gender)


# AGE DISTRIBUTON
st.subheader("Age Distribution")

age_bins = pd.cut(
    df["age"],
    bins=[0,18,30,45,60,75,100]
)

ages = (
    age_bins
    .value_counts()
    .sort_index()
)

ages.index = ages.index.astype(str)

st.bar_chart(ages)


# TOP 10 DIAGNOSIS
st.subheader("Top Diagnoses")

top = (
    df["diagnosis"]
      .value_counts()
      .head(10)
)

st.dataframe(top)


# TB MONITORING
tb = df[
    df["diagnosis"].str.contains(
        "Tuberculosis",
        case=False,
        na=False
    )
]

st.metric(
    "TB Cases",
    len(tb)
)
