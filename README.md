# Career Guidance Application (SIH_CG)

A comprehensive career guidance web application built with Flask that helps students discover their ideal career paths through interactive quizzes and provides information about top colleges and universities.

## 🚀 Features

### Core Functionality
- **User Authentication**: Secure login and registration system
- **Career Quiz**: Interactive aptitude test with 10 questions
- **Results Analysis**: AI-powered career recommendations based on quiz responses
- **College Database**: Comprehensive information about top Indian colleges
- **Remember Me**: Persistent login functionality
- **Progress Saving**: Automatic quiz progress saving

### User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Clean, professional interface with smooth animations
- **Keyboard Navigation**: Full keyboard support for accessibility
- **Auto-Login**: Seamless user experience with persistent sessions
- **Real-time Feedback**: Toast notifications and progress indicators

### Technical Features
- **API-Driven**: RESTful API for college data
- **Dynamic Content**: JavaScript-powered dynamic content loading
- **Session Management**: Secure user session handling
- **Data Persistence**: File-based data storage with JSON
- **Error Handling**: Comprehensive error handling and user feedback

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with CSS Variables
- **Data Storage**: JSON files
- **Session Management**: Flask Sessions
- **API**: RESTful API endpoints

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/rabel798/SIH_CG.git
cd SIH_CG
```

### 2. Create Virtual Environment
```bash
python -m venv sihvenv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
sihvenv\Scripts\activate
```

**macOS/Linux:**
```bash
source sihvenv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
python app.py
```

### 6. Access the Application
Open your browser and navigate to: `http://localhost:5000`

## 📁 Project Structure

```
SIH_CG/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Data models and business logic
├── routes.py             # API routes and endpoints
├── requirements.txt      # Python dependencies
├── colleges_data.json    # College database
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Homepage
│   ├── auth.html        # Login/Register page
│   ├── quiz.html        # Career quiz
│   ├── results.html     # Quiz results
│   └── colleges.html    # Colleges page
├── static/              # Static assets (if any)
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## 🎯 Usage Guide

### For Students
1. **Register/Login**: Create an account or login with existing credentials
2. **Take Quiz**: Complete the 10-question career aptitude test
3. **View Results**: Get personalized career recommendations
4. **Explore Colleges**: Browse top colleges and universities
5. **Visit Websites**: Access official college websites directly

### For Developers
1. **API Endpoints**: Use `/api/colleges` to fetch college data
2. **Data Models**: Extend `models.py` for additional functionality
3. **Templates**: Modify HTML templates in `templates/` directory
4. **Styling**: Update CSS in `templates/base.html`

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Homepage |
| `/auth` | GET | Login/Register page |
| `/login` | POST | User login |
| `/register` | POST | User registration |
| `/quiz` | GET | Career quiz page |
| `/save_quiz_progress` | POST | Save quiz progress |
| `/get_quiz_progress` | GET | Get saved progress |
| `/calculate_results` | POST | Calculate career results |
| `/results` | GET | Display results |
| `/colleges` | GET | Colleges page |
| `/api/colleges` | GET | College data API |

## 🎨 Customization

### Adding New Colleges
Edit `colleges_data.json` to add new colleges:
```json
{
  "id": 9,
  "name": "College Name",
  "description": "College description",
  "details": "Detailed information",
  "popular_courses": ["Course1", "Course2"],
  "entrance_exam": "Exam Name",
  "website": "https://college-website.com",
  "category": "Category"
}
```

### Modifying Quiz Questions
Update the `questions` array in `models.py`:
```python
questions = [
    {"id": 1, "question": "Your question here?", "category": "category"},
    # Add more questions...
]
```

### Styling Changes
Modify CSS variables in `templates/base.html`:
```css
:root {
    --primary: #your-color;
    --accent: #your-accent-color;
    /* Other variables... */
}
```

## 🔒 Security Features

- **Session Management**: Secure user sessions
- **Input Validation**: Form validation and sanitization
- **Error Handling**: Comprehensive error handling
- **Data Protection**: Secure data storage and retrieval

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set `DEBUG = False` in `config.py`
2. Use a production WSGI server like Gunicorn
3. Set up proper environment variables
4. Configure reverse proxy (nginx)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Rahul** - *Initial work* - [rabel798](https://github.com/rabel798)

## 🙏 Acknowledgments

- Flask community for excellent documentation
- All contributors who helped improve this project
- Students who provided feedback and suggestions

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Contact the maintainer
- Check the documentation

---

**Made with ❤️ for students seeking career guidance**