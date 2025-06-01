import streamlit as st
import requests


def render():
    st.header("🏥 Predict 30-Day Readmission")
    with st.form("predict_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", 0, 120, 67)
            gender = st.selectbox("Gender", ["M", "F"])
            marital_status = st.selectbox(
                "Marital Status", ["married", "single", "divorced"])
            race = st.selectbox("Race", ["white", "black", "asian"])
            ethnicity = st.selectbox("Ethnicity", ["hispanic", "nonhispanic"])
        with col2:
            recent_encounter_type = st.selectbox(
                "Encounter Type", ["inpatient", "outpatient", "emergency"])
            num_encounters = st.number_input("Number of Encounters", 0, 50, 4)
            avg_encounter_cost = st.number_input(
                "Avg Encounter Cost", 0.0, 10000.0, 3000.0)
            num_conditions = st.number_input("Number of Conditions", 0, 10, 2)
            chronic_flag = st.selectbox("Chronic Disease", [0, 1])
            death_flag = st.selectbox("Deceased?", [0, 1])

        st.subheader("💊 Medications")
        num_meds = st.slider("Number of Medications", 0, 10, 2)
        avg_med_cost = st.number_input(
            "Avg Medication Cost", 0.0, 1000.0, 150.0)
        total_med_cost = st.number_input(
            "Total Medication Cost", 0.0, 10000.0, 500.0)

        submitted = st.form_submit_button("🔍 Predict")
        if submitted:
            payload = {
                "age": age, "gender": gender, "race": race, "ethnicity": ethnicity,
                "marital_status": marital_status, "recent_encounter_type": recent_encounter_type,
                "num_encounters": num_encounters, "avg_encounter_cost": avg_encounter_cost,
                "num_conditions": num_conditions, "chronic_disease_flag": chronic_flag,
                "num_medications": num_meds, "avg_med_cost": avg_med_cost,
                "total_med_cost": total_med_cost, "death_flag": death_flag
            }
            response = requests.post(
                "http://localhost:8000/predict", json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success(
                    f"🧠 Prediction: {'Readmitted' if result['prediction'] == 1 else 'Not Readmitted'}")
                st.info(f"Probability: {result['probability']*100:.2f}%")
            else:
                st.error("Prediction failed. Please check your input.")


if __name__ == "__main__":
    render()
