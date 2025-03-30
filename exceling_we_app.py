# %%writefile app.py
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import io

# Initialize session state for user data
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'page' not in st.session_state:
    st.session_state.page = "login"  # Controls app navigation

if 'experiment_data' not in st.session_state:
    st.session_state.experiment_data = []

# Database setup
DB_FILE = "experiments.db"

def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            experiment_name TEXT,
            date TEXT,
            data TEXT,
            FOREIGN KEY (email) REFERENCES users (email)
        )
    """)
    conn.commit()
    conn.close()

def save_experiment_to_db(email, experiment_name, date, data):
    """Save experiment data to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO experiments (email, experiment_name, date, data) VALUES (?, ?, ?, ?)", 
                   (email, experiment_name, date, data))
    conn.commit()
    conn.close()

def get_experiments_from_db(email):
    """Retrieve all experiments for a specific user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, experiment_name, date, data FROM experiments WHERE email = ?", (email,))
    experiments = cursor.fetchall()
    conn.close()
    return experiments

def update_experiment_in_db(exp_id, experiment_name, data):
    """Update an existing experiment in the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE experiments SET experiment_name = ?, data = ? WHERE id = ?", 
                   (experiment_name, data, exp_id))
    conn.commit()
    conn.close()

def login_page():
    """Enhanced login page."""
    st.title("Welcome to the Lab Data Collection App")

    email = st.text_input("Enter your email address", key="email")
    
    if st.button("Login"):
        if email:
            # Save user to DB if not already present
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO users (email) VALUES (?)", (email,))
            conn.commit()
            conn.close()

            # Set current user and navigate to welcome page
            st.session_state.current_user = email
            st.session_state.page = "welcome"
            st.rerun()
        else:
            st.error("Please enter a valid email address.")

def welcome_page():
    """Improved welcome page."""
    st.title(f"Welcome, {st.session_state.current_user}")

    # Fetch experiments from DB
    experiments = get_experiments_from_db(st.session_state.current_user)
    
    if experiments:
        st.subheader("My Experiments")
        for exp_id, exp_name, exp_date, exp_data in sorted(experiments, key=lambda x: x[2], reverse=True):
            if st.button(f"Edit: {exp_name} (Date: {exp_date})", key=f"edit_{exp_id}"):
                # Load experiment into session state for editing
                st.session_state.experiment_id = exp_id
                st.session_state.experiment_name = exp_name
                st.session_state.experiment_data = eval(exp_data)  # Convert string back to Python object
                st.session_state.page = "experiment_form"
                st.rerun()

    if st.button("Start New Experiment"):
        st.session_state.experiment_id = None  # New experiment has no ID yet
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
    
    with st.form(key="experiment_form"):
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

        if st.form_submit_button("Save Form"):
            form_data = {
                "#Num": procedure_num,
                "Date": procedure_date.strftime("%Y-%m-%d"),
                "Labeling": procedure_labeling,
                "Protein type": protein_type,
                "Concentration [wt/wt%]": protein_concentration,
            }
            st.session_state.experiment_data.append(form_data)
            st.success("Form saved successfully!")

    if st.session_state.experiment_data:
        df = pd.DataFrame(st.session_state.experiment_data)
        st.write(df)

        if st.button("Export to Excel"):
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=experiment_name or "Experiment", index=False)
            
            excel_buffer.seek(0)

            file_name = f"{experiment_name.replace(' ', '_')}_data.xlsx"
            
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
            # Save or update the experiment in DB
            serialized_data = str(st.session_state.experiment_data)  # Convert list to string for storage
            
            if 'experiment_id' in st.session_state and st.session_state.experiment_id is not None:
                update_experiment_in_db(st.session_state.experiment_id, experiment_name, serialized_data)
                st.success(f"Experiment '{experiment_name}' updated successfully!")
            else:
                save_experiment_to_db(st.session_state.current_user, experiment_name, datetime.now().isoformat(), serialized_data)
                st.success(f"Experiment '{experiment_name}' saved successfully!")
            
            # Navigate back to home page after saving
            del st.session_state.experiment_id  # Reset ID for next use
            del st.session_state.experiment_data  # Clear current session's data
            del st.session_state.experiment_name  # Clear current session's name
            
            st.session_state.page = "welcome"
            st.rerun()

# Initialize database on startup
init_db()

# Main app logic
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "welcome":
    welcome_page()
elif st.session_state.page == "experiment_form":
    experiment_form()
