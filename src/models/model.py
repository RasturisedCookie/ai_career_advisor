import streamlit as st
from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np

class CareerAdvisor:
    def __init__(self):
        """Initialize the career advisor with a pre-trained model"""
        self._initialize_career_mapping()
        self._load_model()
        
    def _initialize_career_mapping(self):
        """Initialize career categories and their descriptions"""
        self.careers = {
            "Software Development": {
                "description": "Design and develop software applications and systems",
                "keywords": ["programming", "coding", "software engineering", "web development", "mobile development"],
                "required_skills": ["Python", "Java", "JavaScript", "SQL"],
                "domain": "Technology"
            },
            "Data Science": {
                "description": "Analyze and interpret complex data sets to inform business decisions",
                "keywords": ["data analysis", "machine learning", "statistics", "big data"],
                "required_skills": ["Python", "R", "SQL", "Machine Learning"],
                "domain": "Technology"
            },
            "UX/UI Design": {
                "description": "Design user interfaces and improve user experience for digital products",
                "keywords": ["user experience", "interface design", "wireframing", "prototyping"],
                "required_skills": ["UI Design", "UX Design", "Figma", "Adobe XD"],
                "domain": "Creative"
            },
            "Product Management": {
                "description": "Lead product development and strategy",
                "keywords": ["product strategy", "roadmap planning", "agile", "stakeholder management"],
                "required_skills": ["Product Strategy", "Agile", "Communication"],
                "domain": "Business"
            },
            "Digital Marketing": {
                "description": "Plan and execute digital marketing campaigns",
                "keywords": ["marketing strategy", "social media", "SEO", "content marketing"],
                "required_skills": ["Marketing", "Social Media", "Analytics"],
                "domain": "Marketing"
            },
            "Financial Analysis": {
                "description": "Analyze financial data and make recommendations",
                "keywords": ["financial modeling", "investment analysis", "risk assessment"],
                "required_skills": ["Financial Analysis", "Excel", "Statistics"],
                "domain": "Finance"
            },
            "Healthcare Administration": {
                "description": "Manage healthcare facilities and operations",
                "keywords": ["healthcare management", "patient care", "medical administration"],
                "required_skills": ["Healthcare Management", "Administration", "Communication"],
                "domain": "Healthcare"
            },
            "Educational Technology": {
                "description": "Develop and implement technology solutions for education",
                "keywords": ["e-learning", "educational software", "instructional design"],
                "required_skills": ["Educational Technology", "Instructional Design", "LMS"],
                "domain": "Education"
            }
        }

    def _load_model(self):
        """Load the sentence transformer model"""
        try:
            st.info("Loading AI model...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            st.success("AI model loaded successfully!")
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            self.model = None

    def _prepare_input_text(self, input_data):
        """Prepare input text from user data"""
        parts = []
        
        # Add skills
        if 'skills' in input_data and input_data['skills']:
            parts.append(f"Skills: {', '.join(input_data['skills'])}")
        
        # Add experience
        if 'experience' in input_data:
            exp = input_data['experience']
            if 'current_role' in exp and exp['current_role']:
                parts.append(f"Current Role: {exp['current_role']}")
            if 'level' in exp:
                parts.append(f"Experience Level: {exp['level']}")
            if 'industry' in exp:
                parts.append(f"Industry: {exp['industry']}")
        
        # Add preferences
        if 'preferences' in input_data:
            pref = input_data['preferences']
            if 'interests' in pref and pref['interests']:
                parts.append(f"Interests: {', '.join(pref['interests'])}")
            if 'career_goals' in pref:
                parts.append(f"Career Goals: {pref['career_goals']}")
            if 'work_environment' in pref:
                parts.append(f"Preferred Environment: {pref['work_environment']}")
        
        return " | ".join(parts)

    def get_top_careers(self, input_data, top_k=3):
        """Get career recommendations using semantic similarity"""
        if not self.model:
            st.error("Model not loaded. Using fallback recommendations.")
            return self._get_fallback_recommendations(input_data, top_k)

        # Prepare input text
        input_text = self._prepare_input_text(input_data)
        
        try:
            # Encode input text
            with st.spinner("Analyzing your profile with AI..."):
                input_embedding = self.model.encode(input_text)
                
                # Prepare and encode career descriptions
                career_texts = []
                career_names = []
                
                for career, info in self.careers.items():
                    desc = (f"{career}: {info['description']}. "
                           f"Keywords: {', '.join(info['keywords'])}. "
                           f"Required Skills: {', '.join(info['required_skills'])}. "
                           f"Domain: {info['domain']}")
                    career_texts.append(desc)
                    career_names.append(career)
                
                # Encode all career descriptions
                career_embeddings = self.model.encode(career_texts)
                
                # Calculate similarities
                similarities = util.pytorch_cos_sim(input_embedding, career_embeddings)[0]
                
                # Get top k careers
                top_indices = torch.topk(similarities, min(top_k, len(career_names))).indices
                
                recommendations = []
                for idx in top_indices:
                    score = similarities[idx].item()
                    if score >= 0.3:  # Minimum 30% similarity threshold
                        recommendations.append({
                            'career': career_names[idx],
                            'confidence': round(score * 100, 1)
                        })
                
                return recommendations

        except Exception as e:
            st.error(f"Error in AI predictions: {str(e)}")
            return self._get_fallback_recommendations(input_data, top_k)

    def _get_fallback_recommendations(self, input_data, top_k=3):
        """Fallback method using keyword matching"""
        user_skills = set(skill.lower() for skill in input_data.get('skills', []))
        user_interests = set(interest.lower() for interest in 
                           input_data.get('preferences', {}).get('interests', []))
        
        scores = []
        for career, info in self.careers.items():
            # Calculate skill match
            required_skills = set(skill.lower() for skill in info['required_skills'])
            skill_match = len(user_skills & required_skills) / len(required_skills) if required_skills else 0
            
            # Calculate keyword match
            keywords = set(kw.lower() for kw in info['keywords'])
            keyword_match = len((user_skills | user_interests) & keywords) / len(keywords) if keywords else 0
            
            # Calculate final score
            score = (skill_match * 0.7 + keyword_match * 0.3) * 100
            
            if score >= 30:  # Minimum 30% match required
                scores.append({
                    'career': career,
                    'confidence': round(score, 1)
                })
        
        # Sort by score and return top-k
        scores.sort(key=lambda x: x['confidence'], reverse=True)
        return scores[:top_k]
