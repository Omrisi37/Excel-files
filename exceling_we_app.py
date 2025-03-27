# %%writefile app.py
import streamlit as st
import pandas as pd
import io
from datetime import datetime
from PIL import Image
import os  # Import os module

def main():
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "welcome"

    # ==========================================================
    # Load Images
    # ==========================================================
    image_path = "lab.jpg"  # Or "images/lab_equipment.jpg" if it's in a subdirectory
    if os.path.exists(image_path):  # Check if the image exists
        try:
            lab_image = Image.open(image_path)
        except Exception as e:
            st.warning(f"Error loading image from repo: {e}")
            lab_image = None
    else:
        st.warning("Image not found in the repository.")
        lab_image = None

   # ==========================================================
    # CSS for Background Image
    # ==========================================================
    st.markdown(
        f"""
        <style>
        body {{
            background-image: url("https://github.com/EliavLavi/excel-files/blob/main/lab_equipment.jpg?raw=true");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            margin: 0; /* Reset default body margin */
            height: 100vh; /* Ensure full height */
            overflow: hidden; /* Hide scrollbars */
        }}

        .app-content {{
            position: relative; /* Required for z-index */
            z-index: 1; /* Place content above the shade */
            padding: 20px; /* Add padding */
            background: rgba(255, 255, 255, 0.7); /* Semi-transparent white background for content */
            border-radius: 10px; /* Optional: round corners */
        }}

        body::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.3); /* Adjust the last value (alpha) for the shade */
            z-index: -1; /* Place the shade behind the content */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    # ==========================================================
    # Functions to switch between pages
    # ==========================================================
    def show_welcome_page():
        st.title("Welcome to the Lab Data Collection App")
        st.markdown("A tool for streamlined data entry and management in laboratory experiments.")

        # Display image if available
        if lab_image:
            st.image(lab_image, caption="Lab Equipment", width=400)  # Adjust width as needed
        else:
            st.write("Lab Image Not Available.")
        st.write("Choose a protocol to begin:")

        # Button to Experiments Type 1
        col1, col2, col3 = st.columns([1, 3, 1])  # Adjust column widths for centering
        with col2:
            if st.button("Experiments Type 1", use_container_width=True):
                st.session_state.page = "experiments_type_1"
                st.rerun()

    def show_experiments_type_1():
        st.title("Experiments Type 1 Data Collection")

        # Button to go back to welcome page
        if st.button("Back to Welcome Page"):
            st.session_state.page = "welcome"
            st.rerun()

        # Initialize session state
        if 'all_data' not in st.session_state:
            st.session_state.all_data = {}

        # ==========================================================
        # Form for "Experiments Type 1"
        # ==========================================================
        with st.form(key='experiment_form'):
            # 1. Procedure - Settings
            st.subheader("Procedure - Settings")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                procedure_num = st.text_input("#Num", placeholder="1-Infinity", key="procedure_num")
            with col2:
                procedure_date = st.date_input("Date", value=datetime.now(), key="procedure_date")
            with col3:
                procedure_labeling = st.text_input("Labeling", key="procedure_labeling")
            with col4:
                protein_type = st.selectbox("Protein type", ["", "Type A", "Type B", "Type C"], index=0, key="protein_type")
            with col5:
                protein_concentration = st.text_input("Concentration [wt/wt%]", key="protein_concentration")

            # 2. Procedure - Physical Treatments
            st.subheader("Procedure - Physical Treatments")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                right_valve = st.text_input("Right valve [bar]", placeholder="Number (If used) or N/A", key="right_valve")
            with col2:
                left_valve = st.text_input("Left valve 2 [bar]", placeholder="Number (If used) or N/A", key="left_valve")
            with col3:
                temp_after_HPH = st.text_input("Temp after HPH [°C]", placeholder="Number (If used) or N/A", key="temp_after_HPH")
            with col4:
                HPH_fraction = st.text_input("HPH fraction [%]", placeholder="Number (If used) or N/A", key="HPH_fraction")

            col1, col2 = st.columns(2)
            with col1:
                initial_water_temp = st.text_input("Initial water temp", placeholder="Number (If used) or N/A", key="initial_water_temp")
            with col2:
                acid_name = st.text_input("Acid name", placeholder="Name (If used) or N/A", key="acid_name")

            col1, col2 = st.columns(2)
            with col1:
                mixing_temp = st.text_input("Mixing temp[°C]", placeholder="Number (If used) or N/A", key="mixing_temp")
            with col2:
                mixing_time = st.text_input("Mixing time", placeholder="Number (If used) or N/A", key="mixing_time")
            heat_treatment_fraction = st.text_input("Heat treatment fraction[%]", placeholder="Number (If used) or N/A", key="heat_treatment_fraction")
            ph = st.text_input("pH", placeholder="Number (If used) or N/A", key="ph")

            # 3. Black box ? + Procedure - Enz Hydro
            st.subheader("Black box ? + Procedure - Enzymes Hydrolyzing")
            col1, col2 = st.columns(2)
            with col1:
                enz_YN = st.selectbox("Y/N", ["", "Yes", "No"], index=0, key="enz_YN")
            with col2:
                enz_num = st.text_input("Enz num.", placeholder="Number (If used) or N/A", key="enz_num")

            enz_name = st.selectbox("Name", ["", "Enzyme A", "Enzyme B"], index=0, key="enz_name")

            col1, col2 = st.columns(2)
            with col1:
                enz_concentration = st.text_input("Concentration [%]", placeholder="Number (If used) or N/A", key="enz_concentration")
            with col2:
                enz_added = st.text_input("Added enz [g]", placeholder="Number (If used) or N/A", key="enz_added")

            col1, col2 = st.columns(2)
            with col1:
                enz_addition_temp = st.text_input("Addition temp [°C]", placeholder="Number (If used) or N/A", key="enz_addition_temp")
            with col2:
                enz_ino_time = st.text_input("Ino. time [min]", placeholder="Number (If used) or N/A", key="enz_ino_time")

            col1, col2 = st.columns(2)
            with col1:
                enz_ino_temp = st.text_input("Ino. temp. [°C]", placeholder="Number (If used) or N/A", key="enz_ino_temp")
            with col2:
                enz_stirring = st.text_input("stirring [RPM]", placeholder="Number (If used) or N/A", key="enz_stirring")
            black_box_protein_fraction = st.text_input("black box protein fraction[%]", placeholder="Number (If used) or N/A", key="black_box_protein_fraction")

            # 4. Procedure - Enz Cross
            st.subheader("Procedure - Enzymes Crosslinking")
            col1, col2 = st.columns(2)
            with col1:
                cross_enz_name = st.selectbox("Name", ["", "Crosslinker X", "Crosslinker Y"], index = 0, key="cross_enz_name")

            col1, col2 = st.columns(2)
            with col1:
                cross_enz_num = st.text_input("Enz num.", placeholder="Number (If used) or N/A", key="cross_enz_num")
            with col2:
                cross_enz_concentration = st.text_input("Concentration [%]", placeholder="Number (If used) or N/A", key="cross_enz_concentration")

            col1, col2 = st.columns(2)
            with col1:
                cross_enz_added = st.text_input("Added enz [g]", placeholder="Number (If used) or N/A", key="cross_enz_added")
            with col2:
                cross_enz_addition_temp = st.text_input("Addition temp [°C]", placeholder="Number (If used) or N/A", key="cross_enz_addition_temp")

            col1, col2 = st.columns(2)
            with col1:
                cross_enz_ino_time = st.text_input("Ino. time [min]", placeholder="Number (If used) or N/A", key="cross_enz_ino_time")
            with col2:
                cross_enz_ino_temp = st.text_input("Ino. temp. [°C]", placeholder="Number (If used) or N/A", key="cross_enz_ino_temp")
            cross_enz_stirring = st.text_input("stirring [RPM]", placeholder="Number (If used) or N/A", key="cross_enz_stirring")

            submit_button = st.form_submit_button(label='Save Data')

        # ==========================================================
        # Data Collection and Submission
        # ==========================================================
        if submit_button:
            st.session_state.all_data = {
                'Procedure - Settings': {
                    "#Num": procedure_num,
                    "Date": procedure_date.strftime("%Y-%m-%d"),
                    "Labeling": procedure_labeling,
                    "Protein type": protein_type,
                    "Concentration [wt/wt%]": protein_concentration,
                },
                'Procedure - Physical Treatments': {
                    "Right valve [bar]": right_valve,
                    "Left valve 2 [bar]": left_valve,
                    "Temp after HPH [°C]": temp_after_HPH,
                    "HPH fraction [%]": HPH_fraction,
                    "Initial water temp": initial_water_temp,
                    "Mixing temp[°C]": mixing_temp,
                    "Mixing time": mixing_time,
                    "Heat treatment fraction[%]": heat_treatment_fraction,
                    "pH": ph,
                },
                'Black box ? + Procedure - Enz Hydro': {
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
                },
                'Procedure - Enz Cross': {
                    "Enz num.": cross_enz_num,
                    "Name": cross_enz_name,
                    "Concentration [%]": cross_enz_concentration,
                    "Added enz [g]": cross_enz_added,
                    "Addition temp [°C]": cross_enz_addition_temp,
                    "Ino. time [min]": cross_enz_ino_time,
                    "Ino. temp. [°C]": cross_enz_ino_temp,
                    "stirring [RPM]": cross_enz_stirring,
                }
            }
            st.success("Data saved!")

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
