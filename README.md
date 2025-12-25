# Retrieval-Augmented Generation (RAG) System

This project demonstrates a **Retrieval-Augmented Generation (RAG)** based architecture that enhances Large Language Model (LLM) responses by grounding them in **external knowledge sources** such as documents, websites, or APIs.

The system retrieves the most relevant information before generating a response, improving accuracy, reliability, and context-awareness.

---

## System Architecture

```mermaid
flowchart TD

    %% Data Ingestion Phase
    A[Data Sources<br/>(Websites, PDFs, APIs)]
    B[Document Loader]
    C[Text Splitter]
    D[Text Chunks]
    E[Embedding Model]
    F[(Vector Store)]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F

    %% Query Processing Phase
    Q[User Query]
    QE[Query Embedding]
    R[Retriever<br/>(Semantic Search)]
    CXT[Most Relevant Chunks<br/>(Context)]

    Q --> QE
    QE --> R
    R --> F
    F --> CXT

    %% Response Generation Phase
    P[Prompt<br/>(Context + Query)]
    LLM[Large Language Model]
    RES[Final Response]

    CXT --> P
    Q --> P
    P --> LLM
    LLM --> RES
