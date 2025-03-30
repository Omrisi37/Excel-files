# %%writefile app.py
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import io

# --- SESSION STATE INITIALIZATION ---
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'page' not in st.session_state:
    st.session_state.page = "login"  # Controls app navigation

if 'experiment_data' not in st.session_state:
    st.session_state.experiment_data = []

# --- DATABASE SETUP ---
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
            experiment_type TEXT,
            experiment_name TEXT,
            date TEXT,
            data TEXT,
            FOREIGN KEY (email) REFERENCES users (email)
        )
    """)
    conn.commit()
    conn.close()

def save_experiment_to_db(email, experiment_type, experiment_name, date, data):
    """Save experiment data to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO experiments (email, experiment_type, experiment_name, date, data) VALUES (?, ?, ?, ?, ?)", 
                   (email, experiment_type, experiment_name, date, data))
    conn.commit()
    conn.close()

def get_experiments_from_db(email):
    """Retrieve all experiments for a specific user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, experiment_type, experiment_name, date, data FROM experiments WHERE email = ?", (email,))
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

# --- CSS STYLES ---
def set_page_style():
    st.markdown(
        """
        <style>
            /* General styles */
            body {
                font-family: 'Roboto', sans-serif;
                background-color: #f5f6fa; /* Light background color */
                color: #333;
                margin: 0;
                padding: 0;
            }
            .stApp {
                max-width: 1400px;
                margin: 20px auto;
                padding: 20px;
                background-color: #ffffff; /* White background */
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
            }
            /* Sidebar styles */
            .css-1adrbqk {
                background-color: #f0f2f6; /* Sidebar background color */
                padding: 20px;
                border-radius: 10px;
            }
            /* Titles */
            h1, h2, h3, h4, h5, h6 {
                color: #37474f; /* Dark gray for titles */
            }
            /* Buttons */
            .stButton > button {
                color: #ffffff; /* White text */
                background-color: #007bff; /* Primary blue color */
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            .stButton > button:hover {
                background-color: #0056b3; /* Darker blue on hover */
            }
            /* Forms */
            .stForm {
                background-color: #ffffff; /* White form background */
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle form shadow */
            }
            .stTextInput > label, .stNumberInput > label, .stSelectbox > label, .stDateInput > label {
                color: #37474f; /* Dark gray labels */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- PAGE FUNCTIONS ---
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

    experiment_type = st.selectbox("Choose Experiment Type", ["Type 1"], key="experiment_type_select")

    # Fetch experiments from DB
    try:
        experiments = get_experiments_from_db(st.session_state.current_user)
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return

    if experiments:
        st.subheader("My Experiments")
        for exp_id, exp_type, exp_name, exp_date, exp_data in sorted(experiments, key=lambda x: x[3], reverse=True):
            if st.button(f"Edit: {exp_name} ({exp_type}, Date: {exp_date})", key=f"edit_{exp_id}"):
                st.session_state.experiment_id = exp_id
                st.session_state.experiment_type = exp_type
                st.session_state.experiment_name = exp_name
                st.session_state.experiment_data = eval(exp_data)  # Convert string back to Python object
                st.session_state.page = "experiment_form"
                st.rerun()

    if st.button("Start New Experiment"):
        st.session_state.experiment_id = None
        st.session_state.experiment_type = experiment_type
        st.session_state.experiment_name = ""
        st.session_state.experiment_data = []
        st.session_state.page = "experiment_form"
        st.rerun()

def experiment_form():
    """Form to collect experiment details."""
    st.title(f"Experiment {st.session_state.experiment_type} Data Collection")

    if st.button("Back to Home", key="back_home"):
        st.session_state.page = "welcome"
        st.rerun()

    experiment_name = st.text_input("Experiment Name", value=st.session_state.get("experiment_name", ""))
    
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
        col1, col2 = st.columns(2)
        with col1:
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
            cross_enz_ino_time = st.text_input("Inc. time [min]", placeholder="Number (If used) or N/A", key="cross_enz_ino_time")
        with col2:
            cross_enz_ino_temp = st.text_input("Inc. temp. [°C]", placeholder="Number (If used) or N/A", key="cross_enz_ino_temp")
        cross_enz_stirring = st.text_input("stirring [RPM]", placeholder="Number (If used) or N/A", key="cross_enz_stirring")

        st.subheader("Gel / Drying process")
        col1, col2 = st.columns(2)
        with col1:
            gel_or_drying = st.selectbox("G/D", ["Drying", "Gel"], key="gel_or_drying")

        col1, col2 = st.columns(2)
        with col1:
           o_n_incubation = st.selectbox("o.n incubation at 4 °C (Y/N)", ["Yes", "No"], key="o_n_incubation")
        with col2:
            drying_method = st.selectbox("Drying type", ["Freeze dry", "Spray dry","N/A"], key="drying_method")

                # Gel Functionality Section
        st.subheader("Gel Functionality")
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 1.5, 1.5, 2, 2, 2, 2])
        with col1:
            fresh_rehydrated = st.text_input(
                "Fresh/rehydrated", 
                placeholder="Enter value", 
                key="fresh_rehydrated",
                help="Specify whether the gel is fresh or rehydrated."
            )
        with col2:
            added_protein = st.text_input(
                "Added protein?", 
                placeholder="Number (if used) or N/A", 
                key="added_protein",
                help="Enter the amount of added protein or specify 'N/A'."
            )
        with col3:
            added_protein_type = st.text_input(
                "Added protein type", 
                placeholder="Type (if used) or N/A", 
                key="added_protein_type",
                help="Specify the type of added protein or 'N/A'."
            )
        with col4:
            meal_water_ratio = st.text_input(
                "Meal:water:added protein ratio", 
                placeholder="Ratio (if used) or N/A", 
                key="meal_water_ratio",
                help="Provide the ratio of meal to water to added protein."
            )
        with col5:
            rehydration_equipment = st.text_input(
                "Rehydration equipment", 
                placeholder="Enter equipment", 
                key="rehydration_equipment",
                help="Specify the equipment used for rehydration."
            )
        with col6:
            stress_max_load = st.text_input(
                "Stress at Maximum Load (KPa)", 
                placeholder="Insert average stress", 
                key="stress_max_load",
                help="Enter the average stress at maximum load in KPa."
            )
        with col7:
            strain_max_load = st.text_input(
                "Percentage Strain at Maximum Load", 
                placeholder="Insert average strain", 
                key="strain_max_load",
                help="Enter the average strain percentage at maximum load."
            )
        
        # TPA & Sensory Tests Section
        st.subheader("TPA & Sensory Tests")
        col1, col2, col3, col4, col5, col6 = st.columns([1.5, 1.5, 1.5, 1.5, 1.5, 1.5])
        with col1:
            tpa1 = st.text_input(
                "TPA1", 
                placeholder="Enter TPA1 value", 
                key="tpa1",
                help="Enter the first TPA (Texture Profile Analysis) value."
            )
        with col2:
            tpa = st.text_input(
                "TPA", 
                placeholder="Enter TPA value", 
                key="tpa",
                help="Enter the second TPA (Texture Profile Analysis) value."
            )
        with col3:
            chewiness = st.text_input(
                "Chewiness", 
                placeholder="Enter chewiness value", 
                key="chewiness",
                help="Provide a chewiness score based on sensory analysis."
            )
        with col4:
            hardness = st.text_input(
                "Hardness", 
                placeholder="Enter hardness value", 
                key="hardness",
                help="Provide a hardness score based on sensory analysis."
            )
        with col5:
            juiciness = st.text_input(
                "Juiciness", 
                placeholder="Enter juiciness value", 
                key="juiciness",
                help="Provide a juiciness score based on sensory analysis."
            )
        with col6:
            mushiness = st.text_input(
                "Mushiness", 
                placeholder="Enter mushiness value", 
                key="mushiness",
                help="Provide a mushiness score based on sensory analysis."
            )

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
                save_experiment_to_db(st.session_state.current_user, st.session_state.experiment_type, experiment_name, datetime.now().isoformat(), serialized_data)
                st.success(f"Experiment '{experiment_name}' saved successfully!")
            
            # Navigate back to home page after saving
            del st.session_state.experiment_id  # Reset ID for next use
            del st.session_state.experiment_data  # Clear current session's data
            del st.session_state.experiment_name  # Clear current session's name
            
            st.session_state.page = "welcome"
            st.rerun()

# Initialize database on startup
init_db()

# Set page style
set_page_style()

# Main app logic
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "welcome":
    welcome_page()
elif st.session_state.page == "experiment_form":
    experiment_form()
