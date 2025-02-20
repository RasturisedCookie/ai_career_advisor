from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

CAREER_CATEGORIES = [
    # Technology
    "Software Development",
    "Data Science",
    "AI/ML Engineering",
    "DevOps",
    "Cybersecurity",
    "Product Management",
    "UX/UI Design",
    
    # Business & Finance
    "Financial Analysis",
    "Investment Banking",
    "Management Consulting",
    "Business Development",
    "Marketing Strategy",
    "Human Resources",
    
    # Healthcare
    "Healthcare Administration",
    "Clinical Research",
    "Medical Practice",
    "Health Informatics",
    
    # Creative
    "Digital Marketing",
    "Content Creation",
    "Graphic Design",
    "Video Production",
    
    # Education
    "Teaching",
    "Educational Technology",
    "Academic Research",
    "Career Counseling",
    
    # Others
    "Environmental Science",
    "Legal Services",
    "Project Management",
    "Public Relations",
    "Social Work",
    "Real Estate"
]

MODEL_CONFIG = {
    "model_name": "distilbert-base-uncased",  # Smaller, faster model that's good for classification
    "max_length": 512,
    "num_labels": len(CAREER_CATEGORIES)  # Dynamic number of labels based on categories
}
