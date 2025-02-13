import streamlit as st
import subprocess
import os
import time

# Set Streamlit page layout
st.set_page_config(layout="wide")
st.title("Simple Terminal & Embedded Port 8080")

# --- STEP 1: Start HTTP Server on Port 8080 ---
st.subheader("Starting HTTP Server on Port 8080...")

# Check if the server is already running
def is_server_running(port=8080):
    result = subprocess.run(
        f"netstat -an | grep {port}",
        shell=True,
        capture_output=True,
        text=True
    )
    return str(port) in result.stdout

if not is_server_running():
    st.write("Starting server...")
    server_process = subprocess.Popen(
        ["python", "-m", "http.server", "8080"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2)  # Wait for server to start
else:
    st.write("Server is already running on port 8080.")

# --- STEP 2: Terminal Section ---
st.subheader("Basic Terminal Inside Streamlit")

command = st.text_input("Enter a command:", "ls -la")

if st.button("Run Command"):
    output = subprocess.getoutput(command)
    st.text_area("Output:", output, height=300)

# --- STEP 3: Embed HTTP Server Output ---
st.subheader("Embedded Service Running on Port 8080")

st.markdown(
    '<iframe src="http://localhost:8080" width="100%" height="600"></iframe>',
    unsafe_allow_html=True
)

st.write("If you see an error, ensure the server is running properly.")

# --- STEP 4: Stop Server When Streamlit App Closes ---
def stop_server():
    if "server_process" in globals():
        server_process.terminate()
        st.write("Stopped HTTP server.")

st.button("Stop Server", on_click=stop_server)
