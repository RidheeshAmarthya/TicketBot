<img src="https://imgur.com/BSVHVkP.png">



# DocBot: Streamlit Application for Document Q&A with Jira Integration

DocBot is a Streamlit web application that allows users to upload PDF documents, create embeddings, and query them in the context of a specific Jira ticket. It leverages ChromaDB for vector storage, Sentence Transformers for embeddings, and Google Gemini for generating responses.

## Features

* **PDF Upload:** Upload PDF documents for processing.
* **Embedding Creation:** Automatically generates embeddings for the uploaded PDF.
* **Jira Integration:** Fetches Jira ticket details (summary and description) and incorporates them into the query context.
* **Question Answering:** Queries the document content based on the Jira context and provides relevant answers.
* **Source Tracking:** Displays the file names of the source documents used to generate the answer.
* **Clear and User-Friendly Interface:** Streamlit provides a simple and interactive interface.
* **Refresh Button:** Clear previous responses and embedding outputs.

## Prerequisites

Before running DocBot, ensure you have the following installed:

* Python 3.7+
* Streamlit
* Sentence Transformers
* ChromaDB
* Google Generative AI (Gemini)
* Jira Python library (`jira`)
* PyPDF2
* python-dotenv

You can install these dependencies using pip:

```bash
pip install streamlit sentence-transformers chromadb google-generativeai jira PyPDF2 python-dotenv
```

You will also need:

* A Google Cloud project with the Gemini API enabled and an API key.
* A Jira account with API token access.

## Configuration

1.  **Create a `config.py` file:**
    * In the same directory as your script, create a file named `config.py`.
    * Add your Google Gemini API key and Jira API token to the file:

    ```python
    gemini = "YOUR_GEMINI_API_KEY"
    atlassian = "YOUR_JIRA_API_TOKEN"
    ```

2.  **Jira Configuration:**
    * When running the application, you'll need to provide the following Jira details in the sidebar:
        * Jira URL (e.g., `yourdomain.atlassian.net`)
        * Jira Username (your email address)
        * Jira API Token
        * Jira Ticket ID (e.g., `PROJECT-123`)

## Usage

1.  **Run the Streamlit application:**

    ```bash
    streamlit run your_script_name.py
    ```

    Replace `your_script_name.py` with the actual name of your Python script.

2.  **Upload a PDF:**
    * In the sidebar, use the file uploader to select a PDF document.

3.  **Enter Jira details:**
    * Provide the required Jira configuration in the sidebar.

4.  **View results:**
    * The application will display the fetched Jira ticket information, create embeddings for the PDF, and generate a response based on the document content and Jira context.
    * The response will be displayed in the main area of the application.
    * The file names of the source documents will be appended to the response.
    * The output of the embedding creation process will also be displayed.
    * Use the refresh button on the side bar to clear the stored session state.

## File Structure

```
DocBot/
├── your_script_name.py
├── embedding_creator.py
├── query_processor.py
├── jira_handler.py
├── config.py
└── chroma_db/ (ChromaDB storage directory)
```

* `your_script_name.py`: The main Streamlit application script.
* `embedding_creator.py`: Handles PDF processing and embedding creation.
* `query_processor.py`: Queries ChromaDB and interacts with the Gemini model.
* `jira_handler.py`: Fetches Jira ticket information.
* `config.py`: Stores API keys and other configuration settings.
* `chroma_db/`: The directory where ChromaDB stores the vector database.

## Notes

* Ensure that your Jira API token has the necessary permissions to access the specified Jira ticket.
* The quality of the responses depends on the content of the PDF document and the relevance of the Jira context.
* Error handling is included to catch common issues like invalid Jira credentials or query processing errors.
* The application uses Streamlit's session state to prevent unnecessary re-querying and re-embedding.
* The embedding creation output is captured and displayed in the streamlit application.
* The source documents are appended to the answer provided by gemini.
