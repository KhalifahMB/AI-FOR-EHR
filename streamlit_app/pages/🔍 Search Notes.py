import streamlit as st
import requests


def render():
    st.header("🔍 Search Notes")
    query = st.text_input("Enter your query")
    if st.button("Search"):
        res = requests.post(
            "http://localhost:8000/search_notes", json={"query": query})
        if res.status_code == 200:
            results = res.json()["results"]
            for r in results:
                st.markdown(f"**Patient:** {r['patient_id']}")
                st.code(r['snippet'])
        else:
            st.error("Search failed.")


if __name__ == "__main__":
    render()
