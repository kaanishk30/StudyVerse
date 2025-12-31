#!/usr/bin/env python3
"""
Database Migration Script for AI Scheduler
Migrates old schedule table to new structure with AI features
"""

import sqlite3
from datetime import datetime

def migrate_scheduler_database():
    """Migrate database to support AI scheduler features"""
    
    print("🔄 Starting database migration for AI Scheduler...")
    
    conn = sqlite3.connect('studypal.db')
    c = conn.cursor()
    
    # Check if old schedules table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schedules'")
    table_exists = c.fetchone()
    
    if table_exists:
        # Get existing columns
        c.execute("PRAGMA table_info(schedules)")
        columns = [col[1] for col in c.fetchall()]
        
        # Check if we need to migrate
        if 'day_of_week' in columns and 'scheduled_date' not in columns:
            print("  📋 Old schedule structure detected, migrating...")
            
            # Rename old table
            c.execute("ALTER TABLE schedules RENAME TO schedules_old")
            
            # Create new table with updated structure
            c.execute('''
                CREATE TABLE schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    subject TEXT NOT NULL,
                    unit_name TEXT,
                    topic_name TEXT NOT NULL,
                    difficulty TEXT DEFAULT 'medium',
                    estimated_hours INTEGER DEFAULT 2,
                    scheduled_date DATE NOT NULL,
                    start_time TEXT,
                    end_time TEXT,
                    status TEXT DEFAULT 'pending',
                    completion_percentage INTEGER DEFAULT 0,
                    notes TEXT,
                    is_auto_generated INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Migrate old data if any exists
            c.execute("SELECT COUNT(*) FROM schedules_old")
            old_count = c.fetchone()[0]
            
            if old_count > 0:
                print(f"  📦 Migrating {old_count} existing schedules...")
                
                # Map day_of_week to actual dates (next occurrence)
                c.execute('''
                    INSERT INTO schedules 
                    (user_id, subject, topic_name, scheduled_date, start_time, end_time, notes, status)
                    SELECT 
                        user_id,
                        subject,
                        subject as topic_name,
                        date('now', '+' || 
                            CASE day_of_week
                                WHEN 'Monday' THEN 0
                                WHEN 'Tuesday' THEN 1
                                WHEN 'Wednesday' THEN 2
                                WHEN 'Thursday' THEN 3
                                WHEN 'Friday' THEN 4
                                WHEN 'Saturday' THEN 5
                                WHEN 'Sunday' THEN 6
                            END || ' days'),
                        start_time,
                        end_time,
                        notes,
                        CASE WHEN completed = 1 THEN 'completed' ELSE 'pending' END
                    FROM schedules_old
                ''')
                
                print(f"  ✅ Migrated {old_count} schedules")
            
            # Drop old table
            c.execute("DROP TABLE schedules_old")
            print("  🗑️  Removed old table")
        
        elif 'scheduled_date' in columns:
            print("  ✅ Database already using new structure")
        else:
            print("  ⚠️  Unknown table structure, creating new table...")
            c.execute("DROP TABLE schedules")
            create_new_table(c)
    else:
        print("  📝 Creating new schedules table...")
        create_new_table(c)
    
    conn.commit()
    conn.close()
    
    print("✅ Database migration completed successfully!\n")

def create_new_table(cursor):
    """Create new schedules table with AI features"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT NOT NULL,
            unit_name TEXT,
            topic_name TEXT NOT NULL,
            difficulty TEXT DEFAULT 'medium',
            estimated_hours INTEGER DEFAULT 2,
            scheduled_date DATE NOT NULL,
            start_time TEXT,
            end_time TEXT,
            status TEXT DEFAULT 'pending',
            completion_percentage INTEGER DEFAULT 0,
            notes TEXT,
            is_auto_generated INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

if __name__ == '__main__':
    migrate_scheduler_database()
    print("🎉 Migration complete! You can now use the AI Scheduler.")
