import streamlit as st
import os
import time
import subprocess

st.set_page_config(layout="wide")
st.title("VS Code & Terminal in Streamlit")

# Detect where code-server is installed
CODE_SERVER_PATH = subprocess.getoutput("which code-server").strip()
if not CODE_SERVER_PATH:
    CODE_SERVER_PATH = "/home/appuser/.local/bin/code-server"  # Default path for local installs

# Function to install VS Code Server (without sudo)
def install_code_server():
    if not os.path.exists(CODE_SERVER_PATH):
        st.info("Downloading and installing VS Code Server...")
        install_command = """
        curl -fsSL https://code-server.dev/install.sh | sh 2>&1 | tee install_log.txt
        """
        os.system(install_command)
        st.success("VS Code Server installed successfully!")

# Function to start VS Code Server
def start_code_server():
    st.info(f"Starting VS Code Server from {CODE_SERVER_PATH} ...")
    os.system(f"{CODE_SERVER_PATH} --bind-addr 0.0.0.0:8080 &")
    time.sleep(5)  # Wait for VS Code Server to start
    st.success("VS Code Server started!")

# Function to check if VS Code is running
def is_code_server_running():
    result = subprocess.getoutput("ps aux | grep code-server | grep -v grep")
    return "code-server" in result  # Returns True if running

# Install and start VS Code if not running
install_code_server()
if not is_code_server_running():
    start_code_server()

# Embed VS Code inside Streamlit
st.subheader("VS Code Inside Streamlit")
st.components.v1.iframe("http://localhost:8080", height=800, scrolling=True)

# Manual Terminal inside Streamlit
st.subheader("Manual Terminal Access")

command = st.text_input("Enter a command to run:", "ls -la")

if st.button("Run Command"):
    output = subprocess.getoutput(command)
    st.text_area("Command Output:", output, height=300)
