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
    st.session_state.page = "login"

if 'experiment_data' not in st.session_state:
    st.session_state.experiment_data = []

def login_page():
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
    st.title(f"Welcome, {st.session_state.current_user}")
    experiments = st.session_state.user_data[st.session_state.current_user]["experiments"]
    if experiments:
        st.subheader("Your Saved Experiments")
        for i, exp in enumerate(experiments):
            exp_name = exp.get("experiment_name", f"Experiment {i + 1}")
            if st.button(f"Edit {exp_name}", key=f"edit_{i}"):
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
    st.title("Experiment Type 1 Data Collection")
    experiment_name = st.text_input("Experiment Name", value=st.session_state.get("experiment_name", ""), key="experiment_name")
    st.session_state.experiment_name = experiment_name
    
    with st.form(key="experiment_form"):
        st.subheader("Procedure - Settings")
        col1, col2 = st.columns(2)
        with col1:
            procedure_num = st.text_input("#Num", placeholder="1-Infinity", key="procedure_num")
        with col2:
            procedure_date = st.date_input("Date", value=datetime.now(), key="procedure_date")
        
        st.subheader("Procedure - Enzymes Crosslinking")
        cross_enz_name = st.selectbox("Name", ["Crosslinker X", "Crosslinker Y"], key="cross_enz_name")
        
        col1, col2 = st.columns(2)
        with col1:
            cross_enz_num = st.text_input("Enz num.", placeholder="Number (If used) or N/A", key="cross_enz_num")
        with col2:
            cross_enz_concentration = st.text_input("Concentration [%]", placeholder="Number (If used) or N/A", key="cross_enz_concentration")
        
        if st.form_submit_button("Save Form"):
            form_data = {
                "Experiment Name": experiment_name,
                "Procedure - Enzymes Crosslinking - Name": cross_enz_name,
                "Procedure - Enzymes Crosslinking - Enz num.": cross_enz_num,
                "Procedure - Enzymes Crosslinking - Concentration [%]": cross_enz_concentration,
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
            st.download_button(
                label=f"Download {file_name}",
                data=excel_buffer,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        if st.button("Save Experiment"):
            experiment_data = {
                "experiment_name": st.session_state.experiment_name,
                "rows": st.session_state.experiment_data,
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
