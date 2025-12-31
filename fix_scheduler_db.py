import sqlite3

print("🔧 Fixing schedules database...")

conn = sqlite3.connect('studypal.db')
c = conn.cursor()

# Create schedules table if it doesn't exist
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
        completed INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

print("✅ Schedules table ready")

# Add completed column if it doesn't exist (for existing tables)
try:
    c.execute('ALTER TABLE schedules ADD COLUMN completed INTEGER DEFAULT 0')
    print("✅ Added completed column")
except sqlite3.OperationalError:
    print("ℹ️  completed column already exists")

conn.commit()

# Verify table exists
tables = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
table_names = [t[0] for t in tables]

if 'schedules' in table_names:
    print("\n✅ Schedules table verified!")
    
    # Show table structure
    columns = c.execute("PRAGMA table_info(schedules)").fetchall()
    print("\n📋 Table structure:")
    for col in columns:
        print(f"   • {col[1]} ({col[2]})")
else:
    print("❌ Failed to create schedules table")

conn.close()
print("\n✅ Database updated! Now restart your app.")