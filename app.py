import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
import re

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="YouTube Video Summarizer",
    page_icon="🎥",
    layout="centered"
)

st.title("🎥 YouTube Video Summarizer & Chat")
st.write("Paste any YouTube link to get a quick summary and ask questions.")

# =========================
# HELPER FUNCTIONS
# =========================
def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([t["text"] for t in transcript])
        return text
    except TranscriptsDisabled:
        return None


# =========================
# YOUR ML LOGIC GOES HERE
# =========================
def summarize_video(text):
    """
    🔴 Replace this with your existing
    LangChain / OpenAI / RAG code
    """
    return text[:1000] + "..."


# =========================
# UI
# =========================
video_url = st.text_input("🔗 Enter YouTube Video URL")

if st.button("Summarize"):
    video_id = extract_video_id(video_url)

    if not video_id:
        st.error("Invalid YouTube URL")
    else:
        with st.spinner("Fetching transcript..."):
            transcript_text = get_transcript(video_id)

        if transcript_text is None:
            st.error("Transcript not available for this video.")
        else:
            with st.spinner("Generating summary..."):
                summary = summarize_video(transcript_text)

            st.subheader("📌 Summary")
            st.write(summary)

# =========================
# CHAT SECTION (OPTIONAL)
# =========================
st.divider()
st.subheader("💬 Ask a question about the video")

question = st.text_input("Your question")

if st.button("Ask"):
    if question:
        # 🔴 Replace with RAG-based answer
        st.write("Answer coming from your RAG pipeline...")
