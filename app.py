import streamlit as st
import os
import pty
import subprocess
import select
import threading

# Set Streamlit page layout
st.set_page_config(layout="wide")
st.title("Full Interactive Terminal with Sudo Access")

# Terminal Session Storage
if "terminal_output" not in st.session_state:
    st.session_state.terminal_output = ""

# Function to run the shell in a pseudo-terminal
def run_shell():
    master, slave = pty.openpty()  # Create a pseudo-terminal
    process = subprocess.Popen(
        ["/bin/bash"],
        stdin=slave,
        stdout=slave,
        stderr=slave,
        text=True,
        bufsize=1,
        close_fds=True
    )

    while process.poll() is None:  # While the process is running
        ready, _, _ = select.select([master], [], [], 0.1)
        if ready:
            output = os.read(master, 1024).decode("utf-8", errors="ignore")
            st.session_state.terminal_output += output  # Store output in session state

    os.close(master)
    os.close(slave)

# Run shell in a separate thread
if "shell_thread" not in st.session_state:
    thread = threading.Thread(target=run_shell, daemon=True)
    thread.start()
    st.session_state.shell_thread = thread

# Display terminal output
st.text_area("Terminal Output:", st.session_state.terminal_output, height=400)

# Command input box
command = st.text_input("Enter command (Press Enter to execute):")

# Send command to shell
if command:
    os.system(f"echo '{command}' > /proc/{os.getpid()}/fd/0")
    st.session_state.terminal_output += f"\n$ {command}\n"
    st.rerun()  # Updated from `st.experimental_rerun()`

# --- EMBED PORT 8080 ---
st.subheader("Embedded Port 8080 Service")
st.components.v1.iframe("http://localhost:8080", height=600, scrolling=True)

st.warning("⚠️ Be careful! This gives full root access.")
