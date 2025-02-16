import os
import json
import streamlit as st
from ind_checklist_stlit import load_preprocessed_data, init_vector_store, create_rag_chain

# Prevent Streamlit from auto-reloading on file changes
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

# Define the preprocessed file path
PREPROCESSED_FILE = "preprocessed_docs.json"

# Caching function to prevent redundant RAG processing
@st.cache_data
def cached_response(question: str):
    """Retrieve cached response if available, otherwise compute response."""
    return st.session_state.rag_chain.invoke({"question": question})["response"]

def main():
    st.title("Appian IND Application Assistant")
    st.markdown("Chat about Investigational New Drug Applications")

    # Button to clear chat history
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        if hasattr(st, "rerun"):
            st.rerun()
        else:
            st.experimental_rerun()

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Load preprocessed data and initialize the RAG chain
    if "rag_chain" not in st.session_state:
        if not os.path.exists(PREPROCESSED_FILE):
            st.error(f"❌ Preprocessed file '{PREPROCESSED_FILE}' not found. Please run preprocessing first.")
            return  # Stop execution if preprocessed data is missing

        with st.spinner("🔄 Initializing knowledge base..."):
            documents = load_preprocessed_data(PREPROCESSED_FILE)
            vectorstore = init_vector_store(documents)
            st.session_state.rag_chain = create_rag_chain(vectorstore.as_retriever())

    # Display chat history
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        if hasattr(st, "chat_message"):
            with st.chat_message(role):
                st.markdown(content)
        else:
            st.write(f"**{role.capitalize()}:** {content}")

    # Chat input and response handling
    # Check if st.chat_input is available (Streamlit 1.2 or higher)
    if hasattr(st, "chat_input"):
        prompt = st.chat_input("Ask about IND requirements")
    else:
        prompt = st.text_input("Ask about IND requirements")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        if hasattr(st, "chat_message"):
            with st.chat_message("user"):
                st.markdown(prompt)
        else:
            st.write(f"**User:** {prompt}")

        # Generate response (cached if already asked before)
        response = cached_response(prompt)
        if hasattr(st, "chat_message"):
            with st.chat_message("assistant"):
                st.markdown(response)
        else:
            st.write(f"**Assistant:** {response}")

        # Store bot response in chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
