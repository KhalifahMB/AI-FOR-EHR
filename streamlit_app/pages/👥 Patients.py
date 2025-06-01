import streamlit as st
import requests
import pandas as pd


def render():
    st.title("👥 All Patients")

    # Load patient list
    res = requests.get("http://127.0.0.1:8000/patients/all")
    if res.status_code != 200:
        st.error("Failed to fetch patients")
        return

    patients = res.json()

    for p in patients:
        with st.expander(f"{p['FIRST']} {p['LAST']} — {p['GENDER']}, {p['RACE']}"):
            st.markdown(f"**Patient ID**: `{p['Id']}`")
            st.markdown(f"**DOB**: {p['BIRTHDATE']}")
            if st.button("🔍 View Summary", key=p["Id"]):
                summary_res = requests.get(
                    f"http://localhost:8000/patients/get_patient/{p['Id']}")
                if summary_res.status_code == 200:
                    data = summary_res.json()
                    st.subheader("🧬 Summary")
                    st.json(data["patient"])
                else:
                    st.warning("Patient summary not found.")


if __name__ == "__main__":
    render()
