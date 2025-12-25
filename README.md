# 🎥 YouTube Chat System (RAG + Streamlit)

An AI-powered **YouTube Chat System** that enables users to **chat with YouTube videos** using **Retrieval-Augmented Generation (RAG)**.  
The system extracts video transcripts, builds a semantic search index, and generates accurate, context-aware responses through a **Streamlit-based interactive UI**.

---

## 🚀 Project Overview

Large Language Models cannot directly understand video content.  
This project solves that problem by transforming **YouTube video transcripts into searchable knowledge**, allowing users to ask natural language questions about video content.

The system combines:
- YouTube transcript extraction
- Vector-based semantic search
- Large Language Models
- Interactive Streamlit UI

---

## 🧠 System Architecture

```mermaid
flowchart TD

    %% Ingestion Phase
    A[YouTube Video]
    B[Transcript Extraction]
    C[Text Splitter]
    D[Text Chunks]
    E[Embedding Model]
    F[(FAISS Vector Store)]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F

    %% Query Phase
    Q[User Question]
    QE[Query Embedding]
    R[Retriever\nSemantic Search]
    CXT[Relevant Chunks\nContext]

    Q --> QE
    QE --> R
    R --> F
    F --> CXT

    %% LLM Phase
    P[Prompt\nContext + Question]
    LLM[Large Language Model]
    RES[Final Answer]

    CXT --> P
    Q --> P
    P --> LLM
    LLM --> RES

```
