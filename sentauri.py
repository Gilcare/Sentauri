import re
import streamlit as st
import tempfile
from faster_whisper import WhisperModel


st.title("🫁 Aya", text_alignment = "center")

"""@st.cache_resource
def load_pipeline():
    # Adding torch_dtype="auto" or "float16" speeds up GPU inference
    return pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct", dtype=torch.float16)
pipe = load_pipeline()"""



model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


st.info("""Please say:
\nName,
\nAge,
\nGender,
\nHospital Number,
\nDiagnosis.
\nExample:'John Smith, age 54, male, hospital number 345678, diagnosis asthma.'""")


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

if audio_file is not None:
    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    segments, info = model.transcribe(tmp_path)

    st.write("Language:", info.language)

    full_text = ""

    for segment in segments:
        full_text += segment.text + " "
        st.write(f"{segment.start:.2f}s → {segment.end:.2f}s : {segment.text}")

    st.subheader("Full transcription")
    st.success(full_text)
    patient = extract_fields(full_text)

    st.session_state.name = patient["name"] or ""
    st.session_state.age = patient["age"] or 0
    st.session_state.gender = patient["gender"] or "Female"
    st.session_state.hospital_number = patient["hospital_number"] or ""
    st.session_state.diagnosis = patient["diagnosis"] or ""
    

    st.session_state.patient = patient












st.divider()
# Input Data Via Text
st.divider()

with st.form("Input Patient's Details"):

    name = st.text_input(
        "Name",
        value=st.session_state.patient["name"], key = "name"
    )

    age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=st.session_state.patient["age"], key = "age"
    )

    gender = st.radio(
        "Gender",
        ["Female", "Male"], key = "gender",
        index=0 if st.session_state.patient["gender"] == "Female" else 1
    )

    hospital_number = st.text_input(
        "Hospital Number", key = "hospital_number",
        value=st.session_state.patient["hospital_number"]
    )

    diagnosis = st.text_input(
        "Diagnosis", key = "diagnosis",
        value=st.session_state.patient["diagnosis"]
    )

    submit = st.form_submit_button("Submit")

    if submit:
        st.success("Submitted ☑️")
