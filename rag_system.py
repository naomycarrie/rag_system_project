import os
import subprocess
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import LlamaCpp

def load_and_process_documents():
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
    return chunks

def get_vector_store(chunks):
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {"device": "cpu"}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

    if os.path.exists("faiss_index"):
        vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        print("Vetor store carregado de faiss_index/")
    else:
        vector_store = FAISS.from_documents(chunks, embeddings)
        vector_store.save_local("faiss_index")
        print("Vetor store criado e salvo em faiss_index/")
    return vector_store

def get_local_llm(model_path):
    llm = LlamaCpp(
        model_path=model_path,
        temperature=0.7,
        max_tokens=2000,
        top_p=1,
        n_ctx=4096, 
        n_gpu_layers=0,
        verbose=False, 
    )
    return llm

if __name__ == "__main__":
    print("Carregando e processando documentos...")
    chunks = load_and_process_documents()

    print("Obtendo vetor store...")
    vector_store = get_vector_store(chunks)

    print("Inicializando LLM local...")
    model_path = ".\\llama.cpp\\models\\tinyllama-1.1b-chat-v1.0.Q5_K_M.gguf"
    llm = get_local_llm(model_path)

    retriever = vector_store.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    print("Sistema RAG pronto. Digite suas perguntas (digite \'sair\' para encerrar):\n")

    while True:
        query = input("Você: ")
        if query.lower() == 'sair':
            break

        try:
            result = qa_chain({"query": query})
            print(f"LLM: {result['result']}")
            if 'source_documents' in result:
                print("Fontes:")
                for doc in result['source_documents']:
                    print(f"  - {doc.metadata.get('source', 'N/A')}")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            print("Por favor, tente novamente ou verifique a configuração do modelo LLM.")


            
