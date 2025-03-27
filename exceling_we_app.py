# %%writefile app.py
import streamlit as st
import pandas as pd
from datetime import datetime

def main():
    st.title("Lab Experiment Data Collection")

    # Function to upload and process Excel files
    def upload_excel(section_name, section_title):
        st.subheader(section_title)
        uploaded_file = st.file_uploader(f"Upload {section_title} (Excel)", type=["xlsx", "xls"])
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file)
                return df
            except Exception as e:
                st.error(f"Error reading {section_title}: {e}")
                return None
        return None

    # 1. Procedure - Settings
    settings_df = upload_excel("Settings", "Procedure - Settings")

    # 2. Procedure - Physical Treatments
    physical_treatments_df = upload_excel("Physical Treatments", "Procedure - Physical Treatments")

    # 3. Black box ? + Procedure - Enz Hydro
    enz_hydro_df = upload_excel("Enz Hydro", "Black box ? + Procedure - Enz Hydro")

    # 4. Procedure - Enz Cross
    enz_cross_df = upload_excel("Enz Cross", "Procedure - Enz Cross")

    # 5. Gel / Drying process
    gel_drying_df = upload_excel("Gel Drying", "Gel / Drying process")

    # 6. Gel functionality
    gel_functionality_df = upload_excel("Gel Functionality", "Gel functionality")

    # Merge and Download Button
    st.subheader("Merge and Download")
    if st.button("Create Combined Excel File"):
        dfs = {
            "Procedure Settings": settings_df,
            "Physical Treatments": physical_treatments_df,
            "Enz Hydro": enz_hydro_df,
            "Enz Cross": enz_cross_df,
            "Gel Drying": gel_drying_df,
            "Gel Functionality": gel_functionality_df
        }

        # Remove None dataframes
        valid_dfs = {k: df for k, df in dfs.items() if df is not None}

        if valid_dfs:
            try:
                # Concatenate all dataframes
                combined_df = pd.concat(valid_dfs.values(), ignore_index=True)
                combined_df.insert(0, 'Row Index', combined_df.index)

                # Download Button
                st.download_button(
                    label="Download Combined Excel File",
                    data=combined_df.to_excel(index=False, engine='openpyxl').encode('utf-8'),
                    file_name="combined_lab_data.xlsx",
                    mime="application/vnd.ms-excel"
                )
                st.success("Excel file created, download will start automatically.")

            except Exception as e:
                st.error(f"Error concatenating files: {e}")
        else:
            st.warning("Please upload at least one file to merge.")

if __name__ == "__main__":
    main()
