#!/usr/bin/env python3
"""
Database models for eCourts scraper
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cnr = db.Column(db.String(50), unique=True, nullable=False)
    case_type = db.Column(db.String(10))
    case_number = db.Column(db.String(20))
    case_year = db.Column(db.String(4))
    case_title = db.Column(db.Text)
    court_name = db.Column(db.String(200))
    next_hearing_date = db.Column(db.Date)
    serial_number = db.Column(db.String(20))
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def is_today(self):
        if self.next_hearing_date:
            return self.next_hearing_date == datetime.now().date()
        return False
    
    @property
    def is_tomorrow(self):
        if self.next_hearing_date:
            from datetime import timedelta
            return self.next_hearing_date == (datetime.now().date() + timedelta(days=1))
        return False

class CauseList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    court_name = db.Column(db.String(200))
    total_cases = db.Column(db.Integer, default=0)
    data = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)