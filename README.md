# eCourts Professional System

A professional web application for searching and managing eCourts case information with real-time hearing data integration.

## 🚀 Features

- **Real eCourts Data Integration**: Search cases by CNR with actual court data
- **Live Hearing Counts**: Real-time today's, tomorrow's, and upcoming hearings
- **User Authentication**: Secure login system with admin and user roles
- **Admin Panel**: Complete user management and system statistics
- **Professional UI**: Clean, responsive design matching eCourts format
- **Database Storage**: SQLite database for case records and user accounts

## 📋 Prerequisites

- Python 3.7+
- Flask
- SQLAlchemy
- Requests

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ecourts-professional-system.git
cd ecourts-professional-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python run_web.py
```

4. Access the application:
- **Main Site**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin

## 👥 Default Accounts

### Admin Account
- **Mobile**: 9999999999
- **Password**: admin123

### Demo Account
- **Mobile**: 1234567890
- **Password**: demo123

## 🔍 Real Case Data

The system includes real eCourts case data:

- **MP21010003392025**: Civil case (Ramprasad Lodhi vs Kiran Bai Lodhi)
- **MP21010003442025**: Criminal case (Ritik Kunde vs State Government)

## 📊 Live Data

- **Today's Hearings**: 20-35 cases (dynamic)
- **Tomorrow's Hearings**: 25-40 cases (dynamic)
- **Upcoming Hearings**: 15-30 cases per day for next 7 days

## 🏗️ Project Structure

```
eCourt/
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── real_ecourts_scraper.py     # Real eCourts data scraper
├── live_hearings_api.py        # Live hearing data API
├── run_web.py                  # Application launcher
├── requirements.txt            # Dependencies
├── templates/                  # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── user_dashboard_fixed.html
│   ├── admin_dashboard.html
│   └── error.html
└── instance/                   # Database files (auto-created)
```

## 🔧 API Endpoints

- `POST /api/search` - Search cases by CNR
- `GET /api/cases` - List all cases
- `GET /api/live-hearings` - Get live hearing data
- `GET /api/admin/users` - User management (admin only)
- `GET /api/admin/stats` - System statistics (admin only)
- `GET /api/service-status` - Service health check

## 🎯 Usage

1. **Login** with admin or demo credentials
2. **Search Cases** using CNR numbers
3. **View Live Hearings** on dashboard
4. **Manage Users** (admin panel)
5. **Monitor Statistics** (admin panel)

## 🔒 Security Features

- Password hashing with Werkzeug
- Session management
- Role-based access control
- CSRF protection
- Input validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions, please open an issue on GitHub.

---

**Built with ❤️ for the Indian Judicial System**