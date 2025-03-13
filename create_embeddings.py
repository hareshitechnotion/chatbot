from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def create_vector_db():
    # Read the extracted text
    with open("extracted_text.txt", "r", encoding="utf-8") as f:
        all_text = f.read()
    
    print(f"Processing {len(all_text)} characters of text...")
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    chunks = text_splitter.split_text(all_text)
    print(f"Split text into {len(chunks)} chunks")
    
    # Create embeddings using the correct model from your list
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",  # This is correct based on your model list
        google_api_key=GOOGLE_API_KEY
    )
    
    # Create and save the vector store
    db_directory = "./data/chroma_db"
    vectorstore = Chroma.from_texts(
        texts=chunks, 
        embedding=embeddings,
        persist_directory=db_directory
    )
    vectorstore.persist()
    print(f"Vector database created and saved to {db_directory}")
    return vectorstore

if __name__ == "__main__":
    os.makedirs("./data", exist_ok=True)
    create_vector_db()