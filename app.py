"""
Flask Web Application for Sentiment Analysis
Provides interactive UI for testing sentiment analysis models
"""

import os
import json
import torch
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
from datetime import datetime

# Import model classes
from model_proposed import DimStanceModel, SimpleTokenizer
from preprocess import Preprocessor

app = Flask(__name__)
CORS(app)

# Global variables for models
proposed_model = None
baseline_model = None
vectorizer = None
tokenizer = None
preprocessor = None

# Configuration
VOCAB_SIZE = 5000
MAX_LEN = 50
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_models():
    """Load all available models"""
    global proposed_model, baseline_model, vectorizer, tokenizer, preprocessor
    
    print("[INFO] Loading models...")
    
    # Initialize preprocessor
    preprocessor = Preprocessor(remove_stopwords=True)
    
    # Load proposed model
    try:
        tokenizer = SimpleTokenizer(vocab_size=VOCAB_SIZE)
        proposed_model = DimStanceModel(vocab_size=VOCAB_SIZE).to(DEVICE)
        
        if os.path.exists("results/model_proposed.pt"):
            proposed_model.load_state_dict(torch.load("results/model_proposed.pt", map_location=DEVICE))
            proposed_model.eval()
            print("[INFO] Proposed model loaded successfully")
        else:
            print("[WARNING] Proposed model weights not found")
            proposed_model = None
    except Exception as e:
        print(f"[ERROR] Failed to load proposed model: {e}")
        proposed_model = None
    
    # Load baseline model (if saved)
    try:
        if os.path.exists("results/baseline_model.pkl"):
            with open("results/baseline_model.pkl", "rb") as f:
                baseline_model = pickle.load(f)
            with open("results/vectorizer.pkl", "rb") as f:
                vectorizer = pickle.load(f)
            print("[INFO] Baseline model loaded successfully")
        else:
            print("[WARNING] Baseline model not found")
    except Exception as e:
        print(f"[ERROR] Failed to load baseline model: {e}")

def predict_valence_arousal(text, aspect):
    """Predict valence and arousal scores using the proposed model"""
    if proposed_model is None or tokenizer is None:
        return None
    
    try:
        # Tokenize input
        tokens = tokenizer(text, aspect, max_len=MAX_LEN)
        tokens = tokens.unsqueeze(0).to(DEVICE)  # Add batch dimension
        
        # Predict
        with torch.no_grad():
            va_scores = proposed_model(tokens)
        
        valence, arousal = va_scores[0].cpu().numpy()
        
        return {
            "valence": float(valence),
            "arousal": float(arousal),
            "sentiment": get_sentiment_label(valence, arousal)
        }
    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")
        return None

def predict_baseline(text):
    """Predict using baseline model"""
    if baseline_model is None or vectorizer is None:
        return None
    
    try:
        # Preprocess text
        clean_text = preprocessor.clean_text(text)
        
        # Vectorize
        X = vectorizer.transform([clean_text])
        
        # Predict
        prediction = baseline_model.predict(X)[0]
        probabilities = baseline_model.predict_proba(X)[0]
        
        return {
            "prediction": prediction,
            "confidence": float(max(probabilities)),
            "probabilities": {label: float(prob) for label, prob in zip(baseline_model.classes_, probabilities)}
        }
    except Exception as e:
        print(f"[ERROR] Baseline prediction failed: {e}")
        return None

def get_sentiment_label(valence, arousal):
    """Convert valence and arousal to sentiment label"""
    if valence >= 6.5:
        if arousal >= 6.5:
            return "Excited/Happy"
        else:
            return "Calm/Content"
    elif valence <= 3.5:
        if arousal >= 6.5:
            return "Angry/Anxious"
        else:
            return "Sad/Depressed"
    else:
        if arousal >= 6.5:
            return "Tense/Alert"
        else:
            return "Neutral/Relaxed"

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze text sentiment"""
    try:
        data = request.json
        text = data.get('text', '').strip()
        aspect = data.get('aspect', '').strip()
        model_type = data.get('model', 'proposed')
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        result = {
            "text": text,
            "aspect": aspect,
            "timestamp": datetime.now().isoformat()
        }
        
        if model_type == 'proposed' and aspect:
            # Use proposed model for VA prediction
            prediction = predict_valence_arousal(text, aspect)
            if prediction:
                result["model"] = "Proposed (Transformer)"
                result["prediction"] = prediction
            else:
                return jsonify({"error": "Proposed model not available"}), 503
        
        elif model_type == 'baseline':
            # Use baseline model
            prediction = predict_baseline(text)
            if prediction:
                result["model"] = "Baseline (Logistic Regression)"
                result["prediction"] = prediction
            else:
                return jsonify({"error": "Baseline model not available"}), 503
        
        else:
            return jsonify({"error": "Invalid model type or missing aspect"}), 400
        
        return jsonify(result)
    
    except Exception as e:
        print(f"[ERROR] Analysis failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/batch_analyze', methods=['POST'])
def batch_analyze():
    """Analyze multiple texts"""
    try:
        data = request.json
        texts = data.get('texts', [])
        aspects = data.get('aspects', [])
        model_type = data.get('model', 'proposed')
        
        if not texts:
            return jsonify({"error": "Texts are required"}), 400
        
        results = []
        
        for i, text in enumerate(texts):
            aspect = aspects[i] if i < len(aspects) else ""
            
            if model_type == 'proposed' and aspect:
                prediction = predict_valence_arousal(text, aspect)
                if prediction:
                    results.append({
                        "text": text,
                        "aspect": aspect,
                        "prediction": prediction
                    })
            elif model_type == 'baseline':
                prediction = predict_baseline(text)
                if prediction:
                    results.append({
                        "text": text,
                        "prediction": prediction
                    })
        
        return jsonify({
            "model": model_type,
            "count": len(results),
            "results": results
        })
    
    except Exception as e:
        print(f"[ERROR] Batch analysis failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/model_info', methods=['GET'])
def model_info():
    """Get information about loaded models"""
    return jsonify({
        "proposed_model": proposed_model is not None,
        "baseline_model": baseline_model is not None,
        "device": str(DEVICE),
        "vocab_size": VOCAB_SIZE
    })

@app.route('/api/statistics', methods=['GET'])
def statistics():
    """Get dataset statistics"""
    try:
        stats = {}
        
        # Load dataset if available
        if os.path.exists("main/csv/loaded_data.csv"):
            df = pd.read_csv("main/csv/loaded_data.csv")
            stats["total_samples"] = len(df)
            
            if 'label' in df.columns:
                stats["label_distribution"] = df['label'].value_counts().to_dict()
            
            if 'Text' in df.columns:
                stats["avg_text_length"] = df['Text'].str.split().str.len().mean()
        
        return jsonify(stats)
    
    except Exception as e:
        print(f"[ERROR] Failed to get statistics: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Load models on startup
    load_models()
    
    # Run Flask app
    print("[INFO] Starting Flask server...")
    print(f"[INFO] Access the application at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
