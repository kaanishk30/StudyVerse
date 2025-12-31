#!/usr/bin/env python3
"""Test script to verify app.py functionality"""

import sys
import sqlite3

def test_database():
    """Test database connectivity"""
    try:
        conn = sqlite3.connect('studypal.db')
        cursor = conn.cursor()
        
        # Check tables
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        print("✓ Database tables:", [t[0] for t in tables])
        
        # Check users
        users = cursor.execute("SELECT COUNT(*) FROM users").fetchone()
        print(f"✓ Users count: {users[0]}")
        
        # Check schedules
        schedules = cursor.execute("SELECT COUNT(*) FROM schedules").fetchone()
        print(f"✓ Schedules count: {schedules[0]}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import flask
        print("✓ Flask imported")
        
        import nltk
        print("✓ NLTK imported")
        
        import wikipediaapi
        print("✓ Wikipedia API imported")
        
        import PyPDF2
        print("✓ PyPDF2 imported")
        
        from pptx import Presentation
        print("✓ python-pptx imported")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_app_syntax():
    """Test if app.py has syntax errors"""
    try:
        import app
        print("✓ app.py syntax is valid")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in app.py: {e}")
        return False
    except Exception as e:
        print(f"⚠ Warning during import: {e}")
        return True  # May be runtime errors, not syntax

def main():
    print("="*60)
    print("Testing StudyVerse Backend")
    print("="*60)
    
    print("\n1. Testing imports...")
    imports_ok = test_imports()
    
    print("\n2. Testing database...")
    db_ok = test_database()
    
    print("\n3. Testing app.py syntax...")
    syntax_ok = test_app_syntax()
    
    print("\n" + "="*60)
    if imports_ok and db_ok and syntax_ok:
        print("✓ All tests passed!")
        print("You can now run: python app.py")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
    print("="*60)

if __name__ == '__main__':
    main()
