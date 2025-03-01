import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title= "Data sweeper",layout="wide")
#custom css
st.markdown(
    """
    <style>
    .stApp{
        background_color: black;
        color: white;
        }
       </style>
    """,
    unsafe_allow_html=True
)

#title and discription
st.title("📀 Datasweeper Sterling Integrator By Hafsa Sheikh")
st.write("Transform your files between CSV ans excel formats with built-in data cleaning and Visualization Creating the project for Quarter 3!")

#file uploader
uploaded_files = st.file_uploader("Upload your files (accept CSV or Excel):", type=["csv",".xlsx"], accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext  == ".xlxs":
             df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue

        #file details
        st.write("🔍 Preview the head of the Dataframe")
        st.dataframe(df.head())

        #data cleaning options
        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"remove duplicate from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")
            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(includes=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(numeric_cols.mean())
                    st.write("✅ Missing values have been filled")
    st.subheader("🎯 select coumns to keep")
    columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
    df = df[columns]          

    #data visualization
    st.subheader("📊Data Visualization")
    if st.checkbox(f"Show visualization for {file.name}"):
        st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        #conversion options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"convert {file.name} to:", ["CVS", "Excel"], key=file.name)
        if st.button(f"convert{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats.officedocument.spread.sheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Download{file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            ) 
st.success("🎉 All files processed sucessfully!")
