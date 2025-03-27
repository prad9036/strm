import streamlit as st
import subprocess
import os
import time

st.set_page_config(layout="wide")

# File to track if services have started
SERVICES_TRACK_FILE = ".services_started"

def start_services():
    """Start Cloudflared & Gotty only if not already started in this deployment."""
    if not os.path.exists(SERVICES_TRACK_FILE):
        st.write("🔄 Initializing services...")

        # Commands to start background processes
        commands = [
            "curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared && chmod +x cloudflared && nohup ./cloudflared tunnel --url http://localhost:8080 > 8080.log 2>&1 &",
            "curl -L https://github.com/yudai/gotty/releases/download/v1.0.1/gotty_linux_amd64.tar.gz | tar -xz && chmod +x gotty && export TERM=xterm-256color && nohup ./gotty -w -p 8080 -c 'pradeepydv:prdp1234' bash > gotty.log 2>&1 &"
        ]

        for cmd in commands:
            subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Create a file to indicate services have started
        with open(SERVICES_TRACK_FILE, "w") as f:
            f.write("started")

        st.success("✅ Services started successfully!")
        time.sleep(3)  # Allow time for services to initialize
    else:
        st.write("✅ Services are already running.")

# Ensure services start only once per deployment
start_services()

# --- Streamlit Login & Shell Interface Below ---
st.title("💻 Streamlit CodeShell (Bash-like)")

VALID_USERNAME = "admin"
VALID_PASSWORD = "Pradeep@123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.session_state.username == VALID_USERNAME and st.session_state.password == VALID_PASSWORD:
        st.session_state.logged_in = True
        st.rerun()
    else:
        st.error("Invalid username or password")

def logout():
    st.session_state.logged_in = False
    st.rerun()

if not st.session_state.logged_in:
    st.title("🔒 Login Required")
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")
    if st.button("Login"):
        login()
    st.stop()

st.subheader("⚡ Shell Command")
command = st.text_input("Enter your shell command:", "")

if st.button("Run Command"):
    if command:
        try:
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            st.subheader("📜 Output:")
            if result.stdout:
                st.text_area("Standard Output:", result.stdout, height=250)
            if result.stderr:
                st.subheader("⚠️ Error:")
                st.text_area("Error Output:", result.stderr, height=150)
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
    else:
        st.warning("⚠️ Please enter a command to run.")

if st.button("🚪 Logout"):
    logout()
