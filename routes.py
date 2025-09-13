from flask import render_template, request, redirect, url_for, session, jsonify
import json
import os
import hashlib
import uuid
from models import Quiz
from database import (
    init_database, generate_user_id, create_user, authenticate_user,
    save_quiz_progress, get_quiz_progress, clear_quiz_progress,
    save_quiz_results, get_quiz_results, has_completed_quiz
)

def get_user_id_from_session():
    """Get user ID from session"""
    return session.get('user_id')

def init_routes(app):
    # Initialize database on startup
    init_database()
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/check_login_status')
    def check_login_status():
        if 'user_id' in session:
            user_id = get_user_id_from_session()
            is_first_time = not has_completed_quiz(user_id)
            return jsonify({
                'logged_in': True,
                'user_name': session.get('user_name'),
                'is_first_time': is_first_time
            })
        return jsonify({'logged_in': False})

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
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        # Authenticate user
        user = authenticate_user(email, password)
        if user:
            user_id = generate_user_id(email)
            session['user_id'] = user_id
            session['user_email'] = email
            session['user_name'] = name  # Use the name from login form
            
            
            # Check if this is first-time login
            is_first_time = not has_completed_quiz(user_id)
            session['is_first_time'] = is_first_time
            
            return jsonify({'success': True, 'redirect': '/', 'is_first_time': is_first_time})
        
        return jsonify({'success': False, 'message': 'Invalid credentials'})

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        # Create new user
        success = create_user(name, email, password)
        if success:
            user_id = generate_user_id(email)
            session['user_id'] = user_id
            session['user_email'] = email
            session['user_name'] = name
            session['is_first_time'] = True  # Registration is always first-time
            
            
            return jsonify({'success': True, 'redirect': '/', 'is_first_time': True})
        else:
            return jsonify({'success': False, 'message': 'User already exists'})

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

    @app.route('/clear_session')
    def clear_session():
        """Clear session data - useful for testing"""
        session.clear()
        return jsonify({'success': True, 'message': 'Session cleared'})

    @app.route('/quiz')
    def quiz():
        # Check if user is logged in
        if 'user_id' not in session:
            return redirect(url_for('auth'))
        
        # Check if this is first-time login
        user_id = get_user_id_from_session()
        is_first_time = not has_completed_quiz(user_id)
        
        if is_first_time:
            # First-time users can access quiz
            questions = Quiz.get_questions()
            has_completed = False
        else:
            # Returning users - check if they have completed the quiz
            questions = Quiz.get_questions()
            has_completed = has_completed_quiz(user_id)
        
        return render_template('quiz.html', questions=questions, has_completed=has_completed, is_first_time=is_first_time)

    @app.route('/save_quiz_progress', methods=['POST'])
    def save_quiz_progress():
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not logged in'})
        
        data = request.get_json()
        user_id = get_user_id_from_session()
        
        # Save progress to database
        from database import save_quiz_progress as db_save_quiz_progress
        db_save_quiz_progress(user_id, data.get('answers', []), data.get('currentQuestion', 0))
        
        return jsonify({'success': True})

    @app.route('/get_quiz_progress')
    def get_quiz_progress():
        if 'user_id' not in session:
            return jsonify({'progress': None})
        
        user_id = get_user_id_from_session()
        from database import get_quiz_progress as db_get_quiz_progress
        progress = db_get_quiz_progress(user_id)
        
        if progress:
            return jsonify({'progress': progress})
        
        return jsonify({'progress': None})

    @app.route('/clear_quiz_progress', methods=['POST'])
    def clear_quiz_progress():
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not logged in'})
        
        user_id = get_user_id_from_session()
        from database import clear_quiz_progress as db_clear_quiz_progress
        db_clear_quiz_progress(user_id)
        
        return jsonify({'success': True})

    @app.route('/results')
    def results():
        # Check if user is logged in
        if 'user_id' not in session:
            return redirect(url_for('auth'))
        
        # Check if this is first-time login
        user_id = get_user_id_from_session()
        is_first_time = not has_completed_quiz(user_id)
        
        if is_first_time:
            # First-time users shouldn't access results yet
            return redirect(url_for('quiz'))
        
        results_data = get_quiz_results(user_id)
        recommendations = []
        if results_data:
            recommendations = [career[0] for career in results_data.get('careers', [])]
        
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
            save_quiz_results(user_id, top_careers, answers)
        
        return jsonify({'careers': top_careers})
