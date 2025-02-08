import streamlit as st
import os
import time
import subprocess

st.set_page_config(layout="wide")
st.title("VS Code Embedded in Streamlit")

# Path to store the code-server installation
CODE_SERVER_PATH = "/home/appuser/.local/bin/code-server"

# Function to install code-server if not installed
def install_code_server():
    if not os.path.exists(CODE_SERVER_PATH):
        st.info("Downloading and installing VS Code Server...")
        os.system("curl -fsSL https://code-server.dev/install.sh | sh")
        st.success("VS Code Server installed successfully!")

# Function to start VS Code Server
def start_code_server():
    st.info("Starting VS Code Server...")
    os.system(f"{CODE_SERVER_PATH} --bind-addr 0.0.0.0:8080 &")
    time.sleep(5)  # Wait for VS Code Server to start
    st.success("VS Code Server started!")

# Install code-server if needed
install_code_server()

# Button to start VS Code Server
if st.button("Start VS Code"):
    start_code_server()

# Embed VS Code in Streamlit using an iframe
st.components.v1.iframe("http://localhost:8080", height=800, scrolling=True)
