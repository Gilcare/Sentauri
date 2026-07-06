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


st.info("Please say:

Name,
Age,
Gender,
Hospital Number,
Diagnosis.

Example:
'John Smith, age 54, male, hospital number 345678, diagnosis asthma.'")



import re

def extract_fields(text: str):
    """
    Extract hospital number, age and gender from a transcript.

    Examples:
    - Jared Kushner, age 74, hospital number 36449968, diagnosis pneumonia
    - John Smith, 56-year-old male, hospital no 12345678
    - Hospital #987654, Jane Doe, female, 42 years old
    """

    patient = {
        "hospital_number": None,
        "age": None,
        "gender": None
    }

    # -------------------------
    # Hospital Number
    # Matches:
    # hospital number 12345
    # hospital no 12345
    # hospital #12345
    # -------------------------
    hospital_match = re.search(
        r"hospital\s*(?:number|no\.?|#)\s*(\d+)",
        text,
        re.IGNORECASE
    )

    if hospital_match:
        patient["hospital_number"] = hospital_match.group(1)

    # -------------------------
    # Age
    # Matches:
    # age 74
    # 74 years old
    # 74-year-old
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
    data = extract_patient(full_text)
    st.write(data)












st.divider()
# Input Data Via Text
with st.form("Input Patient's Details", clear_on_submit = True):
  name= st.text_input("Name")
  age= st.number_input("Age")
  gender= st.radio("Gender", ["Female","Male"])
  hospital_number = st.number_input("Hospital Number")
  diagnosis = st.text_input("Diagnosis")
  submit = st.form_submit_button("Submit")
  if submit:
    st.success("Submitted☑️")
