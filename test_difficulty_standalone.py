#!/usr/bin/env python3
"""Standalone test for difficulty estimation - no Flask imports"""

import re

def estimate_difficulty(topic_name):
    """Estimate topic difficulty using balanced keyword matching and complexity analysis"""
    if not topic_name or len(topic_name.strip()) < 3:
        return 'medium'
    
    topic_lower = topic_name.lower()
    topic_words = topic_name.split()
    
    # Enhanced difficulty keywords with more comprehensive coverage
    easy_keywords = [
        'introduction', 'intro', 'basic', 'basics', 'overview', 'fundamentals', 
        'simple', 'getting started', 'beginner', 'elementary', 'foundation',
        'what is', 'definition', 'concept', 'understanding', 'primer',
        'first', 'starting', 'beginning', 'initial', 'essentials'
    ]
    
    medium_keywords = [
        'intermediate', 'application', 'practice', 'implementation', 'working with',
        'using', 'applying', 'methods', 'techniques', 'process', 'procedure',
        'analysis', 'comparison', 'types', 'classification', 'structure',
        'design', 'development', 'building', 'creating', 'programming'
    ]
    
    hard_keywords = [
        'advanced', 'complex', 'optimization', 'theory', 'deep dive', 'architecture',
        'algorithm', 'mathematical', 'proof', 'derivation', 'research', 'cutting-edge',
        'sophisticated', 'intricate', 'comprehensive', 'in-depth', 'expert',
        'quantum', 'neural', 'distributed', 'concurrent', 'cryptographic',
        'theoretical', 'abstract', 'formal'
    ]
    
    # Count keyword matches (case-insensitive, whole word matching)
    easy_score = 0
    medium_score = 0
    hard_score = 0
    
    for keyword in easy_keywords:
        if keyword in topic_lower:
            easy_score += 2  # Strong indicator
    
    for keyword in medium_keywords:
        if keyword in topic_lower:
            medium_score += 2
    
    for keyword in hard_keywords:
        if keyword in topic_lower:
            hard_score += 2
    
    # If clear keyword match found, use it
    if easy_score > medium_score and easy_score > hard_score and easy_score > 0:
        return 'easy'
    if hard_score > easy_score and hard_score > medium_score and hard_score > 0:
        return 'hard'
    if medium_score > 0:
        return 'medium'
    
    # Complexity analysis based on topic characteristics
    complexity_score = 0
    
    # 1. Word count analysis (shorter topics tend to be simpler)
    word_count = len(topic_words)
    if word_count <= 2:
        complexity_score += 0  # Very short, likely easy
    elif word_count <= 4:
        complexity_score += 1  # Short, likely easy-medium
    elif word_count <= 6:
        complexity_score += 2  # Medium length
    else:
        complexity_score += 3  # Long, likely complex
    
    # 2. Technical term detection (CamelCase, numbers, special chars)
    technical_terms = 0
    for word in topic_words:
        # Check for CamelCase (e.g., "JavaScript", "TensorFlow")
        if len(word) > 1 and any(c.isupper() for c in word[1:]):
            technical_terms += 1
        # Check for numbers (e.g., "Python3", "v2.0")
        if any(c.isdigit() for c in word):
            technical_terms += 1
    
    if technical_terms == 0:
        complexity_score += 0
    elif technical_terms == 1:
        complexity_score += 1
    else:
        complexity_score += 2
    
    # 3. Mathematical symbols or special characters
    has_math = any(char in topic_name for char in ['=', '+', '∫', '∑', '∂', '∆', 'α', 'β'])
    if has_math:
        complexity_score += 2
    
    # 4. Version numbers (usually indicates advanced/specific topics)
    has_version = bool(re.search(r'\d+\.\d+|\bv\d+\b', topic_lower))
    if has_version:
        complexity_score += 1
    
    # 5. Subject-specific difficulty patterns (known hard subjects)
    hard_subjects = [
        'calculus', 'quantum', 'thermodynamics', 'genetics', 'organic chemistry',
        'differential equations', 'linear algebra', 'topology', 'cryptography',
        'compiler', 'operating system', 'machine learning', 'deep learning'
    ]
    
    easy_subjects = [
        'html', 'css', 'basic', 'intro', 'overview', 'summary',
        'list', 'guide', 'tutorial', 'example'
    ]
    
    for subject in hard_subjects:
        if subject in topic_lower:
            complexity_score += 2
            break
    
    for subject in easy_subjects:
        if subject in topic_lower:
            complexity_score -= 2  # Reduce score for easy subjects
            break
    
    # 6. Check for action words that indicate difficulty
    if any(word in topic_lower for word in ['learn', 'understand', 'know', 'explore']):
        complexity_score -= 1  # Learning-focused, likely easier
    
    if any(word in topic_lower for word in ['master', 'expert', 'professional', 'advanced']):
        complexity_score += 2  # Mastery-focused, likely harder
    
    # Final difficulty assignment with balanced thresholds
    # Adjusted thresholds to prevent everything being marked as hard
    if complexity_score <= 2:
        return 'easy'
    elif complexity_score <= 5:
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
    failed_tests = []
    
    for topic, expected in test_topics:
        result = estimate_difficulty(topic)
        status = "✓" if result == expected else "✗"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
            failed_tests.append((topic, expected, result))
        
        print(f"{status} {topic:50} → {result:8} (expected: {expected})")
    
    print("="*70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_topics)} tests")
    print("="*70)
    
    if failed == 0:
        print("✅ All tests passed!")
    else:
        print(f"⚠️  {failed} test(s) failed:")
        for topic, expected, got in failed_tests:
            print(f"   - {topic}: expected {expected}, got {got}")
    
    return failed == 0

if __name__ == '__main__':
    run_tests()
