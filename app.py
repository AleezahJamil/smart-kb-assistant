import streamlit as st
from chatbot import ask_question
from weather import get_weather
from wikipedia_api import get_wikipedia_summary
from data_loader import load_pdf, split_into_chunks
from vector_db import add_chunks

st.set_page_config(
    page_title="Smart KBA",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.stApp{
    background: #0b0f19;
}
.brand{
    font-size:20px;
    font-weight:700;
    color:#e2e8f0;
    margin-bottom:4px;
}
.hello-title{
    text-align:center;
    font-size:38px;
    font-weight:700;
    color:#f1f5f9;
    margin-bottom:4px;
}
.hello-sub{
    text-align:center;
    color:#94a3b8;
    font-size:16px;
    margin-bottom:24px;
}
.capability-label{
    text-align:center;
    color:#64748b;
    font-size:13px;
    margin-bottom:14px;
}
.feature-card{
    background:#141925;
    border:1px solid #232838;
    border-radius:14px;
    padding:18px;
    color:#e2e8f0;
}
.feature-icon{ font-size:22px; margin-bottom:6px; }
.feature-title{ font-weight:600; font-size:15px; margin-bottom:2px; }
.feature-desc{ color:#64748b; font-size:12px; }
.nav-item{
    background:#141925;
    border:1px solid #232838;
    border-radius:10px;
    padding:10px 14px;
    margin-bottom:6px;
    color:#cbd5e1;
    font-size:14px;
}
.nav-item-active{
    background:#4f46e5;
    border:1px solid #4f46e5;
    color:white;
    font-weight:600;
}
.doc-status-card{
    background:#141925;
    border:1px solid #232838;
    border-radius:12px;
    padding:16px;
    margin-top:10px;
}
.doc-count{ font-size:26px; font-weight:700; color:#f1f5f9; }
.doc-label{ color:#64748b; font-size:12px; }
.status-dot{ color:#22c55e; font-size:12px; }
.badge{
    display:inline-block;
    padding:3px 10px;
    border-radius:14px;
    font-size:11px;
    font-weight:700;
    margin-bottom:6px;
}
.badge-doc{ background:rgba(99,102,241,0.15); color:#818cf8; }
.badge-weather{ background:rgba(34,197,94,0.15); color:#4ade80; }
.badge-wiki{ background:rgba(250,204,21,0.15); color:#facc15; }
div[data-testid="stChatInput"]{ border-radius:16px; }
.stChatMessage{ border-radius:16px; }
.footer-tag{
    text-align:center;
    color:#475569;
    font-size:12px;
    margin-top:20px;
}
footer{ visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown('<p class="brand">🧠 Smart KBA</p>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="nav-item nav-item-active">💬 Chat</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">📄 Documents</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">🌦 Weather</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">📚 Wikipedia</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**📂 Your Documents**")

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file is not None:
        save_path = f"pdfs/{uploaded_file.name}"
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        with st.spinner("Indexing document..."):
            text = load_pdf(save_path)
            chunks = split_into_chunks(text)
            add_chunks(chunks)
        st.success(f"✅ {uploaded_file.name} indexed!")

    st.markdown("""
    <div class="doc-status-card">
        <div class="doc-count">1</div>
        <div class="doc-label">Document Indexed</div>
        <div class="status-dot">● All systems ready</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.session_state.get("messages"):
        if st.button("🗑 Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")
    st.markdown("**Built with**")
    st.markdown("""
    <span style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:4px 10px;margin:3px;font-size:12px;color:#cbd5e1;display:inline-block;">Groq</span>
    <span style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:4px 10px;margin:3px;font-size:12px;color:#cbd5e1;display:inline-block;">ChromaDB</span>
    <span style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:4px 10px;margin:3px;font-size:12px;color:#cbd5e1;display:inline-block;">MCP</span>
    <span style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:4px 10px;margin:3px;font-size:12px;color:#cbd5e1;display:inline-block;">Wikipedia</span>
    <span style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:4px 10px;margin:3px;font-size:12px;color:#cbd5e1;display:inline-block;">OpenWeather</span>
    """, unsafe_allow_html=True)

# ---------------- Main Area ----------------
st.markdown('<p class="hello-title">Hello! 👋</p>', unsafe_allow_html=True)
st.markdown('<p class="hello-sub">How can I help you today?</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    st.markdown('<p class="capability-label">I can help you with:</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-card"><div class="feature-icon">📄</div><div class="feature-title">Documents</div><div class="feature-desc">Search your uploaded documents</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-card"><div class="feature-icon">🌦</div><div class="feature-title">Weather</div><div class="feature-desc">Get real-time weather updates</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-card"><div class="feature-icon">📚</div><div class="feature-title">Wikipedia</div><div class="feature-desc">Explore knowledge from Wikipedia</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ---------------- Chat History ----------------
for message in st.session_state.messages:
    avatar = "🧑" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        if message["role"] == "assistant" and "badge" in message:
            st.markdown(f'<span class="badge {message["badge"]}">{message["badge_label"]}</span>', unsafe_allow_html=True)
        st.write(message["content"])

# ---------------- Chat Input ----------------
user_input = st.chat_input("Ask anything...", key="main_chat_input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.write(user_input)

    with st.spinner("🤖 Thinking..."):
        text = user_input.lower()

        if "weather" in text:
            city = user_input.split()[-1]
            answer = get_weather(city)
            badge, badge_label = "badge-weather", "🌦 WEATHER"
        elif text.startswith("who is"):
            topic = user_input[7:].strip()
            answer = get_wikipedia_summary(topic)
            badge, badge_label = "badge-wiki", "📚 WIKIPEDIA"
        elif text.startswith("what is"):
            topic = user_input[8:].strip()
            answer = get_wikipedia_summary(topic)
            badge, badge_label = "badge-wiki", "📚 WIKIPEDIA"
        else:
            answer = ask_question(user_input)
            badge, badge_label = "badge-doc", "📄 DOCUMENTS"

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "badge": badge,
        "badge_label": badge_label
    })
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(f'<span class="badge {badge}">{badge_label}</span>', unsafe_allow_html=True)
        st.write(answer)

# ---------------- Footer ----------------
st.markdown('<p class="footer-tag">● Powered by Groq • ChromaDB • MCP</p>', unsafe_allow_html=True)