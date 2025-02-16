import streamlit as st
import subprocess
import os

# (Optional) Load .env file if using python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # If python-dotenv isn't installed, environment variables should still work

st.set_page_config(layout="wide")

# Get credentials from environment variables
USERNAME = os.getenv("STREAMLIT_USERNAME", "admin")  # Default: "admin"
PASSWORD = os.getenv("STREAMLIT_PASSWORD", "password")  # Default: "password"

# --- USER AUTHENTICATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login function
def login():
    if st.session_state.username == USERNAME and st.session_state.password == PASSWORD:
        st.session_state.logged_in = True
        st.rerun()
    else:
        st.error("Invalid username or password")

# Logout function
def logout():
    st.session_state.logged_in = False
    st.rerun()

# Show login form if not logged in
if not st.session_state.logged_in:
    st.title("Login Required")
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")
    if st.button("Login"):
        login()
    st.stop()

# --- MAIN CONTENT (Only visible after login) ---
st.title("Simple Terminal Inside Streamlit")

st.subheader("Basic Terminal")
command = st.text_input("Enter a command:", "ls -la")

if st.button("Run Command"):
    output = subprocess.getoutput(command)
    st.text_area("Output:", output, height=300)

# --- LOGOUT BUTTON ---
if st.button("Logout"):
    logout()
