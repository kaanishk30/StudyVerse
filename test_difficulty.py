#!/usr/bin/env python3
"""Test the enhanced difficulty analysis"""

import sys
import re

# Simulate the AIScheduler.estimate_difficulty method
def estimate_difficulty(topic_name):
    """Estimate topic difficulty using advanced keyword matching and complexity analysis"""
    topic_lower = topic_name.lower()
    
    # Enhanced difficulty keywords
    easy_keywords = [
        'introduction', 'intro', 'basic', 'basics', 'overview', 'fundamentals', 
        'simple', 'getting started', 'beginner', 'elementary', 'foundation',
        'what is', 'definition', 'concept', 'understanding', 'primer'
    ]
    
    medium_keywords = [
        'intermediate', 'application', 'practice', 'implementation', 'working with',
        'using', 'applying', 'methods', 'techniques', 'process', 'procedure',
        'analysis', 'comparison', 'types', 'classification', 'structure'
    ]
    
    hard_keywords = [
        'advanced', 'complex', 'optimization', 'theory', 'deep dive', 'architecture',
        'algorithm', 'mathematical', 'proof', 'derivation', 'research', 'cutting-edge',
        'sophisticated', 'intricate', 'comprehensive', 'in-depth', 'expert',
        'quantum', 'neural', 'distributed', 'concurrent', 'cryptographic'
    ]
    
    # Check for explicit difficulty keywords
    easy_score = sum(1 for keyword in easy_keywords if keyword in topic_lower)
    medium_score = sum(1 for keyword in medium_keywords if keyword in topic_lower)
    hard_score = sum(1 for keyword in hard_keywords if keyword in topic_lower)
    
    # If clear keyword match found
    if hard_score > 0:
        return 'hard'
    if easy_score > medium_score and easy_score > 0:
        return 'easy'
    if medium_score > 0:
        return 'medium'
    
    # Complexity analysis based on topic characteristics
    word_count = len(topic_name.split())
    
    # Check for technical terms (words with capital letters in middle or numbers)
    technical_terms = len([w for w in topic_name.split() if any(c.isupper() for c in w[1:]) or any(c.isdigit() for c in w)])
    
    # Check for mathematical symbols or special characters
    has_math = any(char in topic_name for char in ['=', '+', '-', '*', '/', '^', '∫', '∑', '∂'])
    
    # Check for version numbers or advanced topics
    has_version = bool(re.search(r'\d+\.\d+|\bv\d+\b', topic_lower))
    
    # Scoring system
    complexity_score = 0
    
    # Word count scoring
    if word_count <= 3:
        complexity_score += 0
    elif word_count <= 6:
        complexity_score += 1
    else:
        complexity_score += 2
    
    # Technical terms scoring
    if technical_terms >= 2:
        complexity_score += 2
    elif technical_terms == 1:
        complexity_score += 1
    
    # Mathematical content
    if has_math:
        complexity_score += 2
    
    # Version numbers (usually advanced)
    if has_version:
        complexity_score += 1
    
    # Subject-specific difficulty patterns
    if any(term in topic_lower for term in ['calculus', 'quantum', 'thermodynamics', 'genetics', 'organic chemistry']):
        complexity_score += 2
    
    # Final difficulty assignment
    if complexity_score <= 1:
        return 'easy'
    elif complexity_score <= 3:
        return 'medium'
    else:
        return 'hard'

# Test cases with expected difficulties
test_topics = [
    # Easy topics (score <= 2)
    ("Introduction to Python", "easy"),
    ("Basic HTML Tags", "easy"),
    ("What is JavaScript", "easy"),
    ("Understanding CSS", "easy"),
    ("Beginner's Guide", "easy"),
    ("HTML Basics", "easy"),
    ("Simple Variables", "easy"),
    ("Getting Started", "easy"),
    ("Overview of Java", "easy"),
    ("First Steps", "easy"),
    
    # Medium topics (score 3-5)
    ("Data Structures Implementation", "medium"),
    ("API Integration Methods", "medium"),
    ("Database Design Techniques", "medium"),
    ("Web Application Development", "medium"),
    ("Software Testing Process", "medium"),
    ("Python Programming", "medium"),
    ("Object Oriented Programming", "medium"),
    ("Network Protocols", "medium"),
    ("File System Management", "medium"),
    ("Memory Management", "medium"),
    
    # Hard topics (score > 5)
    ("Advanced Machine Learning Algorithms", "hard"),
    ("Quantum Computing Theory", "hard"),
    ("Neural Network Architecture", "hard"),
    ("Cryptographic Protocols", "hard"),
    ("Distributed Systems Optimization", "hard"),
    ("Calculus and Differential Equations", "hard"),
    ("React v18.0 Advanced Features", "hard"),
    ("Deep Learning Optimization", "hard"),
    ("Compiler Design Theory", "hard"),
    ("Operating System Internals", "hard"),
]

def run_tests():
    print("="*70)
    print("Testing Enhanced Difficulty Analysis")
    print("="*70)
    
    passed = 0
    failed = 0
    
    for topic, expected in test_topics:
        result = estimate_difficulty(topic)
        status = "✓" if result == expected else "✗"
        
        if result == expected:
            passed += 1
            color = ""
        else:
            failed += 1
            color = "FAILED: "
        
        print(f"{status} {topic:50} → {result:8} (expected: {expected})")
    
    print("="*70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_topics)} tests")
    print("="*70)
    
    if failed == 0:
        print("✅ All tests passed!")
    else:
        print(f"⚠️  {failed} test(s) failed")
    
    return failed == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
