# 🚀 Quick Start Guide

## ✅ Your Web Application is Running!

The sentiment analysis web application is now live and accessible at:

**🌐 http://localhost:5000**

Both models are loaded and ready:
- ✓ Proposed Model (Transformer - Valence & Arousal)
- ✓ Baseline Model (Logistic Regression - Classification)

---

## 📖 How to Use

### 1. Open Your Browser
Navigate to: **http://localhost:5000**

### 2. Analyze Single Text

#### Using Proposed Model (Valence & Arousal):
1. Select "Proposed Model (Valence & Arousal)" from the dropdown
2. Enter your text in the text area
3. Enter an aspect (e.g., "environmental_protection", "restaurant", "laptop")
4. Click "Analyze Sentiment"
5. View results showing:
   - **Valence** (1-9): How positive/negative the sentiment is
   - **Arousal** (1-9): How energetic/calm the sentiment is
   - **Sentiment Label**: Combined interpretation

#### Using Baseline Model (Classification):
1. Select "Baseline Model (Classification)" from the dropdown
2. Enter your text in the text area
3. Click "Analyze Sentiment"
4. View results showing:
   - **Prediction**: The predicted category
   - **Confidence**: Model confidence percentage
   - **Class Probabilities**: Distribution across all classes

### 3. Try Example Texts
Click any of the "Example" buttons to load pre-configured sample texts

### 4. Batch Analysis
1. Prepare a CSV file with columns:
   - `Text`: The text to analyze (required)
   - `Aspect`: The aspect (optional, required for Proposed Model)
2. Upload the CSV file
3. Click "Process Batch"
4. Download results as CSV

**Sample CSV provided**: `example_batch.csv`

---

## 🎯 Example Texts to Try

### Positive Environmental Text:
```
Text: "The new environmental protection policy is absolutely fantastic and will help save our planet for future generations."
Aspect: environmental_protection
```

### Negative Restaurant Review:
```
Text: "The food at this restaurant was terrible and the service was extremely slow."
Aspect: restaurant
```

### Positive Product Review:
```
Text: "This laptop has amazing performance and the battery life is incredible."
Aspect: laptop
```

---

## 📊 Understanding Results

### Valence & Arousal Scale (1-9)

**Valence (Positivity):**
- 7-9: Very Positive
- 5.5-7: Positive
- 3.5-5.5: Neutral
- 2-3.5: Negative
- 1-2: Very Negative

**Arousal (Energy):**
- 7-9: Very High Energy (Excited, Angry)
- 5.5-7: High Energy (Alert, Tense)
- 3.5-5.5: Medium Energy
- 2-3.5: Low Energy (Calm, Relaxed)
- 1-2: Very Low Energy (Depressed, Bored)

**Sentiment Combinations:**
- **Excited/Happy**: High valence + High arousal
- **Calm/Content**: High valence + Low arousal
- **Angry/Anxious**: Low valence + High arousal
- **Sad/Depressed**: Low valence + Low arousal
- **Tense/Alert**: Medium valence + High arousal
- **Neutral/Relaxed**: Medium valence + Low arousal

---

## 🛑 Stopping the Server

To stop the web server, press **Ctrl+C** in the terminal where it's running.

Or use Python:
```python
# In a new terminal
python -c "import requests; requests.post('http://localhost:5000/shutdown')"
```

---

## 🔧 Troubleshooting

### Can't Access the Application?
- Make sure the server is running (check terminal output)
- Try: http://127.0.0.1:5000 instead of localhost
- Check if port 5000 is already in use

### Models Not Working?
- Check the terminal output for error messages
- Ensure model files exist in `results/` directory
- Try restarting the server

### Slow Performance?
- The first prediction may be slower (model initialization)
- Subsequent predictions should be faster
- Use batch analysis for multiple texts (more efficient)

---

## 📁 Project Files

```
├── app.py                      # Flask backend server
├── templates/
│   └── index.html             # Web interface
├── static/
│   ├── css/style.css          # Styling
│   └── js/main.js             # Frontend logic
├── results/
│   ├── model_proposed.pt      # Proposed model weights
│   ├── baseline_model.pkl     # Baseline model
│   └── vectorizer.pkl         # Text vectorizer
├── example_batch.csv          # Sample batch file
└── WEB_APP_README.md          # Detailed documentation
```

---

## 🎨 Features

✅ Real-time sentiment analysis  
✅ Two different model types  
✅ Visual valence & arousal indicators  
✅ Batch processing with CSV upload  
✅ Export results to CSV  
✅ Dataset statistics dashboard  
✅ Responsive, modern UI  
✅ Example texts for quick testing  

---

## 📚 Next Steps

1. **Test with your own texts**: Try different types of content
2. **Batch analysis**: Upload the `example_batch.csv` file
3. **Compare models**: Test the same text with both models
4. **Explore statistics**: Check the dataset statistics section
5. **Read full docs**: See `WEB_APP_README.md` for detailed information

---

## 💡 Tips

- **Aspect matters**: For the Proposed Model, the aspect significantly affects results
- **Text length**: Shorter, focused texts often give better results
- **Batch processing**: More efficient for analyzing multiple texts
- **Model comparison**: Try both models to see different perspectives

---

## 🎉 Enjoy Your Sentiment Analysis Dashboard!

For detailed documentation, see: **WEB_APP_README.md**

For issues or questions, check the terminal output for error messages.
