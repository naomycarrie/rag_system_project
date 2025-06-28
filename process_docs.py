import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def process_documents():
    directory = "."
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt") and ("dislexia" in filename or "tdah" in filename or "inclusivos" in filename or "assistivas" in filename or "pedagogicas" in filename):
            file_path = os.path.join(directory, filename)
            loader = TextLoader(file_path)
            documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {"device": "cpu"}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local("faiss_index")
    print("Vetor store criado e salvo em faiss_index/")

if __name__ == "__main__":
    process_documents()

