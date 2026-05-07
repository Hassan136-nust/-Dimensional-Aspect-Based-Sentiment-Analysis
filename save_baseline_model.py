"""
Script to train and save the baseline model for the web application
"""

import os
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from preprocess import Preprocessor

def train_and_save_baseline():
    """Train baseline model and save for web app"""
    
    print("[INFO] Loading dataset...")
    
    # Try to load the dataset
    csv_path = "main/csv/loaded_data.csv"
    if not os.path.exists(csv_path):
        print(f"[ERROR] Dataset not found at {csv_path}")
        print("[INFO] Please run data_loader.py first to create the dataset")
        return
    
    df = pd.read_csv(csv_path)
    
    # Check required columns
    if 'Text' not in df.columns or 'Aspects' not in df.columns:
        print("[ERROR] CSV must contain 'Text' and 'Aspects' columns")
        return
    
    # Drop rows with missing values
    df = df.dropna(subset=['Text', 'Aspects']).reset_index(drop=True)
    
    print(f"[INFO] Loaded {len(df)} samples")
    
    # Initialize preprocessor
    preprocessor = Preprocessor(remove_stopwords=True)
    
    # Preprocess text
    print("[INFO] Preprocessing text...")
    df['clean_text'] = df['Text'].apply(preprocessor.clean_text)
    df['label'] = df['Aspects']
    
    # Handle rare labels for stratified split
    label_counts = df['label'].value_counts()
    stratify_labels = label_counts[label_counts >= 2].index.tolist()
    df_strat = df[df['label'].isin(stratify_labels)]
    df_rare = df[~df['label'].isin(stratify_labels)]
    
    # Stratified split for common labels
    train_strat, test_strat = train_test_split(
        df_strat, test_size=0.2, random_state=42, stratify=df_strat['label']
    )
    
    # Combine with rare labels (all in training)
    train_df = pd.concat([train_strat, df_rare]).reset_index(drop=True)
    test_df = test_strat.reset_index(drop=True)
    
    print(f"[INFO] Training samples: {len(train_df)}, Testing samples: {len(test_df)}")
    
    # Create vectorizer and model
    print("[INFO] Training model...")
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    model = LogisticRegression(max_iter=1000)
    
    # Fit vectorizer and model
    X_train = vectorizer.fit_transform(train_df["clean_text"])
    y_train = train_df["label"]
    
    model.fit(X_train, y_train)
    
    # Evaluate on test set
    X_test = vectorizer.transform(test_df["clean_text"])
    y_test = test_df["label"]
    
    accuracy = model.score(X_test, y_test)
    print(f"[INFO] Test accuracy: {accuracy:.4f}")
    
    # Save model and vectorizer
    os.makedirs("results", exist_ok=True)
    
    with open("results/baseline_model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    with open("results/vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    
    print("[INFO] Model and vectorizer saved to results/")
    print("[SUCCESS] Baseline model is ready for the web application!")

if __name__ == "__main__":
    train_and_save_baseline()
