# Sentiment Analysis Web Application

A modern, interactive web-based UI for testing and analyzing sentiment using machine learning models.

## Features

- 🎯 **Real-time Sentiment Analysis**: Analyze text sentiment instantly
- 📊 **Multiple Models**: Support for both Proposed (Transformer) and Baseline (Logistic Regression) models
- 📈 **Valence & Arousal Scores**: Dimensional sentiment analysis with visual indicators
- 📋 **Batch Processing**: Upload CSV files for bulk analysis
- 💾 **Export Results**: Download analysis results as CSV
- 📊 **Dataset Statistics**: View comprehensive dataset statistics
- 🎨 **Modern UI**: Beautiful, responsive interface with smooth animations

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements_web.txt
```

### 2. Prepare Models

#### Option A: Use Proposed Model (Transformer)
If you have already trained the proposed model:
```bash
# The model should be at: results/model_proposed.pt
# If not, train it first:
python model_proposed.py
```

#### Option B: Use Baseline Model
Train and save the baseline model:
```bash
python save_baseline_model.py
```

**Note**: You need at least one model trained to use the web application.

## Running the Application

### Start the Flask Server

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Access the Web Interface

Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

### Single Text Analysis

1. **Select Model**: Choose between "Proposed Model" or "Baseline Model"
2. **Enter Text**: Type or paste the text you want to analyze
3. **Enter Aspect** (for Proposed Model): Specify the aspect (e.g., "environmental_protection", "restaurant", "laptop")
4. **Click "Analyze Sentiment"**: View results instantly

### Example Texts

The application includes pre-loaded examples. Click any example button to load sample text and aspect.

### Batch Analysis

1. **Prepare CSV File**: Create a CSV with columns:
   - `Text`: The text to analyze (required)
   - `Aspect`: The aspect for analysis (optional, required for Proposed Model)

2. **Upload File**: Click "Choose File" and select your CSV
3. **Process**: Click "Process Batch"
4. **Download Results**: Click "Download Results" to save the analysis

### Understanding Results

#### Proposed Model (Valence & Arousal)
- **Valence**: Measures positivity/negativity (1-9 scale)
  - High (6.5-9): Positive sentiment
  - Low (1-3.5): Negative sentiment
  - Medium (3.5-6.5): Neutral sentiment

- **Arousal**: Measures energy/activation (1-9 scale)
  - High (6.5-9): High energy, excitement
  - Low (1-3.5): Low energy, calm

- **Sentiment Label**: Combined interpretation
  - Excited/Happy: High valence, high arousal
  - Calm/Content: High valence, low arousal
  - Angry/Anxious: Low valence, high arousal
  - Sad/Depressed: Low valence, low arousal
  - Tense/Alert: Medium valence, high arousal
  - Neutral/Relaxed: Medium valence, low arousal

#### Baseline Model (Classification)
- **Prediction**: The predicted aspect/category
- **Confidence**: Model confidence (0-100%)
- **Class Probabilities**: Probability distribution across all classes

## API Endpoints

The application provides REST API endpoints:

### POST /api/analyze
Analyze a single text
```json
{
  "text": "Your text here",
  "aspect": "aspect_name",
  "model": "proposed" or "baseline"
}
```

### POST /api/batch_analyze
Analyze multiple texts
```json
{
  "texts": ["text1", "text2"],
  "aspects": ["aspect1", "aspect2"],
  "model": "proposed" or "baseline"
}
```

### GET /api/model_info
Get information about loaded models

### GET /api/statistics
Get dataset statistics

## Project Structure

```
.
├── app.py                      # Flask application
├── templates/
│   └── index.html             # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css          # Styles
│   └── js/
│       └── main.js            # JavaScript functionality
├── model_proposed.py          # Proposed model definition
├── model_baseline_A.py        # Baseline model
├── preprocess.py              # Text preprocessing
├── save_baseline_model.py     # Script to save baseline model
└── requirements_web.txt       # Python dependencies
```

## Troubleshooting

### Models Not Loading
- Ensure you have trained at least one model
- Check that model files exist in the `results/` directory
- For proposed model: `results/model_proposed.pt`
- For baseline model: `results/baseline_model.pkl` and `results/vectorizer.pkl`

### Port Already in Use
If port 5000 is already in use, modify `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port
```

### CUDA/GPU Issues
The application automatically detects and uses GPU if available. If you encounter CUDA errors:
```python
# In app.py, force CPU usage:
DEVICE = torch.device("cpu")
```

## Development

### Running in Debug Mode
The application runs in debug mode by default, which enables:
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

### Customization
- **Styling**: Edit `static/css/style.css`
- **Functionality**: Edit `static/js/main.js`
- **Layout**: Edit `templates/index.html`
- **Backend Logic**: Edit `app.py`

## Performance Tips

1. **Batch Processing**: Use batch analysis for multiple texts (more efficient)
2. **Model Selection**: Baseline model is faster for simple classification
3. **Text Length**: Shorter texts process faster
4. **GPU Acceleration**: Use GPU for proposed model (if available)

## Security Notes

- The application is designed for local/development use
- For production deployment:
  - Set `debug=False` in `app.py`
  - Use a production WSGI server (e.g., Gunicorn)
  - Add authentication if needed
  - Configure CORS properly

## License

This project is part of the SemEval-2026 Dimensional Stance Analysis task.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the console output for error messages
3. Ensure all dependencies are installed correctly
