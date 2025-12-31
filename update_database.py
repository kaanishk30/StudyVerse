#!/usr/bin/env python3
"""Update database schema to add quiz_data column"""

import sqlite3

def update_database():
    conn = sqlite3.connect('studypal.db')
    cursor = conn.cursor()
    
    # Check if quiz_data column exists
    cursor.execute("PRAGMA table_info(study_history)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'quiz_data' not in columns:
        print("Adding quiz_data column to study_history table...")
        cursor.execute("ALTER TABLE study_history ADD COLUMN quiz_data TEXT")
        conn.commit()
        print("✓ Column added successfully")
    else:
        print("✓ quiz_data column already exists")
    
    conn.close()
    print("✓ Database update complete")

if __name__ == '__main__':
    update_database()
