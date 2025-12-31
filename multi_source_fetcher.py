import requests
from bs4 import BeautifulSoup
import wikipediaapi
import re
import time
from typing import List, Dict, Tuple

class MultiSourceLearner:
    """
    Fetches educational content from multiple sources with automatic fallback
    """
    
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent="AI_Study_Pal_Multi/1.0"
        )
        
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        text = re.sub(r'={2,}[^=]*={2,}', '', text)
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        return text.strip()
    
    def fetch_from_wikipedia(self, query: str) -> Tuple[str, str]:
        """Source 1: Wikipedia"""
        try:
            print(f"  📖 [Wikipedia] Searching: {query}")
            search_terms = [
                query, 
                query.title(), 
                f"{query} (concept)",
                f"{query} (technology)",
                f"{query} (computing)"
            ]
            
            for term in search_terms:
                page = self.wiki.page(term)
                if page.exists():
                    text = page.text if hasattr(page, 'text') else page.summary
                    if len(text) > 100:
                        print(f"  ✅ [Wikipedia] Found: {page.title}")
                        return self.clean_text(text[:3000]), f"Wikipedia: {page.title}"
        except Exception as e:
            print(f"  ⚠️ [Wikipedia] Error: {e}")
        return "", ""
    
    def fetch_from_britannica(self, query: str) -> Tuple[str, str]:
        """Source 2: Britannica (web scraping)"""
        try:
            print(f"  📚 [Britannica] Searching: {query}")
            url = f"https://www.britannica.com/search?query={query.replace(' ', '+')}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find first search result
            first_result = soup.find('a', class_='font-14')
            if first_result and first_result.get('href'):
                article_url = first_result['href']
                if not article_url.startswith('http'):
                    article_url = 'https://www.britannica.com' + article_url
                
                # Fetch article content
                article_response = requests.get(article_url, headers=headers, timeout=10)
                article_soup = BeautifulSoup(article_response.content, 'html.parser')
                
                # Extract paragraphs
                paragraphs = article_soup.find_all('p', limit=10)
                text = ' '.join([p.get_text() for p in paragraphs])
                
                if len(text) > 100:
                    print(f"  ✅ [Britannica] Found article")
                    return self.clean_text(text[:3000]), f"Britannica: {query.title()}"
        except Exception as e:
            print(f"  ⚠️ [Britannica] Error: {e}")
        return "", ""
    
    def fetch_from_simple_wikipedia(self, query: str) -> Tuple[str, str]:
        """Source 3: Simple English Wikipedia (easier to understand)"""
        try:
            print(f"  📖 [Simple Wiki] Searching: {query}")
            simple_wiki = wikipediaapi.Wikipedia(
                language='simple',
                extract_format=wikipediaapi.ExtractFormat.WIKI,
                user_agent="AI_Study_Pal_Multi/1.0"
            )
            
            page = simple_wiki.page(query)
            if page.exists():
                text = page.text if hasattr(page, 'text') else page.summary
                if len(text) > 100:
                    print(f"  ✅ [Simple Wiki] Found: {page.title}")
                    return self.clean_text(text[:3000]), f"Simple Wikipedia: {page.title}"
        except Exception as e:
            print(f"  ⚠️ [Simple Wiki] Error: {e}")
        return "", ""
    
    def fetch_from_arxiv_summary(self, query: str) -> Tuple[str, str]:
        """Source 4: arXiv papers (for technical/scientific topics)"""
        try:
            print(f"  🔬 [arXiv] Searching: {query}")
            api_url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=3"
            
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                entries = soup.find_all('entry')
                
                if entries:
                    combined_text = ""
                    for entry in entries[:2]:
                        summary = entry.find('summary')
                        if summary:
                            combined_text += summary.get_text() + "\n\n"
                    
                    if len(combined_text) > 100:
                        print(f"  ✅ [arXiv] Found {len(entries)} papers")
                        return self.clean_text(combined_text[:3000]), f"arXiv Research Papers"
        except Exception as e:
            print(f"  ⚠️ [arXiv] Error: {e}")
        return "", ""
    
    def fetch_from_duckduckgo(self, query: str) -> Tuple[str, str]:
        """Source 5: DuckDuckGo Instant Answer API"""
        try:
            print(f"  🔍 [DuckDuckGo] Searching: {query}")
            api_url = f"https://api.duckduckgo.com/?q={query}&format=json"
            
            response = requests.get(api_url, timeout=10)
            data = response.json()
            
            text = ""
            if data.get('AbstractText'):
                text = data['AbstractText']
            elif data.get('RelatedTopics'):
                for topic in data['RelatedTopics'][:5]:
                    if isinstance(topic, dict) and topic.get('Text'):
                        text += topic['Text'] + "\n\n"
            
            if len(text) > 100:
                print(f"  ✅ [DuckDuckGo] Found instant answer")
                return self.clean_text(text[:3000]), "DuckDuckGo Instant Answer"
        except Exception as e:
            print(f"  ⚠️ [DuckDuckGo] Error: {e}")
        return "", ""
    
    def search_and_learn(self, query: str) -> Tuple[List[Dict], List[str]]:
        """
        Main method: Try all sources with automatic fallback
        Returns: (segments, sources)
        """
        print(f"\n{'='*60}")
        print(f"🔎 Multi-Source Search for: {query}")
        print(f"{'='*60}")
        
        all_content = []
        sources_used = []
        
        # Try all sources in order
        fetch_methods = [
            self.fetch_from_wikipedia,
            self.fetch_from_simple_wikipedia,
            self.fetch_from_britannica,
            self.fetch_from_duckduckgo,
            self.fetch_from_arxiv_summary
        ]
        
        for fetch_method in fetch_methods:
            try:
                text, source = fetch_method(query)
                if text and len(text) > 100:
                    all_content.append(text)
                    sources_used.append(source)
                    
                    # If we have good content, we can stop
                    if len(text) > 500:
                        break
                
                time.sleep(0.5)  # Be respectful to APIs
            except Exception as e:
                print(f"  ⚠️ Error with {fetch_method.__name__}: {e}")
                continue
        
        if not all_content:
            print(f"  ❌ No content found for '{query}'")
            return [], []
        
        # Combine all content
        combined_text = "\n\n".join(all_content)
        
        # Segment the content
        segments = self._segment_into_topics(combined_text, query)
        
        print(f"  ✅ Created {len(segments)} segments from {len(sources_used)} sources")
        print(f"{'='*60}\n")
        
        return segments, sources_used
    
    def _segment_into_topics(self, text: str, main_topic: str) -> List[Dict]:
        """Split text into digestible segments"""
        from nltk.tokenize import sent_tokenize
        
        try:
            sentences = sent_tokenize(text)
        except:
            sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
        
        # Clean sentences
        complete = []
        for sent in sentences:
            sent = sent.strip()
            if not sent or len(sent.split()) < 3:
                continue
            if sent[-1] not in '.!?':
                sent += '.'
            if len(sent.split()) <= 100:
                complete.append(sent)
        
        if len(complete) < 3:
            return [{
                'title': main_topic,
                'content': complete,
                'key_points': complete
            }]
        
        # Create segments
        segments = []
        segment_size = 5
        
        for i in range(0, len(complete), segment_size):
            batch = complete[i:i+segment_size+2]
            if batch:
                segments.append({
                    'title': f"{main_topic} - Part {len(segments)+1}",
                    'content': batch,
                    'key_points': batch[:5]
                })
        
        return segments


# Example usage
if __name__ == "__main__":
    learner = MultiSourceLearner()
    segments, sources = learner.search_and_learn("Kubernetes")
    
    print(f"\nFound {len(segments)} segments from sources:")
    for source in sources:
        print(f"  - {source}")