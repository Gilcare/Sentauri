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
    data = extract_fields(full_text)
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
