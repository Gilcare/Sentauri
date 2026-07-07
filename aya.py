







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

with st.form("Input Patient's Details", clear_on_submit=False):

    name = st.text_input(
        "Name", key = "name",
        value=st.session_state.patient.get("name", "")
    )

    age = st.number_input(
        "Age", key = "age",
        min_value=0,
        max_value=120,
        value=st.session_state.patient.get("age", 0)
    )

    gender = st.radio(
        "Gender",
        ["Female", "Male"], key = "gender",
        index=0 if st.session_state.patient.get("gender", "Female") == "Female" else 1
    )

    hospital_number = st.text_input(
        "Hospital Number", key="hospital_number",
        value=st.session_state.patient.get("hospital_number", "")
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
            "name": name,
            "age": age,
            "gender": gender,
            "hospital_number": hospital_number,
            "diagnosis": diagnosis
        }

        data.insert_one(patient)

        st.success("Patient record saved successfully. ✅")
