import streamlit as st
from faster_whisper import WhisperModel
import tempfile
import re

st.set_page_config(page_title="Pulmonology Voice Entry", layout="wide")
st.title("🫁 Pulmonology Voice Clinical Entry")

# ---------------------------
# Load model (cached!)
# ---------------------------
@st.cache_resource
def load_model():
    return WhisperModel("base", device="cpu", compute_type="int8")

model = load_model()

# ---------------------------
# Audio input
# ---------------------------
audio_file = st.audio_input("Record Patient Details")

def extract_fields(text: str):
    """
    Simple deterministic parser (fast + offline)
    """

    text = text.lower()

    # Hospital number (assumes digits)
    hospital_number = re.search(r"hospital number\s*(\d+)", text)
    hospital_number = hospital_number.group(1) if hospital_number else None

    # Age
    age = re.search(r"(\d{1,3})\s*year", text)
    age = int(age.group(1)) if age else None

    # Gender
    gender = None
    if "male" in text:
        gender = "Male"
    elif "female" in text:
        gender = "Female"

    # Name (very naive fallback)
    name_match = re.search(r"name\s*([a-z\s]+)", text)
    name = name_match.group(1).strip().title() if name_match else None

    # Diagnosis (everything after "diagnosis")
    diagnosis = None
    diag_match = re.search(r"diagnosis\s*(.*)", text)
    if diag_match:
        diagnosis = diag_match.group(1).strip().title()

    return {
        "hospital_number": hospital_number,
        "full_name": name,
        "age": age,
        "gender": gender,
        "diagnosis": diagnosis
    }

# ---------------------------
# MAIN PIPELINE
# ---------------------------
if audio_file is not None:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    segments, info = model.transcribe(tmp_path)

    transcription = " ".join([s.text for s in segments])

    st.subheader("📝 Transcription")
    st.write(transcription)

    # Extract structured fields
    data = extract_fields(transcription)

    st.subheader("📋 Auto-filled Patient Form")

    with st.form("patient_form"):
        hospital_number = st.text_input("Hospital Number", value=data["hospital_number"] or "")
        full_name = st.text_input("Full Name", value=data["full_name"] or "")
        age = st.number_input("Age", value=data["age"] or 0)
        gender = st.selectbox("Gender", ["Male", "Female"], index=0 if data["gender"] == "Male" else 1)
        diagnosis = st.text_input("Diagnosis", value=data["diagnosis"] or "")

        submitted = st.form_submit_button("Save Patient")

        if submitted:
            st.success("Patient record ready for database insertion")
