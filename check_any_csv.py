import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("Cyberbullying Detection - Load Any CSV File")
print("="*70)

# ============================================================
# STEP 1: SPECIFY YOUR CSV FILE HERE
# ============================================================
# Change this to your CSV filename
CSV_FILE = 'final_dataset_hinglish.csv'

# Specify your column names
TEXT_COLUMN = 'Unnamed: 0'      # Column containing the text/messages
LABEL_COLUMN = 'label'          # Column containing labels (0 or 1)

# ============================================================# ============================================================

print(f"\nLoading CSV file: {CSV_FILE}")
print("-"*70)

try:
    # Load the CSV file
    df = pd.read_csv(CSV_FILE)
    
    print(f"✓ File loaded successfully!")
    print(f"\nDataset Information:")
    print(f"  - Total rows: {len(df)}")
    print(f"  - Columns: {df.columns.tolist()}")
    print(f"  - Shape: {df.shape}")
    
    # Check if required columns exist
    if TEXT_COLUMN not in df.columns:
        print(f"\n❌ Error: Column '{TEXT_COLUMN}' not found!")
        print(f"Available columns: {df.columns.tolist()}")
        exit()
    
    if LABEL_COLUMN not in df.columns:
        print(f"\n❌ Error: Column '{LABEL_COLUMN}' not found!")
        print(f"Available columns: {df.columns.tolist()}")
        exit()
    
    # Show first few rows
    print(f"\nFirst 5 rows:")
    print(df.head())
    
    # Convert -1 labels to 1 (cyberbullying)
    print(f"\nOriginal Label Distribution:")
    print(df[LABEL_COLUMN].value_counts())
    
    # Fix labels: -1 should be 1 (cyberbullying)
    df[LABEL_COLUMN] = df[LABEL_COLUMN].replace(-1, 1)
    
    print(f"\nCorrected Label Distribution:")
    print(f"  Cyberbullying (1): {(df[LABEL_COLUMN] == 1).sum()}")
    print(f"  Non-cyberbullying (0): {(df[LABEL_COLUMN] == 0).sum()}")
    
    print("\n" + "="*70)
    print("Training Model...")
    print("="*70)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df[TEXT_COLUMN], df[LABEL_COLUMN], 
        test_size=0.2, random_state=42
    )
    
    print(f"\n✓ Training samples: {len(X_train)}")
    print(f"✓ Testing samples: {len(X_test)}")
    
    # Vectorize and train
    vectorizer = TfidfVectorizer(max_features=1000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n✓ Model trained successfully!")
    print(f"✓ Accuracy: {accuracy:.2%}")
    
    print("\n" + "="*70)
    print("Testing on Sample Texts")
    print("="*70)
    
    # Test samples - You can add or change these texts
    test_texts = [
        "I love you",
        "Have a great day!",
        "I hate you, go away",
        "Thank you for your help",
        "You're an idiot and nobody likes you",
        "Great job on your presentation!",
        "Kill yourself, loser",
        "I appreciate your hard work",
        "You're so dumb, it's embarrassing",
        "Congratulations on your success!",
        "Fuck you asshole",
        "Nice to meet you",
        "You're a waste of space",
        "That's a brilliant idea",
        "Go die in a hole",
        "You did an amazing job today",
        "You're pathetic and ugly",
        "I'm proud of your achievements",
        "Nobody wants you here",
        "Welcome to the team!"
    ]
    
    print("\nPredictions:")
    print("-"*70)
    for i, text in enumerate(test_texts, 1):
        text_vec = vectorizer.transform([text])
        prediction = model.predict(text_vec)[0]
        probability = model.predict_proba(text_vec)[0]
        
        if prediction == 1:
            label = "⚠️  CYBERBULLYING"
            conf = probability[1]
        else:
            label = "✓ SAFE"
            conf = probability[0]
        
        print(f"\n{i}. \"{text}\"")
        print(f"   → {label} (Confidence: {conf:.2%})")
    
    print("\n" + "="*70)
    print("✓ COMPLETED!")
    print("="*70)
    
except FileNotFoundError:
    print(f"\n❌ Error: File '{CSV_FILE}' not found!")
    print("\nPlease make sure:")
    print("1. The CSV file is in the same folder as this script")
    print("2. The filename is correct")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
