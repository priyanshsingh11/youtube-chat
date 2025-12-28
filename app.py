import streamlit as st
import os
import re

from youtube_transcript_api import YouTubeTranscriptApi

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

# -------------------------------------------------
# STREAMLIT CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="YouTube Chatbot (Gemini + RAG)",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 YouTube Video Chatbot")
st.caption("Built using Gemini + FAISS + RAG")

# -------------------------------------------------
# API KEY
# -------------------------------------------------
api_key = st.text_input("🔑 Enter your Gemini API Key", type="password")

if api_key:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBKMdS83Il_pBVIyMJKaguvFeRNd18ct-A"

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def extract_video_id(url: str):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_transcript(video_id: str):
    try:
        # Newer versions
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
        except:
            transcript = transcript_list.find_generated_transcript(['en'])
        data = transcript.fetch()

    except Exception:
        # Older versions
        data = YouTubeTranscriptApi.get_transcript(video_id)

    return " ".join([item["text"] for item in data])

# -------------------------------------------------
# INPUT
# -------------------------------------------------
yt_url = st.text_input("📺 Enter YouTube Video URL")

if st.button("🚀 Process Video"):
    if not api_key:
        st.error("Please enter your Gemini API key.")
        st.stop()

    if not yt_url:
        st.error("Please enter a YouTube URL.")
        st.stop()

    with st.spinner("Processing video transcript..."):
        try:
            video_id = extract_video_id(yt_url)
            if not video_id:
                st.error("Invalid YouTube URL")
                st.stop()

            # 1️⃣ Transcript
            text = get_transcript(video_id)

            # 2️⃣ Split text (same as notebook logic)
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = splitter.split_text(text)

            # 3️⃣ Embeddings (SAME as notebook)
            embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2"
            )

            # 4️⃣ FAISS vector store
            vector_store = FAISS.from_texts(chunks, embeddings)
            retriever = vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )

            # 5️⃣ Gemini LLM (SAME as notebook)
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash-lite",
                temperature=0.2
            )

            # 6️⃣ Prompt (aligned with notebook)
            prompt = PromptTemplate.from_template(
                """
You are a helpful assistant.
Answer ONLY from the provided transcript context.
If the context is insufficient, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""
            )

            # 7️⃣ LCEL RAG Chain
            rag_chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | llm
            )

            st.session_state.rag = rag_chain
            st.success("✅ Video processed successfully!")

        except Exception as e:
            st.error(f"Error: {e}")

# -------------------------------------------------
# CHAT
# -------------------------------------------------
if "rag" in st.session_state:
    st.divider()
    st.subheader("💬 Ask Questions")

    question = st.text_input("Type your question")

    if st.button("Ask"):
        if not question:
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                response = st.session_state.rag.invoke(question)
                st.markdown("### 🤖 Answer")
                st.write(response.content)
