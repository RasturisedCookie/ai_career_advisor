import streamlit as st
from src.chatbot.career_advisor_bot import CareerAdvisorBot

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }

    .stButton button {
        border-radius: 20px;
        height: 38px;
        width: 38px;
        line-height: 38px;
        background-color: rgb(255, 75, 75);
        color: white;
        font-weight: 400;
        padding: 0;
        border: none;
        transition: all 0.2s ease;
        margin-right: 10px;
    }
    
    .stButton button:hover {
        background-color: rgb(255, 45, 45);
    }

    @keyframes popIn {
        0% {
            opacity: 0;
            transform: scale(0.8) translateY(20px);
        }
        100% {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }

    .stChatMessage {
        background-color: #262b36 !important;
        margin-bottom: 1rem;
        padding: 1rem;
        border-radius: 10px;
        animation: popIn 0.3s ease-out forwards;
        transform-origin: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stChatMessage p {
        color: rgba(255, 255, 255, 0.95) !important;
        line-height: 1.5;
        font-size: 1rem;
    }

    .stChatMessage [data-testid="StyledLinkIconContainer"] {
        color: rgba(255, 255, 255, 0.7) !important;
    }

    .stChatInput {
        border-radius: 20px !important;
        background-color: #262b36 !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }

    .stChatInput:focus {
        border-color: rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.2) !important;
    }

    footer {
        display: none !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #0e1117;
    }

    .chat-container {
        margin-bottom: 100px;
        padding-bottom: 20px;
    }

    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #0e1117;
        padding: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 1000;
        backdrop-filter: blur(10px);
    }

    .input-container > div {
        max-width: 800px;
        margin: 0 auto;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 800px;
    }

    h1, h2, h3, p {
        color: rgba(255, 255, 255, 0.95) !important;
    }

    [data-testid="stMarkdownContainer"] {
        color: rgba(255, 255, 255, 0.95) !important;
    }

    /* Style bullet points */
    [data-testid="stMarkdownContainer"] ul {
        list-style-type: none;
        padding-left: 0;
    }

    [data-testid="stMarkdownContainer"] ul li {
        padding-left: 1.5em;
        position: relative;
        margin: 0.5em 0;
        color: rgba(255, 255, 255, 0.95) !important;
    }

    [data-testid="stMarkdownContainer"] ul li:before {
        content: "•";
        position: absolute;
        left: 0.5em;
        color: rgb(255, 75, 75);
    }
</style>
""", unsafe_allow_html=True)

def create_chat_interface():
    st.markdown("""
    Try asking:
    • Skills needed for AI?
    • Data science job market?
    • Dev to Product Manager path?
    • Top paying tech roles?
    """)
    
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = CareerAdvisorBot()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in reversed(st.session_state.chat_history):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    input_cols = st.columns([0.5, 7])
    
    with input_cols[0]:
        if st.button("🗑️"):
            st.session_state.chat_history = []
            st.session_state.chatbot.clear_conversation()
            st.rerun()
    
    with input_cols[1]:
        if prompt := st.chat_input("Ask me about career paths..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.get_response(prompt)
                st.session_state.chat_history.append({"role": "assistant", "content": response["response"]})
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.markdown("# 🚀 AI Career Advisor\nAsk anything about your career journey")
    create_chat_interface()

if __name__ == "__main__":
    main()