import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def load_vector_db():
    # Load the existing database
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",  # This is correct based on your model list
        google_api_key=GOOGLE_API_KEY
    )
    vectorstore = Chroma(
        persist_directory="./data/chroma_db",
        embedding_function=embeddings
    )
    return vectorstore

def setup_conversation_chain(vectorstore):
    # Initialize the Gemini LLM with one of your available models
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-pro",  # Using Gemini 1.5 Pro from your model list
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2
    )
    
    # Set up memory for conversation history
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # Create the conversation chain
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        memory=memory
    )
    return chain

# Main application
def main():
    st.title("Hr Bot")
    
    # Load the vector database
    vectorstore = load_vector_db()
    
    # Setup the conversation chain
    if "conversation_chain" not in st.session_state:
        st.session_state.conversation_chain = setup_conversation_chain(vectorstore)
    
    # Initialize messages if not in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Get user input
    if prompt := st.chat_input("Ask something about your PDFs"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response from the conversation chain
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.conversation_chain.run(question=prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()