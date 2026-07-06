import re
import streamlit as st
import tempfile
from faster_whisper import WhisperModel


st.title("🫁 Aya", text_alignment = "center")

@st.cache_resource
def load_pipeline():
    # Adding torch_dtype="auto" or "float16" speeds up GPU inference
    return pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct", dtype=torch.float16)
pipe = load_pipeline()



model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def extract_patient(text):

    patient = {}

    patterns = {
        "hospital_number": r"hospital number\s+(\d+)",
        "name": r"name\s+(.+?)(?=age|male|female|diagnosis|$)",
        "age": r"age\s+(\d+)",
        "diagnosis": r"diagnosis\s+(.+)$"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.I)
        if match:
            patient[key] = match.group(1).strip()

    patient["gender"] = ""

    if re.search(r"\bfemale\b", text, re.I):
        patient["gender"] = "Female"

    elif re.search(r"\bmale\b", text, re.I):
        patient["gender"] = "Male"

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
