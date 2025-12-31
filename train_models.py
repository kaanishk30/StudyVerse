import pandas as pd
import numpy as np
import wikipediaapi
import nltk
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPRegressor
import joblib
import time
import os

# Create models directory
if not os.path.exists('models'):
    os.makedirs('models')

# NLTK Setup
print("📦 Downloading NLTK data...")
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

# ==========================================
# 1. DATA COLLECTION
# ==========================================
print("🔄 Connecting to Wikipedia...")
wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="AI_Study_Pal_Project/1.0 (contact: students@example.com)" 
)

# Expanded topic list with exact Wikipedia page names
topics = [
    "Python (programming language)", 
    "Artificial intelligence", 
    "Machine learning", 
    "Photosynthesis", 
    "Gravity", 
    "United States",
    "Calculus", 
    "DNA", 
    "Economy", 
    "Climate change", 
    "William Shakespeare", 
    "Quantum mechanics",
    "Thermodynamics", 
    "Neuroscience", 
    "American Civil War",
    "Bacteria",
    "World War II",
    "French Revolution",
    "Solar System",
    "Biology",
    "Chemistry",
    "Physics",
    "Mathematics",
    "Computer science",
    "Psychology"
]

data_list = []
print("📥 Downloading articles...")
successful = 0
failed = 0

for topic in topics:
    try:
        page = wiki.page(topic)
        if page.exists():
            # Get longer text for better training
            full_text = page.text if hasattr(page, 'text') else page.summary
            summary_text = full_text[0:800] if len(full_text) > 800 else full_text
            
            # Better difficulty classification
            is_hard = any(x in topic.lower() for x in ['calculus', 'quantum', 'thermodynamics', 'neuroscience', 'physics'])
            difficulty = 'hard' if is_hard else 'easy'
            
            data_list.append({
                'text': summary_text,
                'subject': topic,
                'difficulty': difficulty
            })
            successful += 1
            print(f"  ✓ {topic}")
        else:
            print(f"  ✗ {topic} - Page not found")
            failed += 1
    except Exception as e:
        print(f"  ✗ {topic} - Error: {str(e)[:50]}")
        failed += 1
    
    time.sleep(0.3)  # Be nice to Wikipedia

print(f"\n✅ Successfully collected {successful} samples")
print(f"❌ Failed: {failed} samples")

if len(data_list) < 5:
    print("⚠️ WARNING: Very few samples collected. Models may not work well.")

df = pd.DataFrame(data_list)

# ==========================================
# 2. ML: LOGISTIC REGRESSION (Difficulty)
# ==========================================
print("\n🧠 Training Quiz Difficulty Model...")
vectorizer = CountVectorizer(stop_words='english', max_features=1000, min_df=1)
X = vectorizer.fit_transform(df['text'])
y = df['difficulty']

log_reg = LogisticRegression(max_iter=1000)
log_reg.fit(X, y)

joblib.dump(vectorizer, 'models/vectorizer.pkl')
joblib.dump(log_reg, 'models/quiz_model.pkl')
print("  ✓ Difficulty classifier saved")

# ==========================================
# 3. DL: NEURAL NETWORK (Summarization Scorer)
# ==========================================
print("🧠 Training Neural Importance Scorer...")
tfidf_summary = TfidfVectorizer(max_features=100, stop_words='english', min_df=1)
X_dl = tfidf_summary.fit_transform(df['text']).toarray()
y_dl = np.array([min(len(t.split())/100, 1.0) for t in df['text']]) 

model = MLPRegressor(
    hidden_layer_sizes=(32, 16), 
    activation='relu', 
    solver='adam', 
    max_iter=1000,
    random_state=42
)
model.fit(X_dl, y_dl)

joblib.dump(model, 'models/summary_model.pkl')
joblib.dump(tfidf_summary, 'models/tfidf_summary.pkl')
print("  ✓ Summary model saved")

print("\n✅ SUCCESS! All models trained and saved to 'models/' folder")
print("\n🚀 Now run: python app.py")