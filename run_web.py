#!/usr/bin/env python3
"""
Quick launcher for the eCourts Professional System with Authentication
"""

import os
import sys
from app import app, init_database

if __name__ == '__main__':
    print("Starting eCourts Professional System...")
    print("=" * 50)
    print("Access the web interface at: http://localhost:5000")
    print("")
    print("Default Login Credentials:")
    print("Admin: Mobile: 9999999999, Password: admin123")
    print("Demo User: Mobile: 1234567890, Password: demo123")
    print("")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Ensure directories exist
    os.makedirs('results', exist_ok=True)
    os.makedirs('downloads', exist_ok=True)
    
    try:
        # Initialize database
        init_database()
        
        # Start the app on port 5000 instead of 5001
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)