import streamlit as st
import requests


def render():
    st.header("🔎 Analyze Clinical Note")
    note = st.text_area("Paste clinical note for analysis")
    if st.button("Analyze"):
        res = requests.post(
            "http://localhost:8000/analyze_note", json={"note": note})
        if res.status_code == 200:
            data = res.json()
            st.subheader("🧬 Extracted Entities")
            for ent in data["entities"]:
                st.write(f"- **{ent['label']}**: {ent['entity']}")
            st.subheader("📝 Summary")
            st.info(data["summary"])
        else:
            st.error("Failed to analyze note.")


render()
