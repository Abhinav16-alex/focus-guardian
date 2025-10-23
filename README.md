# focus-guardian
A desktop app that lets you block distracting websites for set periods (Pomodoro style) and shows your focus stats. Why it's impressive: Combines UI, system control, and data visualization.
# 🛡️ FocusGuard - Distraction-Blocking Productivity App

> A full-stack productivity application that helps you stay focused by blocking distracting websites during work sessions. Built with Python Flask backend and React frontend.

---

## 🎯 Problem Statement

In today's digital world, it's incredibly easy to get distracted by social media, news sites, and entertainment platforms while trying to work or study. **FocusGuard** solves this problem by:

- ✅ Blocking distracting websites during focus sessions
- ✅ Implementing Pomodoro-style timers for structured work
- ✅ Tracking productivity statistics and streaks
- ✅ Providing visual analytics to monitor focus habits

---

## ✨ Features

### 🎯 Core Features

1. **Smart Focus Timer**
   - Pomodoro mode (25 minutes)
   - Quick focus (15 minutes)
   - Deep work mode (90 minutes)
   - Real-time countdown with progress visualization

2. **Website Blocking**
   - Blocks websites at system level (hosts file)
   - Preset categories (Social Media, News, Entertainment)
   - Custom website blocking
   - Automatic enable/disable with timer

3. **Productivity Analytics**
   - Total focus time tracking
   - Session completion statistics
   - Daily/weekly activity charts
   - Focus streaks (current & best)
   - Completion rate percentage

4. **Blocklist Management**
   - Add/remove websites easily
   - Quick-add preset categories
   - View all blocked sites with categories

---

## 🛠️ Tech Stack

### Backend
- **Python 3.9+**
- **Flask 3.0** - Web framework
- **SQLAlchemy** - ORM for database
- **SQLite** - Database
- **Flask-CORS** - Cross-origin resource sharing
- **Threading** - Timer management

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **Lucide React** - Icons

---

## 📦 Installation & Setup

### Prerequisites

- Python 3.9 or higher
- Node.js 16+ and npm
- Admin/sudo privileges (for website blocking)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/focusguard.git
cd focusguard
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Flask backend (with admin privileges)
# On Windows (Run as Administrator):
python run.py

# On Linux/Mac:
sudo python run.py
```

Backend will start at: `http://localhost:5000`

### Step 3: Frontend Setup

Open a **new terminal** and:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will start at: `http://localhost:5173`

---

## 🚀 Usage

1. **Open your browser** and go to `http://localhost:5173`

2. **Add websites to block:**
   - Go to "Blocklist" tab
   - Add individual websites (e.g., `facebook.com`)
   - Or use preset categories for quick setup

3. **Start a focus session:**
   - Go to "Focus Timer" tab
   - Click on a duration (25, 15, or 90 minutes)
   - Websites will be blocked automatically
   - Timer shows countdown and progress

4. **View your statistics:**
   - Go to "Analytics" tab
   - See total focus time, sessions completed
   - Check your current streak
   - View weekly activity chart

---

## 📂 Project Structure

```
focusguard/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── config.py            # Configuration
│   │   ├── models.py            # Database models
│   │   ├── routes.py            # API endpoints
│   │   ├── blocker.py           # Website blocking logic
│   │   ├── timer.py             # Focus timer service
│   │   └── analytics.py         # Analytics calculations
│   ├── requirements.txt
│   └── run.py                   # Main entry point
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Timer.jsx
│   │   │   ├── BlocklistManager.jsx
│   │   │   └── Analytics.jsx
│   │   ├── services/
│   │   │   └── api.js           # API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## 🔧 API Endpoints

### Focus Session Endpoints

- `POST /api/focus/start` - Start focus session
- `POST /api/focus/stop` - Stop focus session
- `GET /api/focus/status` - Get current status

### Blocklist Endpoints

- `GET /api/blocklist` - Get all blocked sites
- `POST /api/blocklist` - Add site to blocklist
- `DELETE /api/blocklist/<id>` - Remove site
- `POST /api/blocklist/preset/<category>` - Add preset category

### Analytics Endpoints

- `GET /api/analytics/overview?days=7` - Get overview stats
- `GET /api/analytics/daily?days=30` - Get daily breakdown
- `GET /api/analytics/streaks` - Get streak information
- `GET /api/analytics/history?limit=50` - Get session history

---

## 💡 How It Works

### Website Blocking Mechanism

FocusGuard uses **hosts file manipulation** to block websites at the system level:

1. When you start a focus session, the app modifies your system's hosts file
2. It redirects blocked domains to `127.0.0.1` (localhost)
3. This prevents your browser from accessing those sites
4. When the session ends, the blocking is automatically removed

**Note:** This requires admin/sudo privileges to modify the hosts file.

---

## 📸 Screenshots

### Focus Timer
![Timer Screenshot](docs/screenshots/timer.png)

### Analytics Dashboard
![Analytics Screenshot](docs/screenshots/analytics.png)

### Blocklist Manager
![Blocklist Screenshot](docs/screenshots/blocklist.png)

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/
```

### Manual Testing

1. Start a 1-minute focus session
2. Try to access a blocked site (should be blocked)
3. Wait for timer to complete
4. Verify sites are unblocked
5. Check analytics for recorded session

---

## 🚨 Important Notes

### Admin Privileges Required

This app **MUST** be run with administrator/sudo privileges to modify the hosts file for website blocking.

### Platform Compatibility

- ✅ Windows (tested)
- ✅ Linux (tested)
- ✅ macOS (tested)

### Browser Compatibility

Works with all major browsers:
- Chrome
- Firefox
- Safari
- Edge

---

## 🔮 Future Enhancements

- [ ] Browser extension version
- [ ] Mobile app (React Native)
- [ ] Cloud sync across devices
- [ ] Whitelist mode (allow only specific sites)
- [ ] Scheduled focus sessions
- [ ] Break reminders
- [ ] Pomodoro cycle automation
- [ ] Export data as CSV/PDF
- [ ] Dark mode
- [ ] Sound notifications

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- Built for Innovation Phase Project
- Python Internship Showcase
- Inspired by Pomodoro Technique
- Icons by Lucide React

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/focusguard/issues) page
2. Create a new issue with detailed information
3. Contact the maintainer

---

**⭐ If you found this project helpful, please give it a star!**
