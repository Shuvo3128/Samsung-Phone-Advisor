import streamlit as st
import requests
import time
import uuid

# ======================================================
# CONFIG
# ======================================================
API_URL = "http://127.0.0.1:8000/api/ask"
REQUEST_TIMEOUT = 120

st.set_page_config(
    page_title="Samsung Phone Advisor",
    page_icon="📱",
    layout="wide",
)

# ======================================================
# CUSTOM CSS
# ======================================================
st.markdown(
    """
    <style>
    body { background-color: #f9fafb; }
    .chat-box {
        padding: 14px 16px;
        border-radius: 10px;
        margin-bottom: 14px;
        line-height: 1.6;
        font-size: 15px;
    }
    .user-msg {
        background-color: #eef2ff;
        border-left: 4px solid #6366f1;
    }
    .bot-msg {
        background-color: #ffffff;
        border-left: 4px solid #22c55e;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .title-text {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .subtitle {
        color: #6b7280;
        font-size: 15px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ======================================================
# SESSION STATE INIT
# ======================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# ======================================================
# CALLBACKS (IMPORTANT)
# ======================================================
def clear_chat():
    st.session_state.chat_history = []
    st.session_state.user_input = ""

def send_message():
    question = st.session_state.user_input.strip()
    if not question:
        return

    st.session_state.chat_history.append(("user", question))

    try:
        response = requests.post(
            API_URL,
            json={"question": question},
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code == 200:
            answer = response.json().get("answer", "No response returned.")
        else:
            answer = f"❌ API error (status {response.status_code})"

    except requests.exceptions.ConnectionError:
        answer = (
            "❌ Cannot connect to backend.\n\n"
            "Run:\n`uvicorn app.main:app --reload`"
        )
    except requests.exceptions.Timeout:
        answer = "❌ Request timed out."
    except Exception as e:
        answer = f"❌ Error: {e}"

    st.session_state.chat_history.append(("assistant", answer))
    st.session_state.user_input = ""

# ======================================================
# SIDEBAR
# ======================================================
with st.sidebar:
    st.markdown("### ⚙️ Controls")
    st.button("🧹 Clear Chat", on_click=clear_chat)

    st.divider()
    st.markdown("### ℹ️ Session Info")
    st.code(st.session_state.session_id)

# ======================================================
# HEADER
# ======================================================
st.markdown('<div class="title-text">📱 Samsung Phone Advisor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-powered Samsung recommendations using Database • RAG • Multi-Agent System</div>',
    unsafe_allow_html=True,
)

st.divider()

# ======================================================
# INPUT AREA
# ======================================================
st.text_input(
    "Ask a question",
    placeholder="e.g. Compare Samsung Galaxy S23 Ultra and S22 Ultra",
    key="user_input",
)

st.button("Ask 🚀", on_click=send_message)
st.caption("Try: *best Samsung phone under $1000*")

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
    "Built with FastAPI • PostgreSQL • SQL-based RAG • Multi-Agent System • Ollama (Local LLM)"
)
