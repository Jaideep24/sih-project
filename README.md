# 🧠 Soulence - Student Mental Health Platform

> **Smart India Hackathon 2025 Project**  
> **Team:** AuxiliumAI  
> **Live Website:** [https://auxiliumai.pythonanywhere.com](https://auxiliumai.pythonanywhere.com)

---

## 📖 About the Project

Soulence is a comprehensive digital platform designed to support student mental health and well-being. Developed during the Smart India Hackathon 2024, this platform addresses the growing mental health challenges faced by students in educational institutions by providing peer support, professional counseling, and wellness tracking tools.

Our platform creates a safe, supportive environment where students can:
- Connect with peers through moderated chat rooms
- Schedule appointments with counselors
- Track their mood and mental wellness journey
- Access mental health resources and support

## 👥 Team AuxiliumAI

**Team Leader:** [Amishi Verma](https://github.com/amishiverma)

**Team Members:**
- [Ishani Taishete](https://github.com/ishanitaishete)
- [Aryan Upadhyay](https://github.com/UsaaryanByte07)
- [Vishva Desai](https://github.com/vishva-desai)
- [Paawan Dabhi](https://github.com/PaawanDabhi333)
- [Jaideep Singh](https://github.com/Jaideep24)

---

## ✨ Features

### 🎯 Core Features
- **Student Dashboard** - Personalized wellness tracking and overview
- **Peer Chat Rooms** - Real-time group conversations with moderation
- **Chat History** - View past conversations from completed chat rooms
- **Counselor Booking** - Schedule and manage appointments with mental health professionals
- **Mood Tracking** - Daily mood logging with visual analytics
- **Wellness Hub** - Mental health resources and self-help tools
- **Supervisor Dashboard** - Administrative tools for counselors and supervisors

### 🔒 Security & Privacy
- Secure user authentication and session management
- Role-based access control (Students, Counselors, Supervisors)
- Privacy-focused chat system with moderated environments
- Secure data handling for sensitive mental health information

---

## 🛠️ Tech Stack

### Backend
<div align="left">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/>
</div>

### Frontend
<div align="left">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3"/>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript"/>
  <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap"/>
</div>

### Real-time Communication
<div align="left">
  <img src="https://img.shields.io/badge/Stream_Chat-005FFF?style=for-the-badge&logo=stream&logoColor=white" alt="Stream Chat"/>
</div>

### Deployment
<div align="left">
  <img src="https://img.shields.io/badge/PythonAnywhere-1D9FD7?style=for-the-badge&logo=pythonanywhere&logoColor=white" alt="PythonAnywhere"/>
</div>

### Development Tools
<div align="left">
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git"/>
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  <img src="https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white" alt="VS Code"/>
</div>

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Jaideep24/sih-project.git
   cd sih-project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example settings file
   cp sih_prototype/settings.example.py sih_prototype/settings.py
   
   # Edit settings.py with your configuration
   # Add your Stream Chat API credentials and other settings
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000`
   - Create an account or login to explore the features

---

## 📱 How to Use

### For Students
1. **Sign Up/Login** - Create your student account
2. **Complete Profile** - Add your institution and personal details
3. **Explore Dashboard** - View your wellness overview and quick actions
4. **Join Chat Rooms** - Connect with peers in topic-based discussions
5. **Book Appointments** - Schedule sessions with available counselors
6. **Track Mood** - Log daily mood entries and view your progress
7. **Access Resources** - Explore wellness tools and mental health resources

### For Counselors
1. **Login** - Access your counselor dashboard
2. **Manage Slots** - Set availability for student appointments
3. **View Appointments** - Review scheduled sessions with students
4. **Monitor Students** - Access student wellness data (with permissions)

### For Supervisors
1. **Admin Dashboard** - Overview of platform usage and statistics
2. **Student Management** - View and manage student accounts
3. **Counselor Oversight** - Monitor counselor activities and appointments
4. **Platform Analytics** - Access usage statistics and insights

---

## 🌟 Key Highlights

- **Real-time Chat System** - Powered by Stream Chat API for seamless communication
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile devices
- **Privacy-First Approach** - Secure handling of sensitive mental health data
- **Scalable Architecture** - Built with Django for easy scaling and maintenance
- **User-Friendly Interface** - Intuitive design focused on user experience
- **Comprehensive Features** - All-in-one platform for student mental health support

---

## 📊 Project Structure

```
sih-project/
├── sih_app/                    # Main Django application
│   ├── models.py              # Database models
│   ├── views.py               # View controllers
│   ├── urls.py                # URL routing
│   ├── forms.py               # Django forms
│   ├── templates/             # HTML templates
│   ├── templatetags/          # Custom template tags
│   └── migrations/            # Database migrations
├── sih_prototype/             # Django project settings
│   ├── settings.example.py    # Settings template
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI configuration
├── static/                    # Static files (CSS, JS, images)
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## 🤝 Contributing

While this was our hackathon project, we welcome contributions and suggestions! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project was developed for the Smart India Hackathon 2025. Feel free to use this code for educational and non-commercial purposes.

---

## 🙏 Acknowledgments

- **Smart India Hackathon 2024** - For providing the platform to showcase our solution
- **Stream Chat** - For their excellent real-time messaging API
- **Django Community** - For the robust web framework
- **PythonAnywhere** - For reliable hosting services
- **Our Mentors and Judges** - For their valuable feedback and guidance

---

## 📞 Contact

For any questions or inquiries about this project, feel free to reach out to any of our team members through their GitHub profiles.

**Live Demo:** [https://auxiliumai.pythonanywhere.com](https://auxiliumai.pythonanywhere.com)

---

<div align="center">
  <h3>💙 Built with care for student mental health and well-being 💙</h3>
  <p><strong>Team AuxiliumAI - Smart India Hackathon 2025</strong></p>
</div>
