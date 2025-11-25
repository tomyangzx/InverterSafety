import os
import glob
from typing import List
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Configuration
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def load_documents():
    """
    Load documents from the data directory.
    Supports PDF, TXT, and MD files.
    """
    documents = []
    
    # Load PDFs
    print(f"Scanning {DATA_PATH} for documents...")
    pdf_loader = DirectoryLoader(DATA_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents.extend(pdf_loader.load())
    
    # Load Text files
    txt_loader = DirectoryLoader(DATA_PATH, glob="**/*.txt", loader_cls=TextLoader)
    documents.extend(txt_loader.load())

    # Load Markdown files
    md_loader = DirectoryLoader(DATA_PATH, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
    documents.extend(md_loader.load())
    
    print(f"Loaded {len(documents)} documents.")
    return documents

def create_vector_db():
    documents = load_documents()
    if not documents:
        print("No documents found in data/ directory. Please add some files first.")
        return

    # Split Text
    print("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")
    
    # Create Embeddings (Runs locally)
    print(f"Loading embedding model: {EMBEDDING_MODEL}...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    # Store in Chroma (Persist to disk)
    print(f"Creating/Updating vector database at {DB_PATH}...")
    # If the DB already exists, this will append to it. 
    # To start fresh, you might want to delete the DB_PATH directory first.
    db = Chroma.from_documents(chunks, embeddings, persist_directory=DB_PATH)
    db.persist()
    print("Database successfully created/updated.")

if __name__ == "__main__":
    create_vector_db()
