#!/usr/bin/env python3
"""
Test study time tracking
"""

from app import app
import json

def test_study_time_tracking():
    """Test if study time is being tracked and saved"""
    
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['current_study'] = {
                'segments': [{
                    'title': 'Test Topic',
                    'content': ['Test content'],
                    'quiz': [
                        {
                            'question': 'Test question?',
                            'options': ['A', 'B', 'C', 'D'],
                            'answer': 'A',
                            'type': 'Multiple Choice'
                        }
                    ]
                }],
                'topic': 'Test Topic',
                'quiz_mode': 'enabled',
                'sources': ['Test']
            }
        
        # Simulate quiz submission with 120 seconds (2 minutes) study time
        response = client.post('/submit_quiz',
            json={
                'segment_index': 0,
                'answers': {'0': 'A'},
                'study_duration': 120  # 2 minutes = 120 seconds
            },
            content_type='application/json'
        )
        
        print(f"Response Status: {response.status_code}")
        data = response.get_json()
        print(f"Response Data: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            print(f"\n✅ Quiz submitted successfully!")
            print(f"Study time added: {data.get('study_time_added')} minutes")
            
            # Check database
            import sqlite3
            conn = sqlite3.connect('studypal.db')
            conn.row_factory = sqlite3.Row
            stats = conn.execute('SELECT total_study_time, total_quizzes FROM user_stats WHERE user_id = 1').fetchone()
            conn.close()
            
            print(f"\nDatabase Check:")
            print(f"  Total Study Time: {stats['total_study_time']} minutes")
            print(f"  Total Quizzes: {stats['total_quizzes']}")
            
            return True
        else:
            print(f"\n❌ Quiz submission failed!")
            return False

if __name__ == '__main__':
    print("="*60)
    print("Testing Study Time Tracking")
    print("="*60)
    
    success = test_study_time_tracking()
    
    print("\n" + "="*60)
    if success:
        print("✅ TEST PASSED - Study time tracking works!")
    else:
        print("❌ TEST FAILED - Study time tracking not working")
    print("="*60)
