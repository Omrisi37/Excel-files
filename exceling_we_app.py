# %%writefile app.py
import streamlit as st
import pandas as pd
import io
from datetime import datetime

def main():
    st.title("Lab Experiment Data Collection")

    # Initialize session state to store data
    if 'all_data' not in st.session_state:
        st.session_state.all_data = []

    # 1. Procedure - Settings
    st.subheader("1. Procedure - Settings")
    procedure_num = st.text_input("#Num", "")
    procedure_date = st.date_input("Date", value=datetime.now())  # Default to today
    procedure_labeling = st.text_input("Labeling", "")
    protein_type = st.selectbox("Protein type", ["", "Type A", "Type B", "Type C"], index=0) #index=0 makes the first slot balnk
    protein_concentration = st.text_input("Concentration [wt/wt%]", "")

    # 2. Procedure - Physical Treatments
    st.subheader("2. Procedure - Physical Treatments")
    right_valve = st.text_input("Right valve [bar]", "")
    left_valve = st.text_input("Left valve 2 [bar]", "")
    temp_after_HPH = st.text_input("Temp after HPH [°C]", "")
    HPH_fraction = st.text_input("HPH fraction [%]", "")
    initial_water_temp = st.text_input("Initial water temp", "")
    mixing_temp = st.text_input("Mixing temp[°C]", "")
    mixing_time = st.text_input("Mixing time", "")
    heat_treatment_fraction = st.text_input("Heat treatment fraction[%]", "")
    pH = st.text_input("pH", "")

    # 3. Black box ? + Procedure - Enz Hydro
    st.subheader("3. Black box ? + Procedure - Enz Hydro")
    enz_YN = st.selectbox("Y/N", ["", "Yes", "No"], index=0)
    enz_num = st.text_input("Enz num.", "")
    enz_name = st.selectbox("Name", ["", "Enzyme A", "Enzyme B"], index=0)
    enz_concentration = st.text_input("Concentration [%]", "")
    enz_added = st.text_input("Added enz [g]", "")
    enz_addition_temp = st.text_input("Addition temp [°C]", "")
    enz_ino_time = st.text_input("Ino. time [min]", "")
    enz_ino_temp = st.text_input("Ino. temp. [°C]", "")
    enz_stirring = st.text_input("stirring [RPM]", "")
    black_box_protein_fraction = st.text_input("black box protein fraction[%]", "")

    # 4. Procedure - Enz Cross
    st.subheader("4. Procedure - Enz Cross")
    cross_enz_num = st.text_input("Enz num.", "")
    cross_enz_name = st.selectbox("Name", ["", "Crosslinker X", "Crosslinker Y"], index = 0)
    cross_enz_concentration = st.text_input("Concentration [%]", "")
    cross_enz_added = st.text_input("Added enz [g]", "")
    cross_enz_addition_temp = st.text_input("Addition temp [°C]", "")
    cross_enz_ino_time = st.text_input("Ino. time [min]", "")
    cross_enz_ino_temp = st.text_input("Ino. temp. [°C]", "")
    cross_enz_stirring = st.text_input("stirring [RPM]", "")

    # Collect data
    if st.button("Save Data"):
        data = {
            "Procedure #Num": procedure_num,
            "Procedure Date": procedure_date.strftime("%Y-%m-%d"),
            "Procedure Labeling": procedure_labeling,
            "Protein Type": protein_type,
            "Protein Concentration": protein_concentration,
            "Right Valve": right_valve,
            "Left Valve": left_valve,
            "Temp after HPH": temp_after_HPH,
            "HPH Fraction": HPH_fraction,
            "Initial Water Temp": initial_water_temp,
            "Mixing Temp": mixing_temp,
            "Mixing Time": mixing_time,
            "Heat Treatment Fraction": heat_treatment_fraction,
            "pH": pH,
            "Enz Y/N": enz_YN,
            "Enz Num": enz_num,
            "Enz Name": enz_name,
            "Enz Concentration": enz_concentration,
            "Enz Added": enz_added,
            "Enz Addition Temp": enz_addition_temp,
            "Enz Ino. Time": enz_ino_time,
            "Enz Ino. Temp": enz_ino_temp,
            "Enz Stirring": enz_stirring,
            "Black Box Protein Fraction": black_box_protein_fraction,
            "Cross Enz Num": cross_enz_num,
            "Cross Enz Name": cross_enz_name,
            "Cross Enz Concentration": cross_enz_concentration,
            "Cross Enz Added": cross_enz_added,
            "Cross Enz Addition Temp": cross_enz_addition_temp,
            "Cross Enz Ino. Time": cross_enz_ino_time,
            "Cross Enz Ino. Temp": cross_enz_ino_temp,
            "Cross Enz Stirring": cross_enz_stirring,
        }
        st.session_state.all_data.append(data)
        st.success("Data saved!")

    # Create Combined Excel File and Download
    st.subheader("Create Combined Excel File and Download")
    if st.button("Create and Download Excel File"):
        if st.session_state.all_data:
            try:
                df = pd.DataFrame(st.session_state.all_data)

                # Create an in-memory buffer
                excel_buffer = io.BytesIO()

                # Use Pandas Excel writer and save to buffer
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Combined Data', index=False)

                excel_buffer.seek(0)  # Reset buffer to the beginning

                # Download Button
                st.download_button(
                    label="Download Combined Excel File",
                    data=excel_buffer,
                    file_name="combined_lab_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Error creating Excel file: {e}")
        else:
            st.warning("No data saved yet.")

if __name__ == "__main__":
    main()
