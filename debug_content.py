#!/usr/bin/env python3
"""
Debug script to test content processing
Run this to see what's happening with your PDFs and searches
"""

import PyPDF2
import wikipediaapi
from nltk.tokenize import sent_tokenize
import re

def test_pdf_extraction(pdf_path):
    """Test PDF extraction"""
    print("\n" + "="*60)
    print(f"📄 TESTING PDF: {pdf_path}")
    print("="*60)
    
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            print(f"✅ PDF loaded successfully")
            print(f"📊 Total pages: {len(reader.pages)}")
            
            total_text = ""
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                total_text += text
                print(f"  Page {i+1}: {len(text)} characters")
            
            print(f"\n📝 Total extracted: {len(total_text)} characters")
            print(f"\n🔍 First 300 characters:")
            print("-" * 60)
            print(total_text[:300])
            print("-" * 60)
            
            # Count sentences
            sentences = sent_tokenize(total_text)
            print(f"\n📊 Found {len(sentences)} sentences")
            
            if len(sentences) > 0:
                print(f"\n📝 First 3 sentences:")
                for i, sent in enumerate(sentences[:3], 1):
                    print(f"  {i}. {sent}")
            
            return total_text
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_wikipedia_search(query):
    """Test Wikipedia search"""
    print("\n" + "="*60)
    print(f"🔎 TESTING WIKIPEDIA SEARCH: {query}")
    print("="*60)
    
    wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent="DebugScript/1.0"
    )
    
    # Try different variations
    variations = [
        query,
        query.title(),
        query.capitalize(),
        f"{query} (software)",
        f"{query} (technology)",
        f"{query} (computing)"
    ]
    
    for variant in variations:
        print(f"\n🔍 Trying: '{variant}'")
        try:
            page = wiki.page(variant)
            
            if page.exists():
                print(f"  ✅ FOUND!")
                print(f"  📄 Title: {page.title}")
                print(f"  🔗 URL: {page.fullurl}")
                
                text = page.text if hasattr(page, 'text') else page.summary
                print(f"  📊 Length: {len(text)} characters")
                
                # Show first 500 chars
                print(f"\n  📝 Preview:")
                print("  " + "-" * 56)
                preview = text[:500].replace('\n', '\n  ')
                print(f"  {preview}")
                print("  " + "-" * 56)
                
                return text
            else:
                print(f"  ❌ Not found")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n❌ Could not find any Wikipedia page for '{query}'")
    return None

def test_segmentation(text, topic):
    """Test text segmentation"""
    print("\n" + "="*60)
    print(f"✂️ TESTING SEGMENTATION: {topic}")
    print("="*60)
    
    # Clean text
    cleaned = text
    
    # Extract sentences
    sentences = sent_tokenize(cleaned)
    print(f"📊 Found {len(sentences)} sentences")
    
    # Filter sentences
    complete = []
    for sent in sentences:
        sent = sent.strip()
        if (sent and 
            sent[-1] in '.!?' and 
            3 <= len(sent.split()) <= 100):
            complete.append(sent)
    
    print(f"✅ Kept {len(complete)} quality sentences")
    
    # Create segments
    if len(complete) < 3:
        print("⚠️ Too few sentences for segmentation")
        return []
    
    segments = []
    current_batch = []
    segment_num = 1
    
    for i, sent in enumerate(complete):
        current_batch.append(sent)
        
        if len(current_batch) >= 5:
            segments.append({
                'title': f"{topic} - Part {segment_num}",
                'content': current_batch[:],
                'key_points': current_batch[:5]
            })
            print(f"  📦 Segment {segment_num}: {len(current_batch)} sentences")
            current_batch = []
            segment_num += 1
    
    if current_batch:
        segments.append({
            'title': f"{topic} - Part {segment_num}",
            'content': current_batch,
            'key_points': current_batch[:5]
        })
        print(f"  📦 Segment {segment_num}: {len(current_batch)} sentences")
    
    print(f"\n✅ Created {len(segments)} segments")
    
    # Show first segment
    if segments:
        print(f"\n📝 FIRST SEGMENT PREVIEW:")
        print("-" * 60)
        seg = segments[0]
        print(f"Title: {seg['title']}")
        print(f"Content ({len(seg['content'])} sentences):")
        for i, sent in enumerate(seg['content'][:3], 1):
            print(f"  {i}. {sent}")
        print("-" * 60)
    
    return segments

def main():
    """Run all tests"""
    print("\n" + "🔧 CONTENT PROCESSING DEBUG TOOL" + "\n")
    
    # Test 1: PDF extraction
    pdf_path = input("📁 Enter path to PDF file (or press Enter to skip): ").strip()
    if pdf_path:
        pdf_text = test_pdf_extraction(pdf_path)
        if pdf_text:
            test_segmentation(pdf_text, "Your PDF Content")
    
    # Test 2: Wikipedia search
    print("\n" + "-"*60)
    search_query = input("\n🔎 Enter search term to test (e.g., 'pods', 'jenkins'): ").strip()
    if search_query:
        wiki_text = test_wikipedia_search(search_query)
        if wiki_text:
            test_segmentation(wiki_text, search_query.title())
    
    print("\n" + "="*60)
    print("✅ Debug session complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
    except:
        pass
    
    main()