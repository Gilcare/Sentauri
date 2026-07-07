import streamlit as st
from datetime import date

from database import patient_data
from constants import DIAGNOSES


st.title("📝 Add New Patient")


# -------------------------
# Session State Initialization
# -------------------------

if "visit_date" not in st.session_state:
    st.session_state.visit_date = date.today()

if "selected_diagnosis" not in st.session_state:
    st.session_state.selected_diagnosis = "Other"

if "custom_diagnosis" not in st.session_state:
    st.session_state.custom_diagnosis = ""

if "gender" not in st.session_state:
    st.session_state.gender = "Female"

if "age" not in st.session_state:
    st.session_state.age = 0


st.divider()


# -------------------------
# Patient Form
# -------------------------

with st.form(
    "Input Patient Details",
    clear_on_submit=True
):

    name = st.text_input(
        "Name",
        key="name"
    )


    age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        key="age"
    )


    gender = st.radio(
        "Gender",
        ["Female", "Male"],
        key="gender"
    )


    hospital_number = st.text_input(
        "Hospital Number",
        key="hospital_number"
    )


    # Diagnosis dropdown
    selected_diagnosis = st.selectbox(
        "Diagnosis",
        DIAGNOSES,
        key="selected_diagnosis"
    )


    # Visit date
    visit_date = st.date_input(
        "Visit Date",
        key="visit_date"
    )


    # -------------------------
    # Custom Diagnosis
    # -------------------------

    if selected_diagnosis == "Other":

        custom_diagnosis = st.text_input(
            "Other Diagnosis",
            key="custom_diagnosis",
            placeholder="e.g. Hypertensive Heart Disease"
        )

        diagnosis = custom_diagnosis.strip()

    else:

        diagnosis = selected_diagnosis



    submit = st.form_submit_button(
        "Submit"
    )



# -------------------------
# Save Patient
# -------------------------

if submit:

    if selected_diagnosis == "Other" and not diagnosis:

        st.error(
            "Please enter a diagnosis."
        )

    else:

        patient = {

            "name": name,

            "age": age,

            "gender": gender,

            "hospital_number": hospital_number,

            "diagnosis": diagnosis,

            "visit_date": visit_date.isoformat()

        }


        patient_data.insert_one(patient)


        st.success(
            "Patient record saved successfully. ✅"
        )
