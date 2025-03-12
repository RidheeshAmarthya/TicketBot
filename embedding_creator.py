import config
import pdfplumber
from sentence_transformers import SentenceTransformer
import chromadb
import re
import os

# Extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file in larger chunks."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text as a block (preserving paragraphs)
            text += page.extract_text() + "\n"
    return re.sub(r'\n+', ' ', text).strip()  # Remove excessive newlines

# Split the extracted text into chunks
def chunk_text(text, chunk_size=512):
    """Splits text into larger chunks, while preserving newlines."""
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# Store the embeddings in ChromaDB
def store_embeddings(pdf_path):
    """Stores PDF text embeddings in ChromaDB."""
    model = SentenceTransformer("all-mpnet-base-v2")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection(name="rag_store")

    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size=1024)  # Increase chunk size here
    embeddings = model.encode(chunks).tolist()

    # Get the base file name (without extension)
    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]

    for i, chunk in enumerate(chunks):
        # Generate a unique ID based on the file name and chunk index
        unique_id = f"{base_filename}_chunk_{i}"
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i]],
            ids=[unique_id]  # Use the unique ID here
        )

if __name__ == "__main__":
    pdf_path = "data/EPD.pdf"  # Example path (replace with your file)
    store_embeddings(pdf_path)
    print(f"Embeddings for {pdf_path} created successfully.")