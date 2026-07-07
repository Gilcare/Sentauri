import re
import streamlit as st
import tempfile
from faster_whisper import WhisperModel
from pymongo import MongoClient


st.title("🫁 Aya", text_alignment = "center")


#MongoDB access
db_access = st.secrets.mongo_db_key



# DATABASE SETUP
client = MongoClient(db_access)  
db = client["Alveoli"]

# Create collections
data = db["Patient_Data"]




# Input Data Via Text

# List of common pulmonology diagnoses
DIAGNOSES = [
    "Asthma",
    "Atypical Pneumonia",
    "Benign Lung Mass",
    "COPD",
    "Diffuse Parenchymal Lung Disease",
    "Disseminated Tuberculosis",
    "Pulmonary Tuberculosis",
    "Post-TB Lung Sequelae",
    "Interstitial Lung Disease",
    "Lung Cancer",
    "Pneumonia",
    "Bronchiectasis",
    "Pleural Effusion",
    "Pulmonary Fibrosis",
    "Pulmonary Embolism",
    "Sarcoidosis",
    "Obstructive Sleep Apnea",
    "COVID-19 Pneumonia",
    "Empyema thoracis",
    "Supporative Lung Disease",
    "Pneumothorax",
    "Lymphangioleiomyomatosis",
    "Pulmonary Langerhans Cell Histiocytosis",
    "Viral Pharyngitis",
    "Other"
]

# Determine which diagnosis to pre-select
current_diagnosis = st.session_state.patient.get("diagnosis", "")

if current_diagnosis in DIAGNOSES:
    diagnosis_index = DIAGNOSES.index(current_diagnosis)
else:
    diagnosis_index = DIAGNOSES.index("Other")

st.divider()

with st.form("Input Patient's Details", clear_on_submit=True):

    name = st.text_input(
        "Name", 
        key = "name",
    )

    age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        key = "age"
    )

    gender = st.radio(
        "Gender",
        ["Female", "Male"], 
        key = "gender"
    )

    hospital_number = st.text_input(
        "Hospital Number", 
        key="hospital_number"
       
    )

    # Diagnosis dropdown
    selected_diagnosis = st.selectbox(
        "Diagnosis",
        DIAGNOSES,
        index=diagnosis_index
    )

    # Allow custom diagnosis
    if selected_diagnosis == "Other":
        diagnosis = st.text_input(
            "Other Diagnosis",
            value=current_diagnosis
        )
    else:
        diagnosis = selected_diagnosis

    submit = st.form_submit_button("Submit", clear_on_submit=True)

    if submit:

        patient = {
            "name": name,
            "age": age,
            "gender": gender,
            "hospital_number": hospital_number,
            "diagnosis": diagnosis
        }

        data.insert_one(patient)

        st.success("Patient record saved successfully. ✅")
