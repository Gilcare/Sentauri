import re
import streamlit as st
import tempfile
from datetime import date
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



if "visit_date" not in st.session_state:
    st.session_state.visit_date = date.today()
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
"""current_diagnosis = st.session_state.get("diagnosis", "")

if current_diagnosis in DIAGNOSES:
    diagnosis_index = DIAGNOSES.index(current_diagnosis)
else:
    diagnosis_index = DIAGNOSES.index("Other")"""


# -------------------------
# Diagnosis
# -------------------------

# Initialize session state
if "selected_diagnosis" not in st.session_state:
    st.session_state.selected_diagnosis = "Other"

if "custom_diagnosis" not in st.session_state:
    st.session_state.custom_diagnosis = ""




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
        key="selected_diagnosis"
    )


    visit_date = st.date_input(
        "Visit Date",
        key="visit_date"
    )

    
    # If "Other" is selected, allow custom diagnosis entry
    if selected_diagnosis == "Other":
        st.text_input(
            "Enter Diagnosis",
            key="custom_diagnosis",
            placeholder="e.g. Allergic Bronchopulmonary Aspergillosis"
        )
        diagnosis = st.session_state.custom_diagnosis.strip()
    else:
        diagnosis = selected_diagnosis

    submit = st.form_submit_button("Submit")

    if submit:

        if selected_diagnosis == "Other" and not diagnosis:
            st.error("Please enter a diagnosis.")

        else:
            patient = {
            "name": name,
            "age": age,
            "gender": gender,
            "hospital_number": hospital_number,
            "diagnosis": diagnosis,
            "visit_date": st.session_state.visit_date.isoformat(),
            }
            
            data.insert_one(patient)
            
            st.success("Patient record saved successfully. ✅")
