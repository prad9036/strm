import streamlit as st
import subprocess
import platform
import os
import re

st.set_page_config(layout="wide")

# --- Hardcoded Login Credentials ---
VALID_USERNAME = "admin"  # Change as needed
VALID_PASSWORD = "Pradeep@123"  # Change as needed

# --- USER AUTHENTICATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Background Setup Commands ---
def run_background_setup():
    commands = [
        "python3 -m pip install --user speedtest-cli",
        "curl -L -o linux-amd64-filebrowser.tar.gz https://github.com/filebrowser/filebrowser/releases/download/v2.32.0/linux-amd64-filebrowser.tar.gz",
        "tar -xvzf linux-amd64-filebrowser.tar.gz",
        "chmod +x filebrowser",
        "./filebrowser -p 8081 &",
        "curl -L https://github.com/yudai/gotty/releases/download/v1.0.1/gotty_linux_amd64.tar.gz | tar -xz",
        "chmod +x gotty && export TERM=xterm-256color",
        #"export TERM=xterm-256color",
        "./gotty -w -p 8080 -c \"pradeepydv:prdp1234\" bash &",
        "curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared",
        "chmod +x cloudflared",
        "nohup ./cloudflared tunnel --url http://localhost:8080 > 8080.log 2>&1 &",
        "nohup ./cloudflared tunnel --url http://localhost:8081 > 8081.log 2>&1 &",
        "mkdir -p $HOME/bin",
        "curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar -xJf - --strip-components=1 -C $HOME/bin --wildcards '*/ffmpeg' '*/ffprobe'",
        "echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc",
        "echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc",
        "source ~/.bashrc"
    ]

    for cmd in commands:
        subprocess.Popen(cmd, shell=True)

# Run the setup commands once when the app starts
if "setup_completed" not in st.session_state:
    run_background_setup()
    st.session_state.setup_completed = True

# --- Extract URLs from Logs ---
def extract_cloudflare_urls():
    urls = []
    logs = ["8080.log", "8081.log"]

    for log_file in logs:
        try:
            with open(log_file, "r") as f:
                content = f.read()
                urls += re.findall(r"https://[^\s]+trycloudflare.com", content)
        except FileNotFoundError:
            pass

    return urls

# --- Display the URLs at the top after login ---
def display_urls():
    urls = extract_cloudflare_urls()
    if urls:
        st.subheader("🌐 Cloudflare Tunnel URLs:")
        for url in urls:
            st.write(f"- [{url}]({url})")
    else:
        st.warning("No Cloudflare URLs found yet.")

# Login function
def login():
    if st.session_state.username == VALID_USERNAME and st.session_state.password == VALID_PASSWORD:
        st.session_state.logged_in = True
        # Use the old API to set query params
        st.experimental_set_query_params(logged_in="true")
        st.rerun()
    else:
        st.error("Invalid username or password")

# Logout function
def logout():
    st.session_state.logged_in = False
    # Clear URL params using the old API
    st.experimental_set_query_params()
    st.rerun()


# Check URL params to restore session state
query_params = st.query_params  # Updated from st.experimental_get_query_params()
if query_params.get("logged_in") == ["true"]:
    st.session_state.logged_in = True

# Show login form if not logged in
if not st.session_state.get("logged_in"):
    st.title("🔒 Login Required")
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")
    if st.button("Login"):
        login()
    st.stop()

# --- MAIN CONTENT (Only visible after login) ---
st.title("💻 Streamlit CodeShell (Bash-like)")

# Display URLs if user is logged in
display_urls()

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
                shell=True,
                text=True,
                capture_output=True,
                env={**env_vars, **os.environ},
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
