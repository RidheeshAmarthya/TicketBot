import embedding_creator
import query_processor
import jira_handler
import os
import config
import streamlit as st
from tempfile import NamedTemporaryFile
import time
import sys
from io import StringIO
from contextlib import redirect_stdout

def main():
    """Main function for the Streamlit web application."""

    st.title("DocBot")

    st.sidebar.header("Configuration")

    # Jira Configuration (in sidebar)
    jira_url = st.sidebar.text_input("Jira URL", value="ridheesh.atlassian.net")
    jira_username = st.sidebar.text_input("Jira Username", value="vridheesh@gmail.com")
    jira_token = st.sidebar.text_input("Jira API Token", value=config.atlassian, type="password")
    jira_ticket = st.sidebar.text_input("Jira Ticket ID", value="MBA-7")

    # PDF Upload (in sidebar)
    uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

    if st.sidebar.button("Refresh"):  # Use a sidebar button for refresh
        # Clear any existing results (important for refresh)
        if 'response' in st.session_state:
            del st.session_state['response']
        if 'captured_output' in st.session_state:  # Also clear captured output
            del st.session_state['captured_output']


    if not jira_url or not jira_username or not jira_token or not jira_ticket:
        st.error("Please fill in all Jira configuration fields.")
        return  # Stop execution if Jira config is missing

    if uploaded_file is not None:
        # Handle PDF file upload and embedding creation.
        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            pdf_path = tmp_file.name
            st.info("Creating embeddings...")
             # Redirect stdout to capture print statements from embedding_creator
            with StringIO() as output, redirect_stdout(output):
                embedding_creator.store_embeddings(pdf_path)
                st.session_state['captured_output'] = output.getvalue()  # Store the captured output
            st.success("Embeddings created!")
            os.remove(pdf_path)


    # Get Jira ticket information
    try:
        ticket = jira_handler.get_jira_issue(jira_url, jira_username, jira_token, jira_ticket)
        st.sidebar.success(f"Successfully fetched Jira ticket: {jira_ticket}")
        st.sidebar.write(f"**Summary:** {ticket[0]}")
        st.sidebar.write(f"**Description:** {ticket[1]}")


    except Exception as e:
        st.sidebar.error(f"Error fetching Jira ticket: {e}")
        return


    # Build the combined query (no user input)
    final_query = f"This is related to JIRA ticket {jira_ticket}: Summary: {ticket[0]}, Description: {ticket[1]}. Get the most relevant information."


    # Use session state to manage the response and avoid re-querying unnecessarily.
    if 'response' not in st.session_state:
        with st.spinner("Querying..."):
            try:
                response = query_processor.query_chromadb_and_gemini(final_query)
                st.session_state['response'] = response  # Store in session state
            except Exception as e:
                st.error(f"Error during query processing: {e}")
                return # prevent further processing if we error out.

    # Display the response (from session state)
    if 'response' in st.session_state:
        st.subheader("Suggestion:")
        st.write(st.session_state['response'])

    # Display captured output (from embedding_creator)
    if 'captured_output' in st.session_state:
        st.subheader("Embedding Creation Output:")
        st.text(st.session_state['captured_output'])




if __name__ == "__main__":
    main()