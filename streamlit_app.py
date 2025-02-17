# streamlit_app.py
import streamlit as st
import os

port = int(os.environ.get("PORT", 8080))
st.write(f"Hello, World! Port: {port}")  # Include the port in the output

if __name__ == "__main__":
    st.run(server_address="0.0.0.0", server_port=port)
