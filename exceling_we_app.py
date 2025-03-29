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

if 'experiments' not in st.session_state:
    st.session_state.experiments = []  # Stores all experiment rows


def login_page():
    """Login page for user authentication."""
    st.title("Welcome to the Lab Data Collection App")
    email = st.text_input("Enter your email address", key="email")

    if st.button("Login"):
        if email:
            st.session_state.current_user = email
            if email not in st.session_state.user_data:
                # Initialize user data if first login
                st.session_state.user_data[email] = {"experiments": []}
            st.success(f"Welcome back, {email}!")
            st.rerun()  # Updated method to rerun the app
        else:
            st.error("Please enter a valid email address.")


def welcome_page():
    """Welcome page after login."""
    st.title(f"Welcome, {st.session_state.current_user}")

    # Display saved experiments
    if st.session_state.user_data[st.session_state.current_user]["experiments"]:
        st.subheader("Your Saved Experiments")
        for i, exp in enumerate(st.session_state.user_data[st.session_state.current_user]["experiments"]):
            exp_name = exp.get("experiment_name", f"Experiment {i + 1}")
            if st.button(f"Edit {exp_name}", key=f"edit_{i}"):
                # Load experiment into session state for editing
                st.session_state.experiments = exp["rows"]
                experiment_form(exp_name)

    # Button to start a new experiment
    if st.button("Start New Experiment"):
        experiment_form()


def experiment_form(exp_name=None):
    """Form to fill experiment details."""
    if exp_name is None:
        exp_name = st.text_input("Enter Experiment Name", key="experiment_name")
        user_name = st.text_input("Enter Your Name", key="user_name")

    # Add rows dynamically
    if "rows" not in st.session_state:
        st.session_state.rows = []

    with st.form(key="experiment_form"):
        # Add input fields for a single row
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

        if st.form_submit_button(label="Save Row"):
            row_data = {
                "#Num": procedure_num,
                "Date": procedure_date.strftime("%Y-%m-%d"),
                "Labeling": procedure_labeling,
                "Protein type": protein_type,
                "Concentration [wt/wt%]": protein_concentration,
            }
            st.session_state.rows.append(row_data)
            st.success("Row added successfully!")

    # Display saved rows
    if st.session_state.rows:
        df = pd.DataFrame(st.session_state.rows)
        st.write(df)

        # Save experiment
        if exp_name and user_name and st.button("Save Experiment"):
            experiment_data = {
                "experiment_name": exp_name,
                "user_name": user_name,
                "rows": st.session_state.rows,
            }
            current_email = st.session_state.current_user
            if current_email:
                st.session_state.user_data[current_email]["experiments"].append(experiment_data)
                st.success(f"Experiment '{exp_name}' saved successfully!")
                # Reset rows for next experiment
                del st.session_state.rows

    # Export to Excel
    if df is not None and not df.empty and exp_name and user_name and st.button("Export to Excel"):
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name=exp_name)

        excel_buffer.seek(0)
        file_name = f"{exp_name.replace(' ', '_')}_data.xlsx"

        # Download button for Excel file
        st.download_button(
            label=f"Download {file_name}",
            data=excel_buffer,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


# Main app logic
if not st.session_state.current_user:
    login_page()
else:
    welcome_page()
