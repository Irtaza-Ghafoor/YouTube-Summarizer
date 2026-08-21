# ⚡ NexusTube AI - Next-Gen Video Intelligence Hub

<div align="center">

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python Version](https://img.shields.io/badge/Python-3.10%257C3.11%257C3.12-blue.svg)](https://www.python.org/)
[![Groq API](https://img.shields.io/badge/Powered%2520by-Groq%2520Llama-orange.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Transform lengthy YouTube lectures, tutorials, and podcasts into structured intelligence reports, interactive quizzes, multi-language translations, and real-time conversational insights.

</div>

---

## 🚀 Overview

**NexusTube AI** is a state-of-the-art SaaS application designed to eliminate information overload from long-form video content. Powered by ultra-fast LLMs via the **Groq API** and **YouTube Transcript API**, NexusTube extracts transcript data and leverages advanced prompt engineering to deliver comprehensive intelligence reports in seconds.

---

## ✨ Core Features

*   **🎯 Multiple Intelligence Modes:** 
    *   *Comprehensive Summary*: Deep, well-structured analytical breakdowns.
    *   *Key Bullet Points*: High-impact lessons and core facts extracted cleanly.
    *   *Chapter Breakdown*: Logical section flows with structured summaries.
*   **🎭 Dynamic Report Tones:** Customize output styles—choose between *Executive / Professional*, *Simple & Beginner Friendly*, or *Technical & Developer Focused*.
*   **🧠 AI Quiz Hub:** Automatically generates 5 interactive multiple-choice questions (MCQs) from the transcript with hidden answers to test your knowledge.
*   **🌐 Instant Report Translation:** Translate reports seamlessly into Urdu (اردو), Spanish, French, Hindi, and Arabic.
*   **💬 Chat with Video:** An interactive RAG-powered chat interface enabling users to query the transcript directly for precise answers.
*   **📥 Export Functionality:** Download generated intelligence reports instantly in Markdown (`.md`) format.

---

## 🛠️ Tech Stack

*   **Frontend & UI:** Streamlit (with custom high-end SaaS glassmorphism CSS styling)
*   **AI Engine:** Groq API (`llama-3.3-70b-versatile` / Llama models)
*   **Data Extraction:** `youtube-transcript-api`
*   **Environment Management:** Python-dotenv

---

## ⚙️ Local Installation & Setup

Follow these steps to run NexusTube AI locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Irtaza-Ghafoor/YouTube-Summarizer.git](https://github.com/Irtaza-Ghafoor/YouTube-Summarizer.git)
   cd YouTube-Summarizer

# 1. **Create and activate a virtual environment:**
python -m venv venv

 **On Windows:**

venv\Scripts\activate

 **On Mac/Linux:**
 
source venv/bin/activate

# 2. **Install dependencies:**
pip install -r requirements.txt

# 3. **Configure Environment Variables:**
Create a .env file in the root directory and add your Groq API key:

GROQ_API_KEY=your_actual_groq_api_key_here

# 4.**Run the Streamlit Application:**
streamlit run app.py

# 📦 Requirements (requirements.txt)
streamlit

youtube-transcript-api

groq

python-dotenv

# **💡 How to Use**
Paste any valid YouTube Video URL into the sidebar input.

Select your preferred Intelligence Mode and Report Tone.

Click "✨ Generate Intelligence".

Explore the analytics metrics, read the breakdown report, test your knowledge in the Quiz Hub, translate it, or chat directly with the video!