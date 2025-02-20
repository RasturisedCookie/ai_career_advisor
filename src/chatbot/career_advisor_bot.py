import os
from openai import OpenAI
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from dotenv import load_dotenv

nltk.download('punkt')
nltk.download('stopwords')

class CareerAdvisorBot:
    def __init__(self):
        load_dotenv()
        self.nlp = spacy.load("en_core_web_sm")
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.environ["GITHUB_TOKEN"]
        )
        
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
    
    def get_response(self, user_input):
        try:
            skills = self._extract_skills(user_input)
            self.conversation_history.append({"role": "user", "content": user_input})
            
            response = self.client.chat.completions.create(
                messages=self.conversation_history,
                model="gpt-4o",
                temperature=0.7,
                stream=True
            )
            
            full_response = ""
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
            
            self.conversation_history.append({"role": "assistant", "content": full_response})
            
            if len(self.conversation_history) > 7:
                self.conversation_history = [self.system_message] + self.conversation_history[-6:]
            
            return {"response": full_response, "extracted_skills": skills}
            
        except Exception as e:
            return {"response": "I apologize, but I encountered an error. Please try asking your career question again.", "extracted_skills": []}
    
    def clear_conversation(self):
        self.conversation_history = [self.system_message]
