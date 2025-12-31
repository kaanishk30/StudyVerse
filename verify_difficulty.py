"""Quick verification of difficulty estimation logic"""
import re

def estimate_difficulty(topic_name):
    """Estimate topic difficulty - copied from app.py"""
    if not topic_name or len(topic_name.strip()) < 3:
        return 'medium'
    
    topic_lower = topic_name.lower()
    topic_words = topic_name.split()
    
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
    
    easy_score = 0
    medium_score = 0
    hard_score = 0
    
    for keyword in easy_keywords:
        if keyword in topic_lower:
            easy_score += 2
    
    for keyword in medium_keywords:
        if keyword in topic_lower:
            medium_score += 2
    
    for keyword in hard_keywords:
        if keyword in topic_lower:
            hard_score += 2
    
    if easy_score > medium_score and easy_score > hard_score and easy_score > 0:
        return 'easy'
    if hard_score > easy_score and hard_score > medium_score and hard_score > 0:
        return 'hard'
    if medium_score > 0:
        return 'medium'
    
    complexity_score = 0
    
    word_count = len(topic_words)
    if word_count <= 2:
        complexity_score += 0
    elif word_count <= 4:
        complexity_score += 1
    elif word_count <= 6:
        complexity_score += 2
    else:
        complexity_score += 3
    
    technical_terms = 0
    for word in topic_words:
        if len(word) > 1 and any(c.isupper() for c in word[1:]):
            technical_terms += 1
        if any(c.isdigit() for c in word):
            technical_terms += 1
    
    if technical_terms == 0:
        complexity_score += 0
    elif technical_terms == 1:
        complexity_score += 1
    else:
        complexity_score += 2
    
    has_math = any(char in topic_name for char in ['=', '+', '∫', '∑', '∂', '∆', 'α', 'β'])
    if has_math:
        complexity_score += 2
    
    has_version = bool(re.search(r'\d+\.\d+|\bv\d+\b', topic_lower))
    if has_version:
        complexity_score += 1
    
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
            complexity_score -= 2
            break
    
    if any(word in topic_lower for word in ['learn', 'understand', 'know', 'explore']):
        complexity_score -= 1
    
    if any(word in topic_lower for word in ['master', 'expert', 'professional', 'advanced']):
        complexity_score += 2
    
    if complexity_score <= 2:
        return 'easy'
    elif complexity_score <= 5:
        return 'medium'
    else:
        return 'hard'

# Quick test
print("Testing a few examples:")
print(f"'Introduction to Python' -> {estimate_difficulty('Introduction to Python')} (expected: easy)")
print(f"'Basic HTML' -> {estimate_difficulty('Basic HTML')} (expected: easy)")
print(f"'Python Programming' -> {estimate_difficulty('Python Programming')} (expected: medium)")
print(f"'Advanced Machine Learning' -> {estimate_difficulty('Advanced Machine Learning')} (expected: hard)")
print(f"'Quantum Computing' -> {estimate_difficulty('Quantum Computing')} (expected: hard)")
print("\nDone!")
