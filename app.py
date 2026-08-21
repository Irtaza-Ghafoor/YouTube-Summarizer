import os
import re
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="NexusTube AI - Video Intelligence Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ADVANCED SaaS CSS STYLING ====================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b, #090d16);
        color: #f3f4f6;
        font-family: 'Inter', sans-serif;
    }
    .hero-badge {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        padding: 6px 18px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 600;
        color: white;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
        margin-bottom: 12px;
    }
    
    /* Refined Uniform Metric Cards */
    .metric-card {
        background: #111827;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 140px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .metric-card h4 {
        color: #9ca3af;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 10px;
        margin-top: 0;
    }
    .metric-card h2 {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }

    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
    }
    [data-testid="stSidebar"] {
        background: rgba(10, 15, 30, 0.9) !important;
        border-right: 1px solid #1f2937;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================
def extract_video_id(url):
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    elif "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    return None

def get_youtube_transcript(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None, "Error: Invalid YouTube URL format."
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(video_id)
        full_text = " ".join([snippet.text for snippet in transcript_list.snippets])
        return full_text, None
    except Exception as e:
        return None, f"Could not fetch transcript. Make sure captions are enabled. (Details: {str(e)})"

def call_groq_ai(system_prompt, user_content):
    api_key = os.getenv("GROQ_API_KEY")
    try:
        if not api_key and "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    if not api_key:
        return "Error: Groq API Key not found in environment or secrets."

    client = Groq(api_key=api_key.strip())
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            model="openai/gpt-oss-120b",
        )
        content = response.choices[0].message.content
        cleaned_content = re.sub(r'<a\s+name=".*?".*?></a>', '', content)
        return cleaned_content
    except Exception as e:
        return f"AI Generation Error: {str(e)}"

# ==================== CLEAN QUIZ RENDERER ====================
def render_quiz(quiz_text):
    questions = quiz_text.split("Q:")
    for i, q in enumerate(questions):
        if not q.strip():
            continue
        parts = q.split("Answer:")
        st.markdown(f"#### Question {i}")
        st.markdown(parts[0].strip())
        
        if len(parts) > 1:
            with st.expander("👁️ View Correct Answer"):
                st.success(parts[1].strip())
        st.markdown("---")

# ==================== SIDEBAR CONFIG ====================
with st.sidebar:
    st.markdown("### ⚡ NexusTube Control Center")
    st.markdown("Transform long lectures into structured reports & interactive insights.")
    st.markdown("---")
    
    video_url = st.text_input("🔗 YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
    
    summary_type = st.selectbox(
        "🎯 Intelligence Mode",
        ["Comprehensive Summary", "Key Bullet Points", "Chapter Breakdown with Timestamps"]
    )
    
    tone_mode = st.selectbox(
        "🎭 Report Tone",
        ["Executive / Professional", "Simple & Beginner Friendly", "Technical & Developer Focused"]
    )
    
    st.markdown("---")
    generate_btn = st.button("✨ Generate Intelligence", width='stretch')

# ==================== MAIN DASHBOARD LAYOUT ====================
st.markdown('<div class="hero-badge">⚡ Next-Gen Video Intelligence Platform</div>', unsafe_allow_html=True)
st.title("AI YouTube Video & Lecture Summarizer")
st.markdown("Paste any YouTube URL in the sidebar to extract transcripts, generate hidden-answer AI quizzes, translate reports, and chat directly with the video content.")
st.markdown("<br>", unsafe_allow_html=True)

# State Management for Session Data
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "result" not in st.session_state:
    st.session_state.result = None
if "quiz_result" not in st.session_state:
    st.session_state.quiz_result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Video Preview & Analytics Metadata Cards
if video_url.strip():
    vid_id = extract_video_id(video_url)
    if vid_id:
        col_prev1, col_prev2 = st.columns([1, 2])
        with col_prev1:
            st.image(f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg", width='stretch', caption="Target Video")
        with col_prev2:
            st.markdown("### 📌 Target Analysis Ready")
            st.markdown(f"**Video ID:** `{vid_id}`")
            st.markdown(f"**Selected Mode:** `{summary_type}` | **Tone:** `{tone_mode}`")
            st.markdown("Click **'Generate Intelligence'** in the sidebar to process analysis.")

st.markdown("---")

# ==================== GENERATION & RESULTS ENGINE ====================
if generate_btn:
    if not video_url.strip():
        st.warning("⚠️ Please provide a valid YouTube link in the sidebar first!")
    else:
        with st.spinner("🔄 Fetching transcript stream and executing deep AI analysis..."):
            transcript, err = get_youtube_transcript(video_url)
            
            if err:
                st.error(err)
            else:
                st.session_state.transcript = transcript
                
                tone_prompt_modifier = {
                    "Executive / Professional": "Maintain a polished, executive, and highly professional tone.",
                    "Simple & Beginner Friendly": "Keep explanations simple, intuitive, and easy for a beginner to grasp.",
                    "Technical & Developer Focused": "Focus heavily on technical depth, architecture, frameworks, and implementation details."
                }.get(tone_mode, "")

                prompts = {
                    "Comprehensive Summary": f"Provide a detailed, well-structured summary of this video transcript, highlighting core concepts and takeaways using Markdown headings. Do not include raw HTML anchor tags. {tone_prompt_modifier}",
                    "Key Bullet Points": f"Extract 5-10 core high-impact bullet points summarizing the most important lessons or facts. Do not include raw HTML anchor tags. {tone_prompt_modifier}",
                    "Chapter Breakdown with Timestamps": f"Create logical chapters/sections based on the video flow, providing a descriptive title and key summary for each. Do not include raw HTML anchor tags. {tone_prompt_modifier}"
                }

                system_prompt = prompts.get(summary_type, prompts["Comprehensive Summary"])
                user_payload = f"Here is the video transcript:\n\n{transcript[:14000]}"
                
                st.session_state.result = call_groq_ai(system_prompt, user_payload)
                st.session_state.quiz_result = None  
                st.session_state.chat_history = []  

# Render Results Dashboard if data exists in session state
if st.session_state.result:
    words_count = len(st.session_state.transcript.split()) if st.session_state.transcript else 0
    est_read_time = max(1, words_count // 200)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><h4>📝 Transcript Words</h4><h2>{words_count:,}</h2></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><h4>⏱️ Est. Reading Time</h4><h2>{est_read_time} mins</h2></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><h4>🤖 AI Engine</h4><h2>Groq Llama</h2></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)

    tab_report, tab_quiz, tab_translate, tab_chat = st.tabs([
        "📊 Analysis Report", 
        "🧠 AI Quiz Hub", 
        "🌐 Translate Report", 
        "💬 Chat with Video"
    ])
    
    with tab_report:
        st.markdown(f"### Report Mode: {summary_type}")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(st.session_state.result)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📥 Export Markdown Report",
            data=st.session_state.result,
            file_name="nexustube_intelligence_report.md",
            mime="text/markdown",
            type="primary"
        )
        
    with tab_quiz:
        st.markdown("### 🧠 AI Knowledge Check (Quiz Generator)")
        st.markdown("Test your understanding of the video concepts with interactive hidden-answer MCQs.")
        
        if st.button("🎲 Generate 5-Question Quiz"):
            with st.spinner("Crafting quiz questions from transcript..."):
                quiz_prompt = """
                You are an expert educator. Based on this video transcript, generate 5 multiple-choice questions (MCQs) with 4 options each (A, B, C, D).
                FORMAT: 
                Q: [Question Text]
                A. [Option]
                B. [Option]
                C. [Option]
                D. [Option]
                Answer: [Correct Option Letter and Text]
                
                DO NOT use any HTML tags. Keep it strictly clean Markdown text.
                """
                quiz_payload = f"Transcript:\n{st.session_state.transcript[:12000]}"
                st.session_state.quiz_result = call_groq_ai(quiz_prompt, quiz_payload)
                
        if st.session_state.quiz_result:
            render_quiz(st.session_state.quiz_result)
        else:
            st.info("Click the button above to generate a custom interactive quiz for this video.")

    with tab_translate:
        st.markdown("### 🌐 Instant Report Translation")
        st.markdown("Translate the generated intelligence report into your preferred language.")
        
        target_lang = st.selectbox("Select Target Language", ["Urdu (اردو)", "Spanish", "French", "Hindi (हिन्दी)", "Arabic (العربية)"])
        
        if st.button("🌍 Translate Report Now"):
            with st.spinner(f"Translating report to {target_lang}..."):
                trans_prompt = f"Translate the following analytical report accurately into {target_lang}, keeping the markdown formatting intact. Do not output raw HTML tags."
                translated_text = call_groq_ai(trans_prompt, st.session_state.result)
                st.markdown(translated_text)
                st.download_button(
                    label=f"📥 Download Translated Report ({target_lang})",
                    data=translated_text,
                    file_name=f"nexustube_report_{target_lang.split()[0].lower()}.md",
                    mime="text/markdown"
                )
        else:
            st.info("Select a language and click the translate button.")

    with tab_chat:
        st.markdown("### 💬 Ask Anything About This Video")
        st.markdown("Have a specific question about the video contents? Query the transcript directly via AI.")
        
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
        user_query = st.chat_input("Type your question about the video here...")
        if user_query:
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)
                
            with st.spinner("Analyzing transcript context..."):
                chat_system_prompt = "You are an expert video research assistant. Answer the user's question accurately based strictly on the provided video transcript context. Avoid raw HTML tags."
                chat_user_payload = f"Transcript Context:\n{st.session_state.transcript[:12000]}\n\nUser Question: {user_query}"
                
                ai_answer = call_groq_ai(chat_system_prompt, chat_user_payload)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_answer})
                
                with st.chat_message("assistant"):
                    st.markdown(ai_answer)
else:
    st.info("👈 **Get Started:** Enter a YouTube link in the sidebar, select your preferred settings, and click **Generate Intelligence**.")