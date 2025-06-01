import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
import glob

st.set_page_config(page_title="📊 EHR Dashboard", layout="wide")
st.title("📊 EHR Assistant Analytics Dashboard")

# Paths
data_dir = "C:/Users/Muhammad A El-kufahn/Documents/SIWES/DATA SCIENCE ADVANCED/AI FOR EHR/data"
processed = os.path.join(data_dir, "processed")
raw = os.path.join(data_dir, "raw")
notes_dir = os.path.join(data_dir, "notes")


# Load training data
@st.cache_data
def load_training_data():
    return pd.read_csv(os.path.join(processed, "training_data.csv"))


# Load notes
@st.cache_data
def load_notes():
    files = glob.glob(os.path.join(notes_dir, "*.json"))
    data = []
    for file in files:
        with open(file, "r") as f:
            content = json.load(f)
            data.append({
                "patient_id": content.get("patient_id", "unknown"),
                "note": content.get("note", ""),
                "filename": os.path.basename(file),
                "words": len(content.get("note", "").split())
            })
    return pd.DataFrame(data)


# Load patient demographics
@st.cache_data
def load_patients():
    return pd.read_csv(os.path.join(raw, "patients.csv"))


df = load_training_data()
notes = load_notes()
patients = load_patients()

# 1. Dataset Overview
with st.expander("📦 Dataset Overview", expanded=True):
    col1, col2 = st.columns(2)
    col1.metric("Total Records", len(df))
    col2.metric("Readmitted %", f"{df['readmitted'].mean() * 100:.2f}%")

# 2. Readmission Pie Chart
with st.expander("📈 Readmission Distribution", expanded=True):
    readmit_counts = df["readmitted"].value_counts()
    labels = ["Not Readmitted", "Readmitted"]
    sizes = [readmit_counts.get(0, 0), readmit_counts.get(1, 0)]
    colors = ["skyblue", "salmon"]

    fig, ax = plt.subplots()
    wedges, _, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        wedgeprops=dict(width=0.6)
    )
    ax.axis("equal")
    ax.legend(wedges, labels, title="Classes",
              loc="center left", bbox_to_anchor=(1, 0.5))
    st.pyplot(fig)

# 3. Feature Summary
with st.expander("📊 Feature Summary Table", expanded=False):
    st.dataframe(df.describe())

# 4. Numeric Feature Distributions
with st.expander("📊 Numeric Feature Distributions", expanded=False):
    num_cols = ["age", "num_conditions", "num_encounters",
                "num_medications", "avg_encounter_cost", "total_med_cost"]
    df[num_cols].hist(bins=20, layout=(2, 3), figsize=(12, 6))
    st.pyplot(plt.gcf())
    plt.clf()

# 5. Notes Overview
with st.expander("📝 Note Upload Activity", expanded=False):
    col1, col2 = st.columns(2)
    col1.metric("Total Notes", len(notes))
    col2.metric("Average Length", f"{notes['words'].mean():.1f} words")

    st.write("📋 Recent Notes")
    st.dataframe(notes[["patient_id", "filename", "words"]
                       ].sort_values("words", ascending=False).head(10))

# 6. Patient Demographics
with st.expander("👥 Patient Demographics", expanded=False):
    categorical_cols = {
        "GENDER": "Gender",
        "RACE": "Race",
        "ETHNICITY": "Ethnicity"
    }

    for col, title in categorical_cols.items():
        st.markdown(f"### 📌 {title}")
        counts = patients[col].value_counts()
        labels = counts.index.tolist()
        sizes = counts.values
        colors = sns.color_palette("pastel")[0:len(labels)]

        fig, ax = plt.subplots()
        wedges, _, _ = ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            colors=colors,
            wedgeprops=dict(width=0.6)
        )
        ax.axis("equal")
        ax.legend(wedges, labels, title=title,
                  loc="center left", bbox_to_anchor=(1, 0.5))
        st.pyplot(fig)
