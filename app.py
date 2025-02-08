import streamlit as st
import os
import time

st.set_page_config(layout="wide")
st.title("Web-Based Terminal & Embedded Port 8080")

# Find the correct flask-shell path
FLASK_SHELL_PATH = os.popen("which flask-shell").read().strip()

if not FLASK_SHELL_PATH:
    st.error("Flask-Shell is not installed or the path is incorrect.")
else:
    def start_web_terminal():
        st.info(f"Starting Web Terminal at {FLASK_SHELL_PATH} on port 8080...")
        os.system(f"{FLASK_SHELL_PATH} --host=0.0.0.0 --port=8080 &")
        time.sleep(3)  # Give time for the server to start
        st.success("Web Terminal is running at port 8080!")

    start_web_terminal()

# --- EMBED PORT 8080 INSIDE STREAMLIT ---
st.subheader("Embedded Web Terminal (Port 8080)")
st.components.v1.iframe("http://localhost:8080", height=600, scrolling=True)
