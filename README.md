# eCourts Professional System with Delhi Courts Real-Time Scraper

A professional web application for searching eCourts case information and downloading real-time cause lists from Delhi Courts with bulk PDF generation.

## 🚀 Key Features

### ✅ **Delhi Courts Real-Time Cause List Scraper**
- **Live Data Scraping**: Real-time data from Delhi Courts official website
- **Bulk PDF Download**: Download cause lists for ALL judges in a court complex
- **Separate PDFs**: Individual PDF file for each judge
- **Any Date Selection**: User can select any date for cause list
- **One-Click Download**: Bulk download all judges' cause lists instantly

### ✅ **eCourts Professional System**
- **Real eCourts Data Integration**: Search cases by CNR with actual court data
- **User Authentication**: Secure login system with admin and user roles
- **Admin Panel**: Complete user management and system statistics
- **Professional UI**: Clean, responsive design matching eCourts format
- **Database Storage**: SQLite database for case records and user accounts

## 📋 Prerequisites

- Python 3.7+
- Flask
- BeautifulSoup4
- ReportLab
- Requests

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/sammed979/ecourts-professional-system.git
cd ecourts-professional-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Access the application:
- **Main Site**: http://localhost:5000
- **Delhi Courts Scraper**: http://localhost:5000/delhi-courts
- **Admin Panel**: http://localhost:5000/admin

## 👥 Default Accounts

### Admin Account
- **Mobile**: 9999999999
- **Password**: admin123

### Demo Account
- **Mobile**: 1234567890
- **Password**: demo123

## 🏛️ Delhi Courts Scraper Usage

1. **Login** to the system
2. **Click** "Delhi Courts - REAL Data" from dashboard
3. **Select** Delhi Court Complex
4. **Choose** date for cause list
5. **Click** "FETCH ALL JUDGES CAUSE LISTS"
6. **Download** individual PDFs for each judge

## 🏗️ Project Structure

```
eCourt/
├── app.py                          # Main Flask application
├── models.py                       # Database models
├── delhi_courts_scraper.py         # Real Delhi Courts scraper
├── real_ecourts_scraper.py         # eCourts case search
├── live_hearings_api.py            # Live hearing data API
├── requirements.txt                # Dependencies
├── templates/
│   ├── login.html                  # Login page
│   ├── register.html               # Registration page
│   ├── user_dashboard_fixed.html   # Main dashboard
│   ├── admin_dashboard.html        # Admin panel
│   └── delhi_causelist.html        # Delhi Courts scraper UI
└── instance/                       # Database files (auto-created)
```

## 🔧 API Endpoints

### eCourts System
- `POST /api/search` - Search cases by CNR
- `GET /api/cases` - List all cases
- `GET /api/live-hearings` - Get live hearing data
- `GET /api/admin/users` - User management (admin only)
- `GET /api/admin/stats` - System statistics (admin only)

### Delhi Courts Scraper
- `GET /api/delhi-courts/complexes` - Get court complexes
- `POST /api/delhi-courts/download` - Generate cause list PDFs
- `GET /api/delhi-courts/download-file` - Download PDF file

## 🎯 Boss Requirements Fulfilled

✅ **Real-time UI**: Live dropdowns for court selection  
✅ **PDF Download**: Generate PDFs for user-selected date  
✅ **From our UI**: Integrated in existing system  
✅ **Bulk Download**: All judges in court complex  
✅ **Real-time Data**: No stored data, fresh scraping  
✅ **Separate PDFs**: Individual file per judge  

## 🔒 Security Features

- Password hashing with Werkzeug
- Session management
- Role-based access control
- Input validation
- Secure file handling

## 📊 Technical Features

- **Web Scraping**: BeautifulSoup4 for real-time data extraction
- **PDF Generation**: ReportLab for professional PDF formatting
- **Responsive Design**: Mobile-friendly interface
- **Error Handling**: Comprehensive error management
- **Progress Indicators**: Real-time feedback during processing

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

**🏛️ Built for the Indian Judicial System with Real Delhi Courts Integration**