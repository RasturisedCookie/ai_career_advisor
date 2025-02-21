import streamlit as st
from src.chatbot.career_advisor_bot import CareerAdvisorBot

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    /* Modern Dark Theme */
    .stApp {
        background-color: #1a1a1a;
    }

    /* Main container width control */
    .main > div {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 1000px !important;
        margin: 0 auto !important;
    }

    /* Chat container styling */
    .chat-container {
        max-width: 800px !important;
        margin: 0 auto !important;
        padding: 1rem !important;
    }

    /* Message styling */
    .stChatMessage {
        background-color: #2d2d2d !important;
        border-radius: 12px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        border: 1px solid #3d3d3d !important;
    }

    /* Chat input container styling */
    .chat-input-container {
        max-width: 800px !important;
        width: 100% !important;
        margin: 0 auto !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        padding: 0 1rem !important;
    }

    /* Input box styling */
    .stChatInput {
        background-color: #2d2d2d !important;
        border-radius: 25px !important;
        border: 1px solid #3d3d3d !important;
        color: white !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }

    .stChatInput > div {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Fix input alignment */
    .stChatFloatingInputContainer {
        bottom: 0 !important;
        position: fixed !important;
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        background: #1a1a1a !important;
        padding: 1rem !important;
        margin: 0 !important;
        z-index: 999 !important;
        display: flex !important;
        justify-content: center !important;
    }

    .stChatFloatingInputContainer > div {
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        max-width: 800px !important;
        width: 100% !important;
        margin: 0 auto !important;
        padding: 0 1rem !important;
    }

    /* Fix textarea */
    .stChatInput textarea {
        padding: 12px 20px !important;
        min-height: 44px !important;
        max-height: 200px !important;
        overflow-y: auto !important;
        resize: none !important;
        background: transparent !important;
        width: 100% !important;
        margin: 0 !important;
        box-sizing: border-box !important;
    }

    /* Delete button specific styling */
    .delete-btn {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
    }

    .delete-btn button {
        border-radius: 50% !important;
        width: 44px !important;
        height: 44px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-width: 44px !important;
        flex-shrink: 0 !important;
        margin: 0 !important;
    }

    /* Text colors */
    h1, h2, h3, p {
        color: #ffffff !important;
    }

    .stMarkdown {
        color: #ffffff !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Suggestions container */
    .suggestions-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        margin: 20px auto;
        max-width: 800px;
        padding: 0 1rem;
    }

    /* Add padding at the bottom for fixed input */
    .chat-interface {
        padding-bottom: 100px !important;
    }

    /* Custom block container */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1000px !important;
        margin: 0 auto !important;
    }
</style>
""", unsafe_allow_html=True)

def create_chat_interface():
    st.markdown("<div class='chat-interface'>", unsafe_allow_html=True)
    
    suggestions = [
        "Skills needed for AI?",
        "Data science job market?",
        "Dev to Product Manager path?",
        "Top paying tech roles?"
    ]

    # Create suggestion container
    st.markdown('<div class="suggestions-container">', unsafe_allow_html=True)
    cols = st.columns(len(suggestions))
    for idx, suggestion in enumerate(suggestions):
        with cols[idx]:
            if st.button(suggestion, key=f"suggestion_{idx}"):
                if 'chatbot' not in st.session_state:
                    st.session_state.chatbot = CareerAdvisorBot()
                if 'chat_history' not in st.session_state:
                    st.session_state.chat_history = []
                
                st.session_state.chat_history.append({"role": "user", "content": suggestion})
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.get_response(suggestion)
                    st.session_state.chat_history.append({"role": "assistant", "content": response["response"]})
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = CareerAdvisorBot()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Chat messages container
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        st.markdown('</div>', unsafe_allow_html=True)

    # Input container at the bottom
    input_container = st.container()
    with input_container:
        st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
        input_cols = st.columns([0.1, 0.9])
        
        with input_cols[0]:
            st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
            if st.button("🗑️", key="clear_chat"):
                st.session_state.chat_history = []
                st.session_state.chatbot.clear_conversation()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with input_cols[1]:
            if prompt := st.chat_input("Ask anything about your career journey...", key="chat_input"):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.get_response(prompt)
                    st.session_state.chat_history.append({"role": "assistant", "content": response["response"]})
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>🚀 AI Career Advisor</h1>", unsafe_allow_html=True)
    create_chat_interface()

if __name__ == "__main__":
    main()