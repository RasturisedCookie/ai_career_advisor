import streamlit as st

class DataProcessor:
    def __init__(self):
        pass
    
    @staticmethod
    def validate_input(input_data):
        """Validate and clean input data"""
        if not input_data:
            return False, "No input data provided"
        
        required_fields = ['skills', 'experience']
        for field in required_fields:
            if field not in input_data:
                return False, f"Missing required field: {field}"
        
        if not input_data['skills']:
            return False, "At least one skill is required"
        
        if not input_data['experience'].get('current_role'):
            return False, "Current role is required"
        
        return True, "Input data is valid"
    
    @staticmethod
    def clean_text(text):
        """Clean and normalize text input"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        return text
    
    @staticmethod
    def normalize_skills(skills):
        """Normalize skill names"""
        if not skills:
            return []
        
        # Convert to lowercase and remove duplicates
        normalized = {s.lower().strip() for s in skills}
        
        # Remove empty strings
        normalized = {s for s in normalized if s}
        
        return list(normalized)
    
    @staticmethod
    def process_input_data(input_data):
        """Process and clean all input data"""
        if not input_data:
            return None
        
        processed = {
            'skills': DataProcessor.normalize_skills(input_data.get('skills', [])),
            'experience': {
                'level': input_data.get('experience', {}).get('level', ''),
                'current_role': DataProcessor.clean_text(input_data.get('experience', {}).get('current_role', '')),
                'industry': DataProcessor.clean_text(input_data.get('experience', {}).get('industry', ''))
            },
            'preferences': {
                'work_style': DataProcessor.clean_text(input_data.get('preferences', {}).get('work_style', '')),
                'company_size': DataProcessor.clean_text(input_data.get('preferences', {}).get('company_size', '')),
                'interests': DataProcessor.normalize_skills(input_data.get('preferences', {}).get('interests', []))
            }
        }
        
        return processed
