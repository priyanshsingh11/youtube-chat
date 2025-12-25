# Retrieval-Augmented Generation (RAG) System

This project demonstrates a Retrieval-Augmented Generation (RAG) architecture that enhances Large Language Model (LLM) responses by grounding them in external knowledge sources such as documents, websites, or APIs.

The system retrieves relevant information before generating a response, improving accuracy and contextual understanding.

---

## System Architecture

```mermaid
flowchart TD

    %% Data Ingestion Phase
    A[Data Sources\nWebsites, PDFs, APIs]
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
    R[Retriever\nSemantic Search]
    CXT[Relevant Chunks\nContext]

    Q --> QE
    QE --> R
    R --> F
    F --> CXT

    %% Response Generation Phase
    P[Prompt\nContext + Query]
    LLM[Large Language Model]
    RES[Final Response]

    CXT --> P
    Q --> P
    P --> LLM
    LLM --> RES
