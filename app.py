import streamlit as st
import subprocess

st.set_page_config(layout="wide")

# --- USER AUTHENTICATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login function
def login():
    if st.session_state.username == "admin" and st.session_state.password == "password":  # Change credentials as needed
        st.session_state.logged_in = True
        st.experimental_rerun()
    else:
        st.error("Invalid username or password")

# Logout function
def logout():
    st.session_state.logged_in = False
    st.experimental_rerun()

# Show login form if not logged in
if not st.session_state.logged_in:
    st.title("Login Required")
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")
    if st.button("Login"):
        login()
    st.stop()  # Stop execution until logged in

# --- MAIN CONTENT (Only visible after login) ---
st.title("Simple Terminal Inside Streamlit")

# --- TERMINAL SECTION ---
st.subheader("Basic Terminal")

command = st.text_input("Enter a command:", "ls -la")

if st.button("Run Command"):
    output = subprocess.getoutput(command)
    st.text_area("Output:", output, height=300)

# --- LOGOUT BUTTON ---
if st.button("Logout"):
    logout()
