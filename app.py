import streamlit as st
import subprocess

st.set_page_config(layout="wide")

# --- USER AUTHENTICATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.session_state.username == "admin" and st.session_state.password == "password":  # Change credentials as needed
        st.session_state.logged_in = True
    else:
        st.error("Invalid username or password")

if not st.session_state.logged_in:
    st.title("Login Required")
    st.text_input("Username", key="username")
    st.text_input("Password", type="password", key="password")
    st.button("Login", on_click=login)
    st.stop()  # Stop execution until logged in

# --- MAIN CONTENT (Only visible after login) ---
st.title("Simple Terminal Inside Streamlit")

# --- TERMINAL SECTION ---
st.subheader("Basic Terminal")

# User input for terminal commands
command = st.text_input("Enter a command:", "ls -la")

if st.button("Run Command"):
    output = subprocess.getoutput(command)
    st.text_area("Output:", output, height=300)

# --- LOGOUT BUTTON ---
if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
