# %%writefile app.py
import streamlit as st
import pandas as pd
import io
from datetime import datetime

def main():
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "welcome"

    # ==========================================================
    # Functions to switch between pages
    # ==========================================================
    def show_welcome_page():
        st.title("Welcome to the Lab Data Collection App")
        st.write("Choose a protocol to begin:")

        if st.button("Experiments Type 1"):
            st.session_state.page = "experiments_type_1"
            st.rerun()

    def show_experiments_type_1():
        st.title("Experiments Type 1 Data Collection")

        # Initialize session state to store data
        if 'all_data' not in st.session_state:
            st.session_state.all_data = {}

        # 1. Procedure - Settings
        st.subheader("1. Procedure - Settings")
        procedure_num = st.text_input("#Num", key="procedure_num")
        procedure_date = st.date_input("Date", value=datetime.now(), key="procedure_date")
        procedure_labeling = st.text_input("Labeling", key="procedure_labeling")
        protein_type = st.selectbox("Protein type", ["", "Type A", "Type B", "Type C"], index=0, key="protein_type")
        protein_concentration = st.text_input("Concentration [wt/wt%]", key="protein_concentration")

        st.session_state.all_data['Procedure - Settings'] = {
            "#Num": procedure_num,
            "Date": procedure_date.strftime("%Y-%m-%d"),
            "Labeling": procedure_labeling,
            "Protein type": protein_type,
            "Concentration [wt/wt%]": protein_concentration,
        }

        # 2. Procedure - Physical Treatments
        st.subheader("2. Procedure - Physical Treatments")
        right_valve = st.text_input("Right valve [bar]", key="right_valve")
        left_valve = st.text_input("Left valve 2 [bar]", key="left_valve")
        temp_after_HPH = st.text_input("Temp after HPH [°C]", key="temp_after_HPH")
        HPH_fraction = st.text_input("HPH fraction [%]", key="HPH_fraction")
        initial_water_temp = st.text_input("Initial water temp", key="initial_water_temp")
        mixing_temp = st.text_input("Mixing temp[°C]", key="mixing_temp")
        mixing_time = st.text_input("Mixing time", key="mixing_time")
        heat_treatment_fraction = st.text_input("Heat treatment fraction[%]", key="heat_treatment_fraction")
        pH = st.text_input("pH", key="pH")

        st.session_state.all_data['Procedure - Physical Treatments'] = {
            "Right valve [bar]": right_valve,
            "Left valve 2 [bar]": left_valve,
            "Temp after HPH [°C]": temp_after_HPH,
            "HPH fraction [%]": HPH_fraction,
            "Initial water temp": initial_water_temp,
            "Mixing temp[°C]": mixing_temp,
            "Mixing time": mixing_time,
            "Heat treatment fraction[%]": heat_treatment_fraction,
            "pH": pH,
        }

        # 3. Black box ? + Procedure - Enz Hydro
        st.subheader("3. Black box ? + Procedure - Enz Hydro")
        enz_YN = st.selectbox("Y/N", ["", "Yes", "No"], index=0, key="enz_YN")
        enz_num = st.text_input("Enz num.", key="enz_num")
        enz_name = st.selectbox("Name", ["", "Enzyme A", "Enzyme B"], index=0, key="enz_name")
        enz_concentration = st.text_input("Concentration [%]", key="enz_concentration")
        enz_added = st.text_input("Added enz [g]", key="enz_added")
        enz_addition_temp = st.text_input("Addition temp [°C]", key="enz_addition_temp")
        enz_ino_time = st.text_input("Ino. time [min]", key="enz_ino_time")
        enz_ino_temp = st.text_input("Ino. temp. [°C]", key="enz_ino_temp")
        enz_stirring = st.text_input("stirring [RPM]", key="enz_stirring")
        black_box_protein_fraction = st.text_input("black box protein fraction[%]", key="black_box_protein_fraction")

        st.session_state.all_data['Black box ? + Procedure - Enz Hydro'] = {
            "Y/N": enz_YN,
            "Enz num.": enz_num,
            "Name": enz_name,
            "Concentration [%]": enz_concentration,
            "Added enz [g]": enz_added,
            "Addition temp [°C]": enz_addition_temp,
            "Ino. time [min]": enz_ino_time,
            "Ino. temp. [°C]": enz_ino_temp,
            "stirring [RPM]": enz_stirring,
            "black box protein fraction[%]": black_box_protein_fraction,
        }

        # 4. Procedure - Enz Cross
        st.subheader("4. Procedure - Enz Cross")
        cross_enz_num = st.text_input("Enz num.", key="cross_enz_num")
        cross_enz_name = st.selectbox("Name", ["", "Crosslinker X", "Crosslinker Y"], index = 0, key="cross_enz_name")
        cross_enz_concentration = st.text_input("Concentration [%]", key="cross_enz_concentration")
        cross_enz_added = st.text_input("Added enz [g]", key="cross_enz_added")
        cross_enz_addition_temp = st.text_input("Addition temp [°C]", key="cross_enz_addition_temp")
        cross_enz_ino_time = st.text_input("Ino. time [min]", key="cross_enz_ino_time")
        cross_enz_ino_temp = st.text_input("Ino. temp. [°C]", key="cross_enz_ino_temp")
        cross_enz_stirring = st.text_input("stirring [RPM]", key="cross_enz_stirring")

        st.session_state.all_data['Procedure - Enz Cross'] = {
            "Enz num.": cross_enz_num,
            "Name": cross_enz_name,
            "Concentration [%]": cross_enz_concentration,
            "Added enz [g]": cross_enz_added,
            "Addition temp [°C]": cross_enz_addition_temp,
            "Ino. time [min]": cross_enz_ino_time,
            "Ino. temp. [°C]": cross_enz_ino_temp,
            "stirring [RPM]": cross_enz_stirring,
        }

        # Create Combined Excel File and Download
        st.subheader("Create Combined Excel File and Download")
        if st.button("Create and Download Excel File"):
            if st.session_state.all_data:
                try:
                    # Create a single-row DataFrame from all_data
                    df = pd.DataFrame([st.session_state.all_data])

                    # Flatten the MultiIndex
                    df.columns = [" - ".join(col).strip() for col in df.columns]

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

    # ==========================================================
    # Main app logic: Render different pages based on session state
    # ==========================================================

    if st.session_state.page == "welcome":
        show_welcome_page()
    elif st.session_state.page == "experiments_type_1":
        show_experiments_type_1()

if __name__ == "__main__":
    main()
