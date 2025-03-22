import streamlit as st
import subprocess
import platform
import os

st.set_page_config(layout="wide")

# --- Hardcoded Login Credentials ---
VALID_USERNAME = "admin"  # Change as needed
VALID_PASSWORD = "Pradeep@123"  # Change as needed

# --- USER AUTHENTICATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login function
def login():
    if st.session_state.username == VALID_USERNAME and st.session_state.password == VALID_PASSWORD:
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
    st.title("🔒 Login Required")
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")
    if st.button("Login"):
        login()
    st.stop()

# --- MAIN CONTENT (Only visible after login) ---
st.title("💻 Streamlit CodeShell (Bash-like)")

# --- Display OS Type ---
os_type = platform.system()
st.write(f"**Operating System:** {os_type}")

# --- Multi-line text area for custom environment variables ---
st.subheader("🌍 Set Custom Environment Variables")
variables = st.text_area(
    "Enter environment variables (key=value format, one per line):",
    "",
    placeholder="API_ID=123456\nAPI_HASH=abcdef...\nBOT_TOKEN=xyz...",
)

# --- Input area for the shell command ---
st.subheader("⚡ Shell Command")
command = st.text_input("Enter your shell command:", "")

# --- Button to execute the command ---
if st.button("Run Command"):
    if command:
        try:
            # Parse and set environment variables from input
            env_vars = {}
            for line in variables.strip().split("\n"):
                if "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()

            # Execute the shell command with environment variables
            result = subprocess.run(
                command,
                shell=True,  # Use shell=True for compatibility
                text=True,
                capture_output=True,
                env={**env_vars, **os.environ},  # Merge user vars with system env
            )

            # --- Display the output ---
            st.subheader("📜 Output:")
            if result.stdout:
                st.text_area("Standard Output:", result.stdout, height=250)

            # --- Display errors (if any) ---
            if result.stderr:
                st.subheader("⚠️ Error:")
                st.text_area("Error Output:", result.stderr, height=150)

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
    else:
        st.warning("⚠️ Please enter a command to run.")

# --- LOGOUT BUTTON ---
if st.button("🚪 Logout"):
    logout()
