import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os
import time


hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

st.set_page_config(
    page_title="AI Data Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("AI Data Analysis Dashboard")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])


if uploaded_file:
    
    if uploaded_file is not None:

    # create data folder if not exists
        os.makedirs("data", exist_ok=True)

        file_path = os.path.join("data", uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"File saved to {file_path}")

        df = pd.read_csv(file_path)

        st.dataframe(df.head())

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Information")

    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])

    st.subheader("Column Data Types")
    st.write(df.dtypes)

    st.subheader("Statistical Summary")
    st.write(df.describe())
    

    
    numeric_columns = df.select_dtypes(include=['int64','float64']).columns

    if len(numeric_columns) > 0:

        column = st.selectbox("Select column for visualization", numeric_columns)

       
        data = df[column].values

        placeholder = st.empty()

        fig, ax = plt.subplots()

        for i in range(1, len(data)):

            ax.clear()
            ax.plot(data[:i])   # gradually growing line

            ax.set_title("Animated Line Chart")
            ax.set_xlabel("Index")
            ax.set_ylabel(column)

            placeholder.pyplot(fig)

            time.sleep(0.05)

    conn = sqlite3.connect(':memory:')
    df.to_sql('dataset', conn, index=False, if_exists='replace')

    st.subheader("Run SQL Query")

    query = st.text_area("Enter SQL query")

    if st.button("Run Query"):

        result = pd.read_sql(query, conn)

        st.write(result)
    

    st.sidebar.header("Filters")

    column_filter = st.sidebar.selectbox(
        "Select column to filter",
        df.columns
    )

    value = st.sidebar.text_input("Value")

    if value:

        filtered = df[df[column_filter].astype(str) == value]

        st.write(filtered)
        
    
