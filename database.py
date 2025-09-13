import sqlite3
import json
import hashlib
from datetime import datetime

DATABASE_FILE = 'careerguide.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create quiz_progress table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            answers TEXT NOT NULL,
            current_question INTEGER NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id)
        )
    ''')
    
    # Create quiz_results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            careers TEXT NOT NULL,
            answers TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def generate_user_id(email):
    """Generate a unique user ID based on email"""
    return hashlib.md5(email.encode()).hexdigest()[:12]

# User functions
def create_user(name, email, password):
    """Create a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # User already exists
    finally:
        conn.close()

def get_user_by_email(email):
    """Get user by email"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    return dict(user) if user else None

def authenticate_user(email, password):
    """Authenticate user login"""
    user = get_user_by_email(email)
    if user and user['password'] == password:
        return user
    return None

# Quiz progress functions
def save_quiz_progress(user_id, answers, current_question):
    """Save quiz progress"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    answers_json = json.dumps(answers)
    
    cursor.execute('''
        INSERT OR REPLACE INTO quiz_progress (user_id, answers, current_question)
        VALUES (?, ?, ?)
    ''', (user_id, answers_json, current_question))
    
    conn.commit()
    conn.close()

def get_quiz_progress(user_id):
    """Get quiz progress"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM quiz_progress WHERE user_id = ?', (user_id,))
    progress = cursor.fetchone()
    conn.close()
    
    if progress:
        return {
            'answers': json.loads(progress['answers']),
            'current_question': progress['current_question']
        }
    return None

def clear_quiz_progress(user_id):
    """Clear quiz progress and results"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM quiz_progress WHERE user_id = ?', (user_id,))
    cursor.execute('DELETE FROM quiz_results WHERE user_id = ?', (user_id,))
    
    conn.commit()
    conn.close()

# Quiz results functions
def save_quiz_results(user_id, careers, answers):
    """Save quiz results"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    careers_json = json.dumps(careers)
    answers_json = json.dumps(answers)
    
    cursor.execute('''
        INSERT OR REPLACE INTO quiz_results (user_id, careers, answers)
        VALUES (?, ?, ?)
    ''', (user_id, careers_json, answers_json))
    
    conn.commit()
    conn.close()

def get_quiz_results(user_id):
    """Get quiz results"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM quiz_results WHERE user_id = ?', (user_id,))
    results = cursor.fetchone()
    conn.close()
    
    if results:
        return {
            'careers': json.loads(results['careers']),
            'answers': json.loads(results['answers'])
        }
    return None

def has_completed_quiz(user_id):
    """Check if user has completed quiz"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM quiz_results WHERE user_id = ?', (user_id,))
    count = cursor.fetchone()['count']
    conn.close()
    
    return count > 0
