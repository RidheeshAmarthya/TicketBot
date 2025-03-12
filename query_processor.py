import config
from sentence_transformers import SentenceTransformer
import chromadb
import google.generativeai as genai
import os

# Configure the Gemini API key and model
genai.configure(api_key=config.gemini)

generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

gemini = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    system_instruction="You are an expert at extracting information from documents. Answer the user's question based solely on the provided context. If the answer is not in the context, respond with 'I am sorry, but I cannot answer the question based on the context provided.' Keep it Precise and Accurate. After the answer, write 'Source: ' and then the file name.",
)

# Retrieve top-k relevant chunks from ChromaDB based on the query
def retrieve(query, top_k=1):
    """Retrieves top-k relevant chunks based on the query."""
    model = SentenceTransformer("all-mpnet-base-v2")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection(name="rag_store")

    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    return results

# Query ChromaDB and send context to Gemini for an answer
def query_chromadb_and_gemini(query, top_k=5):
    """
    Queries ChromaDB for relevant context and then sends it to the Gemini model for an answer.
    """
    # Retrieve relevant documents from ChromaDB
    results = retrieve(query, top_k=top_k)
    relevant_chunks = results["documents"]
    ids = results["ids"]

    # Combine all relevant chunks into one context string
    context = ""
    for chunk in relevant_chunks:
        context += " ".join(chunk)

    print(f"Context: {context}")

    chat_session = gemini.start_chat()
    response = chat_session.send_message(context + query)

    # Check if the response is a string or a response object.
    if isinstance(response, str):
        response_text = response
    else:
        response_text = response.text

    # Extract the original file name from the first ID (assuming consistent file naming)
    if ids and ids[0]:
        file_name = ids[0][0].split("_chunk_")[0] + ".pdf" # Assumes all files are pdf.
        return f"{response_text} Source: {file_name}"
    else:
        return response_text

if __name__ == "__main__":
    query = "What is the name of the product?"
    response = query_chromadb_and_gemini(query)
    print(response)