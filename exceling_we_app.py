# %%writefile app.py
import streamlit as st
import pandas as pd
import io
from datetime import datetime

# Initialize session state for user data
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}  # Stores user-specific data

if 'current_user' not in st.session_state:
    st.session_state.current_user = None  # Tracks logged-in user


def login_page():
    """Enhanced login page."""
    st.title("Welcome to the Lab Data Collection App")

    # Email input for login
    email = st.text_input("Enter your email address", key="email")
    if st.button("Login"):
        if email:
            st.session_state.current_user = email
            if email not in st.session_state.user_data:
                st.session_state.user_data[email] = {"experiments": []}
            st.success(f"Logged in as {email}!")
            st.rerun()  # Rerun to show the welcome page
        else:
            st.error("Please enter a valid email address.")


def welcome_page():
    """Improved welcome page."""
    st.title(f"Welcome, {st.session_state.current_user}")

    # Display saved experiments, if any
    if st.session_state.user_data[st.session_state.current_user]["experiments"]:
        st.subheader("Your Saved Experiments")
        for i, exp in enumerate(st.session_state.user_data[st.session_state.current_user]["experiments"]):
            exp_name = exp.get("experiment_name", f"Experiment {i + 1}")
            if st.button(f"Edit {exp_name}", key=f"edit_{i}"):
                # Load the experiment data into session state for editing
                st.session_state.experiment_name = exp_name
                st.session_state.experiment_data = exp["rows"]
                experiment_form()  # Pass experiment name to form
    # Button to start a new experiment
    if st.button("Start New Experiment"):
        st.session_state.experiment_data = []
        experiment_form()  # Start a new experiment form


def experiment_form():
    """Form to collect experiment details with each submission as a new entry."""
    st.title("Experiment Type 1 Data Collection")

    # Experiment name input
    if 'experiment_name' not in st.session_state:
        st.session_state.experiment_name = st.text_input("Experiment Name", key="experiment_name")

    # Form submission
    with st.form(key="experiment_form"):
        # Input fields for a single form
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            procedure_num = col1.text_input("#Num", placeholder="1-Infinity")
        with col2:
            procedure_date = col2.date_input("Date", value=datetime.now())
        with col3:
            procedure_labeling = col3.text_input("Labeling")
        with col4:
            protein_type = col4.selectbox("Protein type", ["Type A", "Type B", "Type C"])
        with col5:
            protein_concentration = col5.text_input("Concentration [wt/wt%]")

        # Save this form submission
        if st.form_submit_button("Save Form"):
            form_data = {
                "#Num": procedure_num,
                "Date": procedure_date.strftime("%Y-%m-%d"),
                "Labeling": procedure_labeling,
                "Protein type": protein_type,
                "Concentration [wt/wt%]": protein_concentration,
            }
            # Save the form data in the current experiment
            if 'experiment_data' not in st.session_state:
                st.session_state.experiment_data = []

            st.session_state.experiment_data.append(form_data)
            st.success("Form saved successfully!")

    # Export to Excel
    if st.session_state.experiment_data:
        df = pd.DataFrame(st.session_state.experiment_data)
        st.write(df)
        # Button to export all saved forms to Excel
        if st.button("Export to Excel"):
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=st.session_state.experiment_name, index=False)
            excel_buffer.seek(0)  # Reset buffer to the beginning

            # Filename and download button
            file_name = f"{st.session_state.experiment_name.replace(' ', '_')}_data.xlsx"
            st.download_button(
                label=f"Download {file_name}",
                data=excel_buffer,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Save experiment for later editing
        if st.button("Save Experiment"):
            experiment_data = {
                "experiment_name": st.session_state.experiment_name,
                "rows": st.session_state.experiment_data,
            }
            # Save to user data
            if st.session_state.current_user not in st.session_state.user_data:
                st.session_state.user_data[st.session_state.current_user] = {"experiments": []}

            st.session_state.user_data[st.session_state.current_user]["experiments"].append(experiment_data)
            st.success("Experiment saved successfully!")
            del st.session_state.experiment_data
            st.rerun()


# Main app logic
if not st.session_state.current_user:
    login_page()
else:
    welcome_page()
