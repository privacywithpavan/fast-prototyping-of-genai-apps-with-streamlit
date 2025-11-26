import streamlit as st
import pandas as pd
import re


def clean_text(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    return text


st.title("Hello, Generative AI")

st.write(
    "This is a simple app to demonstrate Generative AI integration with Streamlit."
)

uploaded_file = st.file_uploader(
    label="Upload your own dataset (CSV format)", type="csv"
)

col1, col2 = st.columns(2)

with col1:
    if st.button("📤 Ingest Dataset"):
        try:
            if uploaded_file is not None:
                dataset = pd.read_csv(uploaded_file)
                st.session_state["df"] = dataset
                st.success("Dataset ingested successfully!")
            else:
                st.info("Please upload a CSV file to ingest the dataset.")
        except Exception as e:
            st.error(f"Error ingesting dataset: {e}")

with col2:
    if st.button("🧹 Parse Reviews"):
        if "df" in st.session_state:
            st.session_state["df"]["CLEANED_SUMMARY"] = st.session_state["df"][
                "SUMMARY"
            ].apply(clean_text)
            st.success("Reviews parsed and cleaned!")
        else:
            st.warning("Please ingest the dataset first.")

if "df" in st.session_state:
    st.subheader("🔍 Filter by Product")
    product = st.selectbox(
        label="Select a product to filter reviews:",
        options=["ALL Products"] + list(st.session_state["df"]["PRODUCT"].unique()),
    )

    st.subheader(f"📁 Reviews for {product}")
    if product != "ALL Products":
        filtered_df = st.session_state["df"][
            st.session_state["df"]["PRODUCT"] == product
        ]
    else:
        filtered_df = st.session_state["df"]

    st.dataframe(filtered_df)

    st.subheader("Sentiment score by Product")
    grouped = st.session_state["df"].groupby("PRODUCT")["SENTIMENT_SCORE"].mean()
    st.bar_chart(grouped)
