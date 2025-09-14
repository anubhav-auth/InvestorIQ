# ingestion_scripts/ingestion_news.py

import os
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()
DATA_DIR = "data/news_articles"
FAISS_INDEX_PATH = "vector_stores/faiss_news_index"
EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"  

def create_knowledge_base():
    """
    Loads documents, splits them, and creates a LangChain-compatible
    FAISS vector store using a local embedding model.
    """
    print(f"Loading documents from: {DATA_DIR}")
    if not os.listdir(DATA_DIR):
        print("\n!!! Data directory is empty.")
        print("Please add some .txt files to the 'data/news_articles' folder and run again.\n")
        return

    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    print(f"Loaded {len(documents)} document(s).")

    text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    nodes = text_splitter.get_nodes_from_documents(documents)
    texts = [node.get_content() for node in nodes]
    print(f"Split documents into {len(texts)} chunks.")

    print(f"Initializing local embedding model: {EMBEDDING_MODEL}")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print("Creating FAISS index... this may take a moment.")
    vector_store = FAISS.from_texts(texts, embedding=embeddings)

    print(f"Saving index to: {FAISS_INDEX_PATH}")
    vector_store.save_local(FAISS_INDEX_PATH)

    print("\n--- Knowledge Base creation complete! ---")
    print("The index was successfully created using a local model, avoiding API limits.")

if __name__ == "__main__":
    create_knowledge_base()