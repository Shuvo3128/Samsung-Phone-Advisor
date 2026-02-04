import streamlit as st
import requests
import time

# ======================================================
# CONFIG
# ======================================================
API_URL = "http://127.0.0.1:8000/api/ask"
REQUEST_TIMEOUT = 120

st.set_page_config(
    page_title="Samsung Phone Advisor",
    page_icon="📱",
    layout="centered",
)

# ======================================================
# CUSTOM CSS (clean + modern)
# ======================================================
st.markdown(
    """
    <style>
    .chat-box {
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 12px;
        line-height: 1.6;
    }
    .user-msg {
        background-color: #eef2ff;
        border-left: 5px solid #6366f1;
    }
    .bot-msg {
        background-color: #f8fafc;
        border-left: 5px solid #22c55e;
    }
    .title-text {
        font-size: 32px;
        font-weight: 700;
    }
    .subtitle {
        color: #6b7280;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ======================================================
# HEADER
# ======================================================
st.markdown('<div class="title-text">📱 Samsung Phone Advisor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-powered Samsung recommendations using Database + RAG + LLM</div>',
    unsafe_allow_html=True,
)

st.divider()

# ======================================================
# SESSION STATE
# ======================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ======================================================
# INPUT AREA
# ======================================================
question = st.text_area(
    "Ask your question",
    placeholder="e.g. Compare Samsung Galaxy S23 Ultra and S22 Ultra",
    height=90,
)

col1, col2 = st.columns([1, 3])
with col1:
    ask_btn = st.button("Ask 📩")
with col2:
    clear_btn = st.button("Clear 🧹")

if clear_btn:
    st.session_state.chat_history = []
    st.rerun()


# ======================================================
# HANDLE REQUEST
# ======================================================
if ask_btn:
    if not question.strip():
        st.warning("⚠️ Please enter a question.")
    else:
        st.session_state.chat_history.append(("user", question))

        with st.spinner("🤖 Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=REQUEST_TIMEOUT,
                )

                if response.status_code == 200:
                    answer = response.json().get(
                        "answer", "No answer returned from backend."
                    )
                else:
                    answer = f"❌ API error (status {response.status_code})"

            except requests.exceptions.ConnectionError:
                answer = (
                    "❌ Cannot connect to backend.\n\n"
                    "Make sure FastAPI is running:\n"
                    "`uvicorn app.main:app --reload`"
                )
            except requests.exceptions.Timeout:
                answer = "❌ Request timed out. LLM may be busy."
            except Exception as e:
                answer = f"❌ Unexpected error: {e}"

        st.session_state.chat_history.append(("assistant", answer))
        time.sleep(0.25)

# ======================================================
# CHAT DISPLAY
# ======================================================
for role, message in st.session_state.chat_history:
    if role == "user":
        st.markdown(
            f"""
            <div class="chat-box user-msg">
            <strong>🧑 You</strong><br>{message}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="chat-box bot-msg">
            <strong>🤖 Advisor</strong><br>{message}
            </div>
            """,
            unsafe_allow_html=True,
        )

# ======================================================
# FOOTER
# ======================================================
st.divider()
st.caption(
    "Built with FastAPI • PostgreSQL • RAG • Multi-Agent System • Ollama (Local LLM)"
)
