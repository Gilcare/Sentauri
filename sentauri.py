import streamlit as st
from faster_whisper import WhisperModel
from transformers import pipeline

st.set_page_config(page_title="Pulmonology", layout="wide")

st.title("🫁Aya", text_alignment = "center")
st.divider()

# Choose model 
model = WhisperModel(
    "base",
    device="cpu",       
    compute_type="int8"
)
audio_file = st.audio_input("Record Data")
if audio_file:
  segments, info = model.transcribe(audio_file)
  print("Language:", info.language)
  for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

st.write(text)

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
