import streamlit as st
import subprocess

st.set_page_config(layout="wide")
st.title("Simple Terminal & Embedded Port 8080")

# --- TERMINAL SECTION ---
st.subheader("Basic Terminal Inside Streamlit")

# User input for terminal commands
command = st.text_input("Enter a command:", "ls -la")

if st.button("Run Command"):
    output = subprocess.getoutput(command)
    st.text_area("Output:", output, height=300)

# --- EMBED PORT 8080 ---
st.subheader("Embedded Service Running on Port 8080")
st.components.v1.iframe("http://localhost:8080", height=600, scrolling=True)
