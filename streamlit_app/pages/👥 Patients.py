import streamlit as st
import requests
import pandas as pd

def render():
    st.title("👥 All Patients")

    # Session defaults
    if "page" not in st.session_state:
        st.session_state.page = 1
    if "limit" not in st.session_state:
        st.session_state.limit = 10
    if "search" not in st.session_state:
        st.session_state.search = ""

    # Sidebar controls
    st.sidebar.header("🔎 Filter & Pagination")
    st.session_state.search = st.sidebar.text_input("Search by name or ID", st.session_state.search)
    st.session_state.limit = st.sidebar.selectbox("Records per page", [10, 20, 50, 100], index=0)
    jump = st.sidebar.number_input("Jump to page", min_value=1, step=1, value=st.session_state.page)
    if st.sidebar.button("Go"):
        st.session_state.page = int(jump)

    # Fetch paginated data
    res = requests.get(f"http://127.0.0.1:8000/patients/all?page={st.session_state.page}&limit={st.session_state.limit}")
    if res.status_code != 200:
        st.error("Failed to fetch patient data.")
        return

    result = res.json()
    patients_df = pd.DataFrame(result["data"])
    total = result["total"]
    total_pages = (total + st.session_state.limit - 1) // st.session_state.limit

    # Filter by search
    query = st.session_state.search.lower()
    if query:
        patients_df = patients_df[
            patients_df["FIRST"].str.lower().str.contains(query) |
            patients_df["LAST"].str.lower().str.contains(query) |
            patients_df["Id"].str.lower().str.contains(query)
        ]

    # Sort controls
    sort_col = st.selectbox("Sort by", patients_df.columns, index=1)
    ascending = st.checkbox("Ascending", value=True)
    patients_df = patients_df.sort_values(by=sort_col, ascending=ascending)

    # Show patients
    for _, p in patients_df.iterrows():
        with st.expander(f"{p['FIRST']} {p['LAST']} — {p['GENDER']}, {p['RACE']}"):
            st.markdown(f"*Patient ID*: {p['Id']}")
            st.markdown(f"*DOB*: {p['BIRTHDATE']}")
            if st.button("🔍 View Summary", key=p["Id"]):
                summary_res = requests.get(
                    f"http://localhost:8000/patients/get_patient/{p['Id']}")

                if summary_res.status_code == 200:
                    data = summary_res.json()
                    st.subheader("🧬 Summary")
                    st.json(data["patient"])
                    # st.subheader("🦠 Conditions")
                    # st.write(", ".join(data["conditions"]))
                    # st.subheader("💊 Medications")
                    # st.write(", ".join(data["medications"]))
                    # st.subheader("📅 Encounters")
                    # st.json(data["encounters"])
                else:
                    st.warning("Could not fetch patient summary.")

    # Pagination controls
    col1, col2, col3 = st.columns([1, 2, 1])
    if col1.button("⬅ Prev") and st.session_state.page > 1:
        st.session_state.page -= 1
        st.experimental_rerun()
    col2.markdown(f"*Page {st.session_state.page} of {total_pages}*")
    if col3.button("Next ➡") and st.session_state.page < total_pages:
        st.session_state.page += 1
        st.experimental_rerun()


if __name__ == "__main__":
    render()