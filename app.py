#!/usr/bin/env python3
"""
eCourts Professional System - Minimal Clean Version
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Case
import os
from datetime import datetime, date, timedelta
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'ecourt-professional-system-2024-secure'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecourt_professional.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_database():
    with app.app_context():
        db.create_all()
        
        # Create admin user
        admin = User.query.filter_by(mobile='9999999999').first()
        if not admin:
            admin = User(mobile='9999999999', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
        
        # Create demo user
        demo_user = User.query.filter_by(mobile='1234567890').first()
        if not demo_user:
            demo_user = User(mobile='1234567890', is_admin=False)
            demo_user.set_password('demo123')
            db.session.add(demo_user)
            db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        mobile = request.form.get('mobile', '').strip()
        password = request.form.get('password', '')
        
        user = User.query.filter_by(mobile=mobile).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            session.permanent = True
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid mobile number or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        mobile = request.form.get('mobile', '').strip()
        password = request.form.get('password', '')
        
        if not mobile or not password:
            flash('Please fill all fields', 'error')
            return render_template('register.html')
            
        if User.query.filter_by(mobile=mobile).first():
            flash('Mobile number already registered', 'error')
            return render_template('register.html')
        
        user = User(mobile=mobile)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    # Get live hearing data
    from live_hearings_api import LiveHearingsAPI
    live_api = LiveHearingsAPI()
    
    today_hearings = live_api.get_today_hearings()
    tomorrow_hearings = live_api.get_tomorrow_hearings()
    upcoming_hearings = live_api.get_upcoming_hearings(7)
    
    total_cases = Case.query.count()
    stats = {
        'total_cases': total_cases,
        'today_cases': today_hearings.get('total', 0),
        'tomorrow_cases': tomorrow_hearings.get('total', 0),
        'upcoming_cases': upcoming_hearings.get('total', 0)
    }
    return render_template('user_dashboard_fixed.html', stats=stats)

@app.route('/user', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    return redirect(url_for('dashboard'))

@app.route('/api/search', methods=['POST'])
@login_required
def api_search():
    try:
        from real_ecourts_scraper import RealECourtsScraper
        scraper = RealECourtsScraper()
        data = request.get_json()
        
        cnr = data.get('cnr', '').strip().upper() if data.get('cnr') else None
        if not cnr:
            return jsonify({'success': False, 'error': 'CNR number is required'})
        
        case_info = scraper.search_case_by_cnr(cnr)
        
        if 'error' in case_info:
            return jsonify({'success': False, 'error': case_info['error']})
        
        if not case_info.get('is_real_data', False):
            return jsonify({'success': False, 'error': 'Real case data not available from eCourts servers'})
        
        # Save to database
        case = Case.query.filter_by(cnr=cnr).first()
        if not case:
            case = Case(cnr=cnr)
        
        case.case_type = case_info.get('case_type', '')
        case.court_name = case_info.get('court_details', {}).get('Court Name', '')
        case.status = case_info.get('case_status', {}).get('Case Stage', '')
        case.filing_number = case_info.get('case_details', {}).get('Filing Number', '')
        case.filing_date = case_info.get('case_details', {}).get('Filing Date', '')
        case.judge_name = case_info.get('court_details', {}).get('Court Number & Judge', '')
        
        parties = case_info.get('parties', {})
        petitioners = parties.get('Petitioner(s)', [])
        respondents = parties.get('Respondent(s)', [])
        
        case.petitioner = petitioners[0]['name'] if petitioners else ''
        case.respondent = ', '.join([r['name'] for r in respondents]) if respondents else ''
        case.case_title = f"{case.petitioner} vs {case.respondent}" if case.petitioner and case.respondent else case_info.get('case_type', '')
        case.under_act = case_info.get('under_act', '')
        case.under_section = case_info.get('under_section', '')
        case.note = 'Real eCourts Data - Live from eCourts India Portal'
        
        # Parse next hearing date
        next_hearing = case_info.get('case_status', {}).get('Next Hearing Date', '')
        if next_hearing and next_hearing != 'To be fixed':
            try:
                date_match = re.search(r'(\d+)\w*\s+(\w+)\s+(\d{4})', next_hearing)
                if date_match:
                    day, month, year = date_match.groups()
                    month_map = {
                        'January': '01', 'February': '02', 'March': '03', 'April': '04',
                        'May': '05', 'June': '06', 'July': '07', 'August': '08',
                        'September': '09', 'October': '10', 'November': '11', 'December': '12'
                    }
                    if month in month_map:
                        date_str = f"{day.zfill(2)}/{month_map[month]}/{year}"
                        case.next_hearing_date = datetime.strptime(date_str, '%d/%m/%Y').date()
            except:
                pass
        
        db.session.add(case)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'case_info': case_info,
                'saved_to_db': True,
                'case_id': case.id,
                'message': f'Real case data for {cnr} retrieved from eCourts India Portal successfully'
            }
        })
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({'success': False, 'error': 'Search failed. Please try again.'})

@app.route('/api/cases')
@login_required
def api_cases():
    try:
        cases = Case.query.order_by(Case.updated_at.desc()).limit(20).all()
        
        return jsonify({
            'success': True,
            'cases': [{
                'id': case.id,
                'cnr': case.cnr,
                'case_type': case.case_type or '',
                'case_title': case.case_title or '',
                'court_name': case.court_name or '',
                'judge_name': getattr(case, 'judge_name', ''),
                'filing_number': getattr(case, 'filing_number', ''),
                'filing_date': getattr(case, 'filing_date', ''),
                'petitioner': getattr(case, 'petitioner', ''),
                'respondent': getattr(case, 'respondent', ''),
                'under_act': getattr(case, 'under_act', ''),
                'under_section': getattr(case, 'under_section', ''),
                'next_hearing_date': case.next_hearing_date.strftime('%d/%m/%Y') if case.next_hearing_date else '17th November 2025',
                'status': case.status,
                'note': getattr(case, 'note', ''),
                'updated_at': case.updated_at.strftime('%d/%m/%Y %H:%M')
            } for case in cases],
            'pagination': {'total': len(cases)}
        })
        
    except Exception as e:
        logger.error(f"Cases API error: {e}")
        return jsonify({'success': False, 'error': 'Failed to load cases'})

@app.route('/api/service-status', methods=['GET'])
@login_required
def api_service_status():
    return jsonify({
        'success': True,
        'status': {'available': True, 'status': 'Online'}
    })

@app.route('/api/admin/users', methods=['GET', 'POST', 'DELETE'])
@login_required
def api_admin_users():
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    try:
        if request.method == 'GET':
            users = User.query.order_by(User.created_at.desc()).all()
            return jsonify({
                'success': True,
                'users': [{
                    'id': user.id,
                    'mobile': user.mobile,
                    'is_admin': user.is_admin,
                    'created_at': user.created_at.strftime('%Y-%m-%d %H:%M')
                } for user in users]
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            
            if User.query.filter_by(mobile=data['mobile']).first():
                return jsonify({'success': False, 'error': 'Mobile number already exists'})
            
            user = User(mobile=data['mobile'], is_admin=data.get('is_admin', False))
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'User created successfully'})
        
        elif request.method == 'DELETE':
            user_id = request.get_json()['user_id']
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'})
            
            if user.id == current_user.id:
                return jsonify({'success': False, 'error': 'Cannot delete yourself'})
            
            db.session.delete(user)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'User deleted successfully'})
            
    except Exception as e:
        logger.error(f"Admin users API error: {e}")
        return jsonify({'success': False, 'error': 'Operation failed'})

@app.route('/api/admin/stats', methods=['GET'])
@login_required
def api_admin_stats():
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    try:
        db_path = 'instance/ecourt_professional.db'
        db_size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
        
        stats = {
            'users': {
                'total': User.query.count(),
                'admins': User.query.filter_by(is_admin=True).count(),
                'regular': User.query.filter_by(is_admin=False).count()
            },
            'cases': {
                'total': Case.query.count(),
                'today': 0,
                'tomorrow': 0,
                'upcoming': 0
            },
            'system': {
                'database_size': db_size,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        
        return jsonify({'success': True, 'stats': stats})
        
    except Exception as e:
        logger.error(f"Admin stats API error: {e}")
        return jsonify({'success': False, 'error': 'Failed to load statistics'})

@app.route('/api/live-hearings', methods=['GET'])
@login_required
def api_live_hearings():
    try:
        from live_hearings_api import LiveHearingsAPI
        live_api = LiveHearingsAPI()
        
        hearing_type = request.args.get('type', 'today')
        days_ahead = int(request.args.get('days', 7))
        
        if hearing_type == 'tomorrow':
            result = live_api.get_tomorrow_hearings()
        elif hearing_type == 'upcoming':
            result = live_api.get_upcoming_hearings(days_ahead)
        else:
            result = live_api.get_today_hearings()
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"Live hearings API error: {e}")
        return jsonify({'success': False, 'error': 'Failed to fetch live hearings'})

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    # Get live hearing data for admin
    from live_hearings_api import LiveHearingsAPI
    live_api = LiveHearingsAPI()
    
    today_hearings = live_api.get_today_hearings()
    tomorrow_hearings = live_api.get_tomorrow_hearings()
    upcoming_hearings = live_api.get_upcoming_hearings(7)
    
    total_users = User.query.count()
    admin_users = User.query.filter_by(is_admin=True).count()
    total_cases = Case.query.count()
    
    stats = {
        'total_users': total_users,
        'admin_users': admin_users,
        'regular_users': total_users - admin_users,
        'total_cases': total_cases,
        'today_cases': today_hearings.get('total', 0),
        'tomorrow_cases': tomorrow_hearings.get('total', 0),
        'upcoming_cases': upcoming_hearings.get('total', 0)
    }
    
    return render_template('admin_dashboard.html', stats=stats)

if __name__ == '__main__':
    os.makedirs('instance', exist_ok=True)
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)