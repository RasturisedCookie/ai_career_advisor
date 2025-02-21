import streamlit as st

# Configuration class to manage API settings
class Config:
    @staticmethod
    def get_github_token():
        if 'GITHUB_TOKEN' not in st.session_state:
            st.session_state.GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
            if not st.session_state.GITHUB_TOKEN:
                raise ValueError("GitHub token not found in secrets.toml")
        return st.session_state.GITHUB_TOKEN
    
    @staticmethod
    def get_gemini_key():
        if 'GEMINI_API_KEY' not in st.session_state:
            st.session_state.GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
            if not st.session_state.GEMINI_API_KEY:
                raise ValueError("Gemini API key not found in secrets.toml")
        return st.session_state.GEMINI_API_KEY
