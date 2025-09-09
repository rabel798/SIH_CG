users = {}

questions = [
    {"id": 1, "question": "Do you enjoy solving math problems?", "category": "analytical"},
    {"id": 2, "question": "Do you like working with computers and technology?", "category": "technical"},
    {"id": 3, "question": "Do you enjoy studying Biology and life sciences?", "category": "scientific"},
    {"id": 4, "question": "Do you like reading and writing essays/stories?", "category": "linguistic"},
    {"id": 5, "question": "Do you prefer working in groups or individually?", "category": "social"},
    {"id": 6, "question": "Do you like learning about history and society?", "category": "social"},
    {"id": 7, "question": "Do you enjoy logical puzzles and problem-solving?", "category": "analytical"},
    {"id": 8, "question": "Do you enjoy designing or creating art/music?", "category": "creative"},
    {"id": 9, "question": "Do you prefer practical experiments over theory?", "category": "practical"},
    {"id": 10, "question": "Do you like business, finance, and management?", "category": "business"}
]

career_recommendations = {
    "analytical": ["Data Scientist", "Software Engineer", "Financial Analyst", "Research Scientist"],
    "technical": ["Software Developer", "Cybersecurity Specialist", "AI/ML Engineer", "Systems Administrator"],
    "scientific": ["Biotechnologist", "Medical Doctor", "Research Scientist", "Environmental Scientist"],
    "linguistic": ["Content Writer", "Journalist", "Teacher", "Translator"],
    "social": ["Social Worker", "HR Manager", "Counselor", "Public Relations"],
    "creative": ["Graphic Designer", "Architect", "Musician", "Film Director"],
    "practical": ["Engineer", "Technician", "Lab Assistant", "Quality Control"],
    "business": ["Business Analyst", "Marketing Manager", "Entrepreneur", "Investment Banker"]
}

class User:
    @staticmethod
    def create_user(email, password, name):
        if email in users:
            return False
        users[email] = {
            'password': password, 
            'name': name, 
            'quiz_answers': [],
            'current_question': 0
        }
        return True
    
    @staticmethod
    def authenticate(email, password):
        return email in users and users[email]['password'] == password
    
    @staticmethod
    def get_user(email):
        return users.get(email, {})
    
    @staticmethod
    def save_quiz_progress(email, answers, current_question):
        if email in users:
            users[email]['quiz_answers'] = answers
            users[email]['current_question'] = current_question
            return True
        return False
    
    @staticmethod
    def get_quiz_progress(email):
        user_data = users.get(email, {})
        return {
            'answers': user_data.get('quiz_answers', []),
            'currentQuestion': user_data.get('current_question', 0)
        }

class Quiz:
    @staticmethod
    def get_questions():
        return questions
    
    @staticmethod
    def calculate_recommendations(answers):
        category_scores = {}
        for answer in answers:
            question = next((q for q in questions if q['id'] == answer['questionId']), None)
            if question:
                category = question['category']
                if category not in category_scores:
                    category_scores[category] = 0
                category_scores[category] += answer['answer']
        
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        recommendations = []
        for category, score in sorted_categories:
            careers = career_recommendations.get(category, [])
            recommendations.extend(careers[:2])
        
        return recommendations[:6]
