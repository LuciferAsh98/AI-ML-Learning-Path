import os
import pinecone
from pathlib import Path
import streamlit as st
import openai
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma, Pinecone
from langchain.document_loaders import DirectoryLoader, PyPDFLoader, CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAIChat
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# Define paths explicitly
TMP_DIR = Path('./data/tmp')
LOCAL_VECTOR_STORE_DIR = Path('./data/vector_store')

st.set_page_config(page_title="RAG Chatbot")

openai_api_key = os.getenv("OPENAI_API_KEY")
pc = Pinecone(api_key="pine_key", environment="us-east-1")
index = 'real-estate'
print("jajflnsfnalkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk", pc.list_indexes().names())
if index not in pc.list_indexes().names():
    pc.create_index(
        name=index,
        dimension=1536,
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-west-2'
        )
    )
# Load documents from specified directory
def load_documents():
    pdf_loader = DirectoryLoader(TMP_DIR.as_posix(), glob='**/*.pdf', loader_cls=PyPDFLoader)
    csv_loader = DirectoryLoader(TMP_DIR.as_posix(), glob='**/*.csv', loader_cls=CSVLoader)
    pdf_documents = pdf_loader.load()
    csv_documents = csv_loader.load()
    return pdf_documents + csv_documents

# Split documents into manageable chunks
def split_documents(documents):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    return text_splitter.split_documents(documents)

# Create embeddings using a local vector database
def embeddings_on_local_vectordb(texts):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    class EmbeddingFunction:
        def __call__(self, input):
            return embeddings.embed_documents(input)
    embedding_function = EmbeddingFunction()
    vectordb = Chroma.from_documents(texts, embedding=embedding_function,
                                     persist_directory=LOCAL_VECTOR_STORE_DIR.as_posix())
    vectordb.persist()
    return vectordb.as_retriever(search_kwargs={'k': 7})

# Initialize Pinecone vector store
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
pinecone_vector_store = PineconeVectorStore(
    index_name="real-estate",
    pinecone_api_key="pine_key",
    embedding=embeddings
)

# Create embeddings using Pinecone
def embeddings_on_pinecone(texts):
    # You may need to handle batching of documents if they are large
    batch_size = 50
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        print("======================================",batch_texts)
        try:
            # Add documents to Pinecone
            print("......................................",batch_texts)
            pinecone_vector_store.add_documents(batch_texts)
        except openai.OpenAIError as e:
            st.error(f"An OpenAI error occurred: {str(e)}")
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            return None
        
    return pinecone_vector_store


# Handle queries to the language model
def query_llm(retriever, query):
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=OpenAIChat(openai_api_key=openai_api_key),
        retriever=retriever,
        return_source_documents=True,
    )
    result = qa_chain({'question': query, 'chat_history': st.session_state.get('messages', [])})
    st.session_state.messages.append((query, result['answer']))
    return result['answer']

# Input fields for user interaction
def input_fields():
    st.session_state.pinecone_db = st.checkbox('Use Pinecone Vector DB')
    st.session_state.source_docs = st.file_uploader("Upload Documents", type=['pdf', 'csv'], accept_multiple_files=True)

# Process uploaded documents
def process_documents():
    if not st.session_state.source_docs:
        st.warning("Please upload documents.")
        return

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    for source_doc in st.session_state.source_docs:
        with open(TMP_DIR / source_doc.name, 'wb') as f:
            f.write(source_doc.read())
    
    documents = load_documents()
    texts = split_documents(documents)
    
    if not st.session_state.pinecone_db:
        st.session_state.retriever = embeddings_on_local_vectordb(texts)
    else:
        st.session_state.retriever = embeddings_on_pinecone(texts)

# Boot the application
def boot():
    input_fields()
    st.button("Submit Documents", on_click=process_documents)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        st.write(f"**User**: {message[0]}")
        st.write(f"**Bot**: {message[1]}")
    
    if query := st.text_input("Ask a question:"):
        st.write(f"**User**: {query}")
        response = query_llm(st.session_state.retriever, query)
        st.write(f"**Bot**: {response}")

if __name__ == '__main__':
    boot()