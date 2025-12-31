#!/usr/bin/env python3
"""
Test script for AI Scheduler functionality
"""

import sys
sys.path.insert(0, '.')

from datetime import datetime
from app import AIScheduler

def test_parse_syllabus():
    """Test syllabus parsing"""
    print("🧪 Testing Syllabus Parsing...")
    
    syllabus = """
Unit 1: Introduction to Data Structures
- Arrays and Linked Lists
- Stacks and Queues
- Trees and Graphs

Unit 2: Algorithms
- Sorting Algorithms
- Searching Algorithms
- Dynamic Programming
"""
    
    structure = AIScheduler.parse_syllabus(syllabus)
    
    print(f"  ✅ Found {len(structure)} units")
    for unit in structure:
        print(f"     📚 {unit['unit_name']}: {len(unit['topics'])} topics")
        for topic in unit['topics']:
            print(f"        - {topic}")
    
    assert len(structure) == 2, "Should find 2 units"
    assert len(structure[0]['topics']) == 3, "Unit 1 should have 3 topics"
    assert len(structure[1]['topics']) == 3, "Unit 2 should have 3 topics"
    
    print("  ✅ Syllabus parsing works!\n")

def test_difficulty_estimation():
    """Test difficulty estimation"""
    print("🧪 Testing Difficulty Estimation...")
    
    test_cases = [
        ("Introduction to Programming", "easy"),
        ("Basic Concepts", "easy"),
        ("Intermediate Data Structures", "medium"),
        ("Advanced Optimization Techniques", "hard"),
        ("Complex Algorithm Theory", "hard"),
        ("Arrays", "easy"),  # Short = easy
        ("Working with Database Systems", "medium"),  # Medium length
    ]
    
    for topic, expected in test_cases:
        result = AIScheduler.estimate_difficulty(topic)
        status = "✅" if result == expected else "❌"
        print(f"  {status} '{topic}' → {result} (expected: {expected})")
    
    print("  ✅ Difficulty estimation works!\n")

def test_schedule_generation():
    """Test schedule generation"""
    print("🧪 Testing Schedule Generation...")
    
    syllabus = """
Unit 1: Python Basics
- Introduction to Python
- Variables and Data Types
- Control Flow

Unit 2: Advanced Python
- Object-Oriented Programming
- File Handling
- Error Handling
"""
    
    schedule = AIScheduler.generate_schedule(
        syllabus_text=syllabus,
        total_days=10,
        start_date="2025-01-01"
    )
    
    print(f"  ✅ Generated {len(schedule)} schedule items")
    
    for i, item in enumerate(schedule[:3], 1):
        print(f"     {i}. {item['scheduled_date']} {item['start_time']}-{item['end_time']}")
        print(f"        {item['topic_name']} ({item['difficulty']}, {item['estimated_hours']}h)")
        print(f"        Unit: {item['unit_name']}")
    
    if len(schedule) > 3:
        print(f"     ... and {len(schedule) - 3} more items")
    
    assert len(schedule) > 0, "Should generate at least one schedule item"
    assert all('scheduled_date' in item for item in schedule), "All items should have dates"
    assert all('difficulty' in item for item in schedule), "All items should have difficulty"
    
    print("  ✅ Schedule generation works!\n")

def test_unstructured_syllabus():
    """Test parsing unstructured topic list"""
    print("🧪 Testing Unstructured Syllabus...")
    
    syllabus = """
Arrays
Linked Lists
Stacks
Queues
Trees
Graphs
"""
    
    structure = AIScheduler.parse_syllabus(syllabus)
    
    print(f"  ✅ Found {len(structure)} unit (General Topics)")
    print(f"  ✅ Found {len(structure[0]['topics'])} topics")
    
    for topic in structure[0]['topics']:
        print(f"     - {topic}")
    
    assert len(structure) == 1, "Should create one general unit"
    assert len(structure[0]['topics']) == 6, "Should find 6 topics"
    
    print("  ✅ Unstructured parsing works!\n")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 AI SCHEDULER TEST SUITE")
    print("="*60 + "\n")
    
    try:
        test_parse_syllabus()
        test_difficulty_estimation()
        test_schedule_generation()
        test_unstructured_syllabus()
        
        print("="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60 + "\n")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit(main())
