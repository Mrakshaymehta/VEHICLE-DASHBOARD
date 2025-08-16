# test.py

import streamlit as st
import pandas as pd

st.title("System Diagnostic Test")

try:
    # 1. Load just ONE file to keep it simple
    st.header("1. Loading 'data/4W.csv'")
    df = pd.read_csv('data/4W.csv', skiprows=4)
    st.success("File loaded successfully.")

    # 2. Show the original column names
    st.header("2. Original Column Names")
    st.info("These are the columns exactly as they appear in the file:")
    st.write(df.columns)

    # 3. Clean the column names by stripping whitespace
    st.header("3. Cleaning Column Names")
    df.columns = df.columns.str.strip()
    st.success("Whitespace stripped successfully.")
    st.info("Columns after cleaning:")
    st.write(df.columns)

    # 4. Rename the 'Maker Name' column
    st.header("4. Renaming 'Maker Name'")
    df.rename(columns={'Maker Name': 'manufacturer'}, inplace=True)
    st.success("Rename function executed.")
    st.info("Columns after renaming:")
    st.write(df.columns)

    # 5. Check if 'manufacturer' column exists
    st.header("5. Final Verification")
    if 'manufacturer' in df.columns:
        st.success("✅ SUCCESS: The 'manufacturer' column now exists.")
    else:
        st.error("❌ FAILURE: The 'manufacturer' column was NOT created.")

except Exception as e:
    st.error(f"An error occurred: {e}")