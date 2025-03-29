# %%writefile app.py
import streamlit as st
import pandas as pd
import io
from datetime import datetime

# Initialize session state for user data
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'page' not in st.session_state:
    st.session_state.page = "login"  # Controls app navigation

if 'experiment_data' not in st.session_state:
    st.session_state.experiment_data = []

def login_page():
    """Enhanced login page."""
    st.title("Welcome to the Lab Data Collection App")

    email = st.text_input("Enter your email address", key="email")
    if st.button("Login"):
        if email:
            st.session_state.current_user = email
            st.session_state.user_data.setdefault(email, {"experiments": []})
            st.session_state.page = "welcome"
            st.rerun()
        else:
            st.error("Please enter a valid email address.")

def welcome_page():
    """Improved welcome page."""
    st.title(f"Welcome, {st.session_state.current_user}")

    experiments = st.session_state.user_data[st.session_state.current_user]["experiments"]
    if experiments:
        st.subheader("My Experiments")
        # Sort experiments by date
        sorted_experiments = sorted(experiments, key=lambda x: x.get("date", datetime.now().isoformat()), reverse=True)

        for i, exp in enumerate(sorted_experiments):
            exp_name = exp.get("experiment_name", f"Experiment {i + 1}")
            exp_date = exp.get("date", datetime.now().isoformat())[:10]  # Extract just the date part

            if st.button(f"Edit: {exp_name} (Date: {exp_date})", key=f"edit_{i}"):
                st.session_state.experiment_name = exp_name
                st.session_state.experiment_data = exp["rows"]
                st.session_state.page = "experiment_form"
                st.rerun()

    if st.button("Start New Experiment"):
        st.session_state.experiment_name = ""
        st.session_state.experiment_data = []
        st.session_state.page = "experiment_form"
        st.rerun()

def experiment_form():
    """Form to collect experiment details."""
    st.title("Experiment Type 1 Data Collection")
    if st.button("Back to Home", key="back_home"):
        st.session_state.page = "welcome"
        st.rerun()

    experiment_name = st.text_input("Experiment Name", value=st.session_state.get("experiment_name", ""))
    st.session_state.experiment_name = experiment_name

    with st.form(key="experiment_form"):
        st.subheader("Procedure - Settings")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            procedure_num = st.text_input("#Num", placeholder="1-Infinity", key="procedure_num")
        with col2:
            procedure_date = st.date_input("Date", value=datetime.now(), key="procedure_date")
        with col3:
            procedure_labeling = st.text_input("Labeling", key="procedure_labeling")
        with col4:
            protein_type = st.selectbox("Protein type", ["Type A", "Type B", "Type C"], key="protein_type")
        with col5:
            protein_concentration = st.text_input("Concentration [wt/wt%]", key="protein_concentration")

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

        st.subheader("Black box ? + Procedure - Enzymes Hydrolyzing")
        col1, col2 = st.columns(2)
        with col1:
            enz_YN = st.selectbox("Y/N", ["Yes", "No"], key="enz_YN")
        with col2:
            enz_num = st.text_input("Enz num.", placeholder="Number (If used) or N/A", key="enz_num")

        enz_name = st.selectbox("Name", ["Enzyme A", "Enzyme B"], key="enz_name")

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

        st.subheader("Procedure - Enzymes Crosslinking")
        cross_enz_name = st.selectbox("Name", ["Crosslinker X", "Crosslinker Y"], key="cross_enz_name")

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

        if st.form_submit_button("Save Form"):
            form_data = {
                "#Num": procedure_num,
                "Date": procedure_date.strftime("%Y-%m-%d"),
                "Labeling": procedure_labeling,
                "Protein type": protein_type,
                "Concentration [wt/wt%]": protein_concentration,

                "Right valve [bar]": right_valve,
                "Left valve 2 [bar]": left_valve,
                "Temp after HPH [°C]": temp_after_HPH,
                "HPH fraction [%]": HPH_fraction,
                "Initial water temp": initial_water_temp,
                "Mixing temp[°C]": mixing_temp,
                "Mixing time": mixing_time,
                "Heat treatment fraction[%]": heat_treatment_fraction,
                "pH": ph,

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

                "Crosslinker Name": cross_enz_name,
                "Crosslinker Enz num.": cross_enz_num,
                "Crosslinker Concentration [%]": cross_enz_concentration,
                "Crosslinker Added enz [g]": cross_enz_added,
                "Crosslinker Addition temp [°C]": cross_enz_addition_temp,
                "Crosslinker Ino. time [min]": cross_enz_ino_time,
                "Crosslinker Ino. temp. [°C]": cross_enz_ino_temp,
                "Crosslinker stirring [RPM]": cross_enz_stirring,
            }
            st.session_state.experiment_data.append(form_data)
            st.success("Form saved successfully!")

    if st.session_state.experiment_data:
        df = pd.DataFrame(st.session_state.experiment_data)
        st.write(df)

        if st.button("Export to Excel"):
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=st.session_state.experiment_name or "Experiment", index=False)
            excel_buffer.seek(0)

            file_name = f"{st.session_state.experiment_name.replace(' ', '_')}_data.xlsx"
            try:
                st.download_button(
                    label=f"Download {file_name}",
                    data=excel_buffer.getvalue(),
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Error creating/downloading Excel file: {e}")

        if st.button("Save Experiment"):
            experiment_data = {
                "experiment_name": st.session_state.experiment_name,
                "rows": st.session_state.experiment_data,
                "date": datetime.now().isoformat()  # Save the current date
            }
            st.session_state.user_data[st.session_state.current_user]["experiments"].append(experiment_data)
            st.success("Experiment saved successfully!")
            st.session_state.page = "welcome"
            st.rerun()

# Main app logic
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "welcome":
    welcome_page()
elif st.session_state.page == "experiment_form":
    experiment_form()
