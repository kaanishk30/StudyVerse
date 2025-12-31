"""
One-time NLTK data download script
Run this once before starting the app
"""
import nltk

print("📦 Downloading all required NLTK data...")
print("This may take a minute...\n")

datasets = [
    'punkt',
    'punkt_tab', 
    'stopwords',
    'averaged_perceptron_tagger',
    'averaged_perceptron_tagger_eng'
]

for dataset in datasets:
    try:
        print(f"Downloading {dataset}...", end=' ')
        nltk.download(dataset, quiet=True)
        print("✓")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n✅ NLTK setup complete!")
print("You can now run: python app.py")