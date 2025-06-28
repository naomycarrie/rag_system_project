# Sistema RAG (Retrieval-Augmented Generation) para Educação Inclusiva

Este projeto implementa um sistema de Geração Aumentada por Recuperação (RAG) focado em educação inclusiva. Ele permite que você faça perguntas sobre tópicos como dislexia, TDAH, métodos inclusivos, tecnologias assistivas e adaptações pedagógicas, e o sistema fornecerá respostas informadas com base em uma base de conhecimento local.

## O que é RAG?

RAG é uma técnica que combina a capacidade de modelos de linguagem grandes (LLMs) de gerar texto com a capacidade de sistemas de recuperação de informações de buscar dados relevantes. Isso significa que, em vez de o LLM responder apenas com base em seu treinamento geral, ele primeiro pesquisa em uma base de conhecimento específica (neste caso, documentos sobre educação inclusiva) e usa essas informações para formular uma resposta mais precisa e contextualizada.

## Estrutura do Projeto

O projeto é composto pelos seguintes arquivos e diretórios:

- `rag_system.py`: O script principal que inicializa o sistema RAG e permite a interação com o usuário.
- `process_docs.py`: Um script para processar seus documentos de texto (PDF, TXT, MD) e criar um índice vetorial FAISS.
- `llm_interface.py`: Contém a lógica para interagir com o modelo de linguagem local (TinyLlama).
- `rag_explanation.md`: Uma explicação detalhada da técnica RAG e a justificativa para a escolha do tema.
- `todo.md`: Um arquivo de registro de tarefas.
- `faiss_index/`: Diretório que armazena o índice vetorial FAISS gerado a partir dos seus documentos.
- `llama.cpp/`: Diretório que contém o projeto `llama.cpp` e o modelo TinyLlama GGUF.

## Pré-requisitos

Para configurar e executar este projeto, você precisará dos seguintes softwares instalados em seu sistema:

- **Python 3.11**: Verifique com `python3.11 --version`.
- **pip**: Verifique com `pip3 --version`.
- **git**
- **cmake**
- **ninja-build**

Você pode instalar `git`, `cmake` e `ninja-build` usando os seguintes comandos:

```bash
sudo apt-get update
sudo apt-get install -y git cmake build-essential ninja-build
```

## Configuração e Execução

Siga os passos abaixo para configurar e executar o sistema RAG:

### 1. Configuração do Llama.cpp e Download do Modelo

Primeiro, clone o repositório `llama.cpp` e compile-o. Em seguida, baixe o modelo TinyLlama GGUF.

```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
cmake -B build -DLLAMA_CURL=OFF
cmake --build build
mkdir -p models
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q5_K_M.gguf -P llama.cpp/models
```

### 2. Instalação das Dependências Python

Instale todas as bibliotecas Python necessárias usando pip:

```bash
pip3 install langchain transformers sentence-transformers faiss-cpu pypdf llama-cpp-python langchain-community
```

### 3. Preparação dos Documentos e Criação do Vetor Store

Coloque seus arquivos de texto (.txt, .pdf ou .md) sobre educação inclusiva (dislexia, TDAH, métodos inclusivos, tecnologias assistivas, adaptações pedagógicas) na mesma pasta onde você salvou `process_docs.py` e `rag_system.py` (neste caso, `/home/ubuntu/`).

Em seguida, execute o script para processar os documentos e criar o índice vetorial FAISS:

```bash
python3.11 process_docs.py
```

Este comando criará uma pasta `faiss_index` contendo o índice vetorial.

### 4. Execução do Sistema RAG

Finalmente, execute o script principal do sistema RAG:

```bash
python3.11 rag_system.py
```

O sistema será inicializado e você poderá digitar suas perguntas no terminal. Digite `sair` para encerrar a interação.

## Contribuição

Sinta-se à vontade para contribuir com este projeto. Você pode abrir issues para relatar bugs ou sugerir melhorias, ou enviar pull requests com novas funcionalidades ou correções.

