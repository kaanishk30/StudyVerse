#!/usr/bin/env python3
"""
Test script to verify search functionality
"""

from app import multi_learner, segment_into_topics, generate_quiz_for_segment

def test_search(query):
    print(f"\n{'='*60}")
    print(f"Testing: {query}")
    print(f"{'='*60}")
    
    # Search
    segments, sources = multi_learner.search_and_learn(query)
    
    print(f"\nResults:")
    print(f"  Segments: {len(segments)}")
    print(f"  Sources: {sources}")
    
    if segments:
        print(f"\nFirst Segment:")
        print(f"  Title: {segments[0].get('title')}")
        print(f"  Content items: {len(segments[0].get('content', []))}")
        print(f"  Key points: {len(segments[0].get('key_points', []))}")
        
        # Test quiz generation
        quiz = generate_quiz_for_segment(segments[0])
        print(f"  Quiz questions: {len(quiz)}")
        
        return True
    else:
        print("  ❌ NO SEGMENTS GENERATED!")
        return False

if __name__ == '__main__':
    tests = [
        "Machine Learning vs Deep Learning",
        "Jenkins",
        "Kubernetes",
        "Photosynthesis"
    ]
    
    results = []
    for query in tests:
        success = test_search(query)
        results.append((query, success))
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for query, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {query}")
    
    all_passed = all(success for _, success in results)
    print(f"\n{'='*60}")
    if all_passed:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print(f"{'='*60}\n")
