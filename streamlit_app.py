import streamlit as st
import os

port = int(os.environ.get("PORT", 8080))
print(f"PORT environment variable: {port}")  # Print the value for debugging
st.title("My Streamlit App")
# ... rest of your code ...

if __name__ == "__main__":
    st.run(server_address="0.0.0.0", server_port=port)
