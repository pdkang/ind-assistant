import streamlit as st
import os

port = int(os.environ.get("PORT", 8080))  # Get port from env or default to 8080. Fallback important!
st.title("My Streamlit App")
# ... rest of your Streamlit app code

if __name__ == "__main__":
    st.run(server_address="0.0.0.0", server_port=port)
