#!/usr/bin/env python3
"""
Database Migration Script
Run this to update your database with new tables and columns
"""
import sqlite3
import os

def migrate_database():
    """Add missing tables and columns to existing database"""
    
    db_path = 'studypal.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found. Please run app.py first to create it.")
        return
    
    print("🔧 Starting database migration...")
    print("="*60)
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    try:
        # 1. Add schedules table if not exists
        print("\n📅 Checking schedules table...")
        c.execute('''
            CREATE TABLE IF NOT EXISTS schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                subject TEXT NOT NULL,
                day_of_week TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                priority TEXT DEFAULT 'medium',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        print("   ✅ Schedules table ready")
        
        # 2. Add total_questions column to user_stats if missing
        print("\n📊 Checking user_stats columns...")
        try:
            c.execute('ALTER TABLE user_stats ADD COLUMN total_questions INTEGER DEFAULT 0')
            print("   ✅ Added total_questions column")
        except sqlite3.OperationalError:
            print("   ℹ️  total_questions column already exists")
        
        # 3. Add study_duration column to study_history if missing
        print("\n📚 Checking study_history columns...")
        try:
            c.execute('ALTER TABLE study_history ADD COLUMN study_duration INTEGER DEFAULT 0')
            print("   ✅ Added study_duration column")
        except sqlite3.OperationalError:
            print("   ℹ️  study_duration column already exists")
        
        # 4. Verify all tables exist
        print("\n🔍 Verifying all tables...")
        tables = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        table_names = [t[0] for t in tables]
        
        required_tables = ['users', 'user_stats', 'study_history', 'user_achievements', 'schedules']
        for table in required_tables:
            if table in table_names:
                print(f"   ✅ {table}")
            else:
                print(f"   ❌ {table} MISSING!")
        
        # 5. Show user stats
        print("\n👥 Current users:")
        users = c.execute('SELECT id, username, email FROM users').fetchall()
        if users:
            for user in users:
                print(f"   • ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")
        else:
            print("   ℹ️  No users yet")
        
        # 6. Show schedule stats
        print("\n📅 Current schedules:")
        schedule_count = c.execute('SELECT COUNT(*) FROM schedules').fetchone()[0]
        print(f"   Total schedules: {schedule_count}")
        
        conn.commit()
        print("\n" + "="*60)
        print("✅ Database migration completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Migration error: {e}")
        conn.rollback()
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

def verify_database():
    """Verify database structure"""
    conn = sqlite3.connect('studypal.db')
    c = conn.cursor()
    
    print("\n📋 Database Structure:")
    print("="*60)
    
    # Get all tables
    tables = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"\n📊 Table: {table_name}")
        
        # Get columns for this table
        columns = c.execute(f"PRAGMA table_info({table_name})").fetchall()
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, is_pk = col
            nullable = "NOT NULL" if not_null else "NULL"
            pk = "PRIMARY KEY" if is_pk else ""
            print(f"   • {col_name} ({col_type}) {nullable} {pk}")
    
    conn.close()
    print("\n" + "="*60)

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════╗
║   AI Study Pal - Database Migration Tool     ║
╚═══════════════════════════════════════════════╝
    """)
    
    migrate_database()
    
    print("\n📋 Would you like to see the full database structure? (y/n)")
    choice = input("> ").strip().lower()
    
    if choice == 'y':
        verify_database()
    
    print("\n✨ Migration complete! You can now run: python app.py")