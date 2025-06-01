import streamlit as st
import requests


def render():
    st.header("📄 Upload Clinical Note")
    patient_id = st.text_input("Patient ID")
    note = st.text_area("Enter clinical note")
    if st.button("📤 Upload Note"):
        res = requests.post("http://localhost:8000/upload_note",
                            json={"patient_id": patient_id, "note": note})
        if res.status_code == 200:
            st.success(f"Note uploaded as {res.json()['filename']}")
        else:
            st.error("Upload failed.")


if __name__ == "__main__":
    render()
