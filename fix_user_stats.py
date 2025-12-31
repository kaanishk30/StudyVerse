#!/usr/bin/env python3
"""Fix user_stats table for existing users"""

import sqlite3

def fix_user_stats():
    """Ensure all users have complete user_stats records"""
    conn = sqlite3.connect('studypal.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("Checking user_stats table...")
    
    # Get all users
    users = cursor.execute('SELECT id FROM users').fetchall()
    print(f"Found {len(users)} users")
    
    fixed = 0
    created = 0
    
    for user in users:
        user_id = user['id']
        
        # Check if user_stats exists
        stats = cursor.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,)).fetchone()
        
        if not stats:
            # Create user_stats
            cursor.execute('''
                INSERT INTO user_stats (user_id, streak, last_activity, total_quizzes, correct_answers, total_questions, total_study_time)
                VALUES (?, 0, NULL, 0, 0, 0, 0)
            ''', (user_id,))
            created += 1
            print(f"  Created user_stats for user {user_id}")
        else:
            # Check if all fields exist
            needs_update = False
            
            # Check for missing columns
            try:
                _ = stats['total_questions']
            except:
                needs_update = True
            
            try:
                _ = stats['total_study_time']
            except:
                needs_update = True
            
            if needs_update:
                # Update to ensure all fields exist
                cursor.execute('''
                    UPDATE user_stats 
                    SET total_questions = COALESCE(total_questions, 0),
                        total_study_time = COALESCE(total_study_time, 0)
                    WHERE user_id = ?
                ''', (user_id,))
                fixed += 1
                print(f"  Fixed user_stats for user {user_id}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Done!")
    print(f"  Created: {created}")
    print(f"  Fixed: {fixed}")
    print(f"  Total: {len(users)}")

if __name__ == '__main__':
    fix_user_stats()
