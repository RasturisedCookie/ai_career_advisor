import os
from openai import OpenAI
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import google.generativeai as genai
from ..config import Config

nltk.download('punkt')
nltk.download('stopwords')

class CareerAdvisorBot:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize OpenAI client with GitHub token
        token = Config.get_github_token()
        if not token:
            raise ValueError("GitHub token not set. Please set it in your Streamlit secrets.")
        
        endpoint = "https://models.inference.ai.azure.com"
        self.model_name = "gpt-4o"
        
        print(f"Token prefix: {token[:7]}...") # This will show just the start of the token
        
        self.client = OpenAI(
            base_url=endpoint,
            api_key=token,
        )
        
        # Initialize Gemini as fallback
        gemini_key = Config.get_gemini_key()
        if gemini_key:
            genai.configure(api_key=gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
        else:
            self.gemini_model = None
        
        self.system_message = {
            "role": "system",
            "content": """You are a friendly Career Advisor AI. Keep all responses under 100 words.

For career questions, reply with:
• Role: [career path]
• Skills: [3-4 key skills]
• Growth: [1-line outlook]

For non-career topics: "Let's focus on your career goals! What skills or roles interest you?"

Be warm but brief."""
        }
        
        self.conversation_history = [self.system_message]
    
    def _extract_skills(self, text):
        doc = self.nlp(text.lower())
        skill_indicators = {'experience', 'skilled', 'knowledge', 'proficient', 'expert', 'familiar'}
        tech_skills = {'python', 'java', 'javascript', 'react', 'angular', 'node', 'sql', 'aws', 'cloud'}
        
        skills = set()
        
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT"]:
                skills.add(ent.text)
        
        for token in doc:
            if token.text in tech_skills:
                skills.add(token.text)
            if token.text in skill_indicators and token.head.dep_ == 'prep':
                skills.add(token.head.text)
        
        return list(skills)
    
    def _get_gemini_response(self, user_input):
        try:
            chat = self.gemini_model.start_chat(history=[])
            chat.send_message(self.system_message["content"])
            response = chat.send_message(user_input)
            return response.text
        except Exception as e:
            return f"Error with Gemini API: {str(e)}"
    
    def get_response(self, user_input):
        try:
            self.conversation_history.append({"role": "user", "content": user_input})
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=self.conversation_history
            )
            bot_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": bot_response})
            return {"response": bot_response, "source": "openai"}
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            try:
                if self.gemini_model:
                    prompt = f"You are a friendly Career Advisor AI. Keep responses under 100 words. Question: {user_input}"
                    gemini_response = self.gemini_model.generate_content(prompt)
                    response_text = gemini_response.text
                    self.conversation_history.append({"role": "assistant", "content": response_text})
                    return {"response": response_text, "source": "gemini"}
                else:
                    raise Exception("Gemini model not initialized")
            except Exception as gemini_error:
                print(f"Gemini API error: {str(gemini_error)}")
                return {
                    "response": "I apologize, but I'm having trouble connecting to my services right now. Please check your API keys in the .streamlit/secrets.toml file and make sure they are set correctly.",
                    "source": "error"
                }
    
    def clear_conversation(self):
        self.conversation_history = [self.system_message]
