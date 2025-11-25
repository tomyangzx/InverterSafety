import os
import argparse
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# Configuration
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# LLM Selection
USE_OPENAI = False # Set to True to use OpenAI (Copilot-like model)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
LLM_MODEL_OLLAMA = "llama3" 
LLM_MODEL_OPENAI = "gpt-4o"

def query_rag(query_text):
    print(f"Querying: {query_text}")
    
    # Load DB
    print("Loading Vector Database...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}. Run src/ingest.py first.")
        return

    db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    
    # Setup LLM
    llm = None
    if USE_OPENAI:
        from langchain_openai import ChatOpenAI
        if not OPENAI_API_KEY:
            print("Error: OPENAI_API_KEY environment variable not set.")
            return
        print(f"Connecting to OpenAI ({LLM_MODEL_OPENAI})...")
        llm = ChatOpenAI(model=LLM_MODEL_OPENAI, api_key=OPENAI_API_KEY)
    else:
        # Setup Local LLM (Ollama)
        print(f"Connecting to Ollama ({LLM_MODEL_OLLAMA})...")
        try:
            llm = Ollama(model=LLM_MODEL_OLLAMA) 
        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            print("Make sure Ollama is installed and running.")
            return

    # Create Chain
    retriever = db.as_retriever(search_kwargs={"k": 4})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    
    # Run Query
    try:
        response = qa_chain.invoke(query_text)
        print("\n" + "="*30 + " ANSWER " + "="*30)
        print(response['result'])
        print("="*68 + "\n")
    except Exception as e:
        print(f"Error running query: {e}")
        print("Ensure 'ollama serve' is running and you have pulled the model (e.g., 'ollama pull llama3').")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the Inverter Safety RAG")
    parser.add_argument("query", nargs="?", help="The question to ask")
    args = parser.parse_args()

    if args.query:
        query_rag(args.query)
    else:
        while True:
            user_input = input("\nEnter your question (or 'q' to quit): ")
            if user_input.lower() in ['q', 'quit', 'exit']:
                break
            query_rag(user_input)
