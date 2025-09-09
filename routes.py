from flask import render_template, request, redirect, url_for, session, jsonify
import json
import os
import hashlib
import uuid
from models import Quiz

def generate_user_id(email):
    """Generate a unique user ID based on email"""
    return hashlib.md5(email.encode()).hexdigest()[:12]

def get_user_id_from_session():
    """Get user ID from session"""
    return session.get('user_id')

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/colleges')
    def colleges():
        return render_template('colleges.html')

    @app.route('/api/colleges')
    def get_colleges():
        try:
            with open('colleges_data.json', 'r') as f:
                colleges = json.load(f)
            return jsonify({'success': True, 'colleges': colleges})
        except FileNotFoundError:
            return jsonify({'success': False, 'message': 'Colleges data not found'}), 404
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    @app.route('/auth')
    def auth():
        return render_template('auth.html')

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        remember_me = data.get('rememberMe', False)
        
        users_file = 'users.json'
        if os.path.exists(users_file):
            with open(users_file, 'r') as f:
                users = json.load(f)
                for user in users:
                    if user['email'] == email and user['password'] == password:
                        user_id = generate_user_id(email)
                        session['user_id'] = user_id
                        session['user_email'] = email
                        session['user_name'] = user['name']
                        
                        if remember_me:
                            session.permanent = True
                        
                        return jsonify({'success': True, 'redirect': '/'})
        
        return jsonify({'success': False, 'message': 'Invalid credentials'})

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        users_file = 'users.json'
        users = []
        if os.path.exists(users_file):
            with open(users_file, 'r') as f:
                users = json.load(f)
        
        for user in users:
            if user['email'] == email:
                return jsonify({'success': False, 'message': 'User already exists'})
        
        users.append({'name': name, 'email': email, 'password': password})
        with open(users_file, 'w') as f:
            json.dump(users, f)
        
        user_id = generate_user_id(email)
        session['user_id'] = user_id
        session['user_email'] = email
        session['user_name'] = name
        return jsonify({'success': True, 'redirect': '/'})

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

    @app.route('/quiz')
    def quiz():
        questions = Quiz.get_questions()
        return render_template('quiz.html', questions=questions)

    @app.route('/save_quiz_progress', methods=['POST'])
    def save_quiz_progress():
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not logged in'})
        
        data = request.get_json()
        user_id = get_user_id_from_session()
        progress_file = f"progress_{user_id}.json"
        
        with open(progress_file, 'w') as f:
            json.dump(data, f)
        
        return jsonify({'success': True})

    @app.route('/get_quiz_progress')
    def get_quiz_progress():
        if 'user_id' not in session:
            return jsonify({'progress': None})
        
        user_id = get_user_id_from_session()
        progress_file = f"progress_{user_id}.json"
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                progress = json.load(f)
            return jsonify({'progress': progress})
        
        return jsonify({'progress': None})

    @app.route('/results')
    def results():
        recommendations = []
        if 'user_id' in session:
            user_id = get_user_id_from_session()
            results_file = f"results_{user_id}.json"
            if os.path.exists(results_file):
                with open(results_file, 'r') as f:
                    data = json.load(f)
                    recommendations = [career[0] for career in data.get('careers', [])]
        
        return render_template('results.html', recommendations=recommendations)

    @app.route('/calculate_results', methods=['POST'])
    def calculate_results():
        data = request.get_json()
        answers = data.get('answers', [])
        
        career_scores = {
            'Software Engineer': 0,
            'Data Scientist': 0,
            'Product Manager': 0,
            'UX Designer': 0,
            'Marketing Manager': 0,
            'Business Analyst': 0,
            'Cybersecurity Specialist': 0,
            'DevOps Engineer': 0
        }
        
        for answer_obj in answers:
            question_id = answer_obj.get('questionId')
            answer_value = answer_obj.get('answer', 0)
            
            if question_id == 1 or question_id == 7:
                career_scores['Data Scientist'] += answer_value
                career_scores['Business Analyst'] += answer_value
            elif question_id == 2:
                career_scores['Software Engineer'] += answer_value
                career_scores['Cybersecurity Specialist'] += answer_value
                career_scores['DevOps Engineer'] += answer_value
            elif question_id == 3:
                career_scores['Data Scientist'] += answer_value
            elif question_id == 4:
                career_scores['UX Designer'] += answer_value
            elif question_id == 5 or question_id == 6:
                career_scores['Product Manager'] += answer_value
                career_scores['Marketing Manager'] += answer_value
            elif question_id == 8:
                career_scores['UX Designer'] += answer_value
            elif question_id == 9:
                career_scores['Software Engineer'] += answer_value
                career_scores['DevOps Engineer'] += answer_value
            elif question_id == 10:
                career_scores['Product Manager'] += answer_value
                career_scores['Business Analyst'] += answer_value
                career_scores['Marketing Manager'] += answer_value
        
        sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
        top_careers = sorted_careers[:3]
        
        if 'user_id' in session:
            user_id = get_user_id_from_session()
            results_file = f"results_{user_id}.json"
            with open(results_file, 'w') as f:
                json.dump({'careers': top_careers, 'answers': answers}, f)
        
        return jsonify({'careers': top_careers})
