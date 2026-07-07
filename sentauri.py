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


model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


if "audio_processed" not in st.session_state:
    st.session_state.audio_processed = False

st.info("""Please say:
\nName,
\nAge,
\nGender,
\nHospital Number,
\nDiagnosis.
\nExample:'Ada Femi, age 25, female, hospital number 345678, diagnosis asthma.'""")


if "patient" not in st.session_state:
    st.session_state.patient = {
        "name": "",
        "age": 0,
        "gender": "Female",
        "hospital_number": "",
        "diagnosis": ""
    }



def extract_fields(text: str):
    """
    Extract patient details from a clinical transcript.

    Expected examples:
    - Jared Kushner, age 74, male, hospital number 36449968, diagnosis pneumonia.
    - Mary Jane Doe, 52-year-old female, hospital number 55667788, diagnosis pulmonary tuberculosis.
    """

    patient = {
        "name": None,
        "age": None,
        "gender": None,
        "hospital_number": None,
        "diagnosis": None
    }

    # -------------------------
    # Name
    # Everything before age or hospital number
    # -------------------------
    name_match = re.search(
        r"^\s*(.+?)(?=,\s*(?:age|\d{1,3}-?year|hospital))",
        text,
        re.IGNORECASE
    )

    if name_match:
        patient["name"] = name_match.group(1).strip().title()

    # -------------------------
    # Age
    # -------------------------
    age_patterns = [
        r"age\s*(\d{1,3})",
        r"(\d{1,3})\s*years?\s*old",
        r"(\d{1,3})[-\s]*year[-\s]*old"
    ]

    for pattern in age_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            patient["age"] = int(match.group(1))
            break

    # -------------------------
    # Gender
    # -------------------------
    gender_match = re.search(
        r"\b(male|female)\b",
        text,
        re.IGNORECASE
    )

    if gender_match:
        patient["gender"] = gender_match.group(1).title()

    # -------------------------
    # Hospital Number
    # -------------------------
    hospital_match = re.search(
        r"hospital\s*(?:number|no\.?|#)\s*(\d+)",
        text,
        re.IGNORECASE
    )

    if hospital_match:
        patient["hospital_number"] = hospital_match.group(1)

    # -------------------------
    # Diagnosis
    # Everything after "diagnosis"
    # -------------------------
    diagnosis_match = re.search(
        r"diagnosis[:,]?\s*(.+?)[.]?$",
        text,
        re.IGNORECASE
    )

    if diagnosis_match:
        patient["diagnosis"] = diagnosis_match.group(1).strip().title()

    return patient




audio_file = st.audio_input("Record Data")

if audio_file is not None and not st.session_state.audio_processed:
    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    segments, info = model.transcribe(tmp_path)

    #st.write("Language:", info.language)

    full_text = ""

    for segment in segments:
        full_text += segment.text + " "
        #st.write(f"{segment.start:.2f}s → {segment.end:.2f}s : {segment.text}")

    st.subheader("Full transcription")
    st.success(full_text)
    patient = extract_fields(full_text)

    st.session_state["name"] = patient["name"] or ""
    st.session_state["age"] = patient["age"] or 0
    st.session_state["gender"] = patient["gender"] or "Female"
    st.session_state["hospital_number"] = patient["hospital_number"] or ""
    st.session_state["diagnosis"] = patient["diagnosis"] or ""

    st.session_state.audio_processed = True



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
current_diagnosis = st.session_state.get("diagnosis", "")

if current_diagnosis in DIAGNOSES:
    diagnosis_index = DIAGNOSES.index(current_diagnosis)
else:
    diagnosis_index = DIAGNOSES.index("Other")

st.divider()

with st.form("Input Patient's Details", clear_on_submit=True):

    name = st.text_input("Name", key="name")

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

    submit = st.form_submit_button("Submit")


    if submit:
        patient = {
            "name": st.session_state.name,
            "age": st.session_state.age,
            "gender": st.session_state.gender,
            "hospital_number": st.session_state.hospital_number,
            "diagnosis": diagnosis
        }

        data.insert_one(patient)

        st.success("Patient record saved successfully.")
        st.session_state.name = ""
        st.session_state.age = 0
        st.session_state.gender = "Female"
        st.session_state.hospital_number = ""
        st.session_state.diagnosis = ""
        
        st.session_state.audio_processed = False
        
        st.rerun ()

