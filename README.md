# Sentiment Analysis Dashboard

A professional, AI-powered web application for analyzing text sentiment using advanced machine learning models.

## 🌟 Features

- **Real-time Sentiment Analysis**: Instant analysis of text sentiment
- **Dual Model Support**: 
  - Proposed Model: Transformer-based Valence & Arousal scoring
  - Baseline Model: Logistic Regression classification
- **Batch Processing**: Upload CSV files for bulk analysis
- **Modern UI**: Professional dark mode interface with animated backgrounds
- **Export Results**: Download analysis results as CSV
- **Dataset Statistics**: View comprehensive dataset insights

## 🚀 Live Demo

**[View Live Application](https://your-app.onrender.com)** *(Update after deployment)*

## 📸 Screenshots

*Add screenshots of your application here*

## 🛠️ Technologies

- **Backend**: Flask, Python 3.12
- **ML Models**: PyTorch, Scikit-learn
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Gunicorn, Render
- **UI**: Font Awesome, Custom CSS

## 📋 Local Setup

### Prerequisites

- Python 3.12+
- pip
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/sentiment-analysis-dashboard.git
cd sentiment-analysis-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements_web.txt
```

3. **Train models** (if not already trained)
```bash
python save_baseline_model.py
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
```
http://localhost:5000
```

## 🌐 Deployment

### Deploy to Render (Recommended)

Follow the detailed guide: [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

**Quick Steps:**
1. Push code to GitHub
2. Connect repository to Render
3. Deploy with one click
4. Your app is live!

### Other Platforms

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for:
- Heroku
- Railway
- Google Cloud Run
- AWS EC2
- Docker

## 📖 Usage

### Single Text Analysis

1. Select your model (Proposed or Baseline)
2. Enter text to analyze
3. Add aspect (for Proposed Model)
4. Click "Analyze Sentiment"
5. View results with scores and visualizations

### Batch Analysis

1. Prepare CSV with `Text` and `Aspect` columns
2. Upload file
3. Click "Process Batch"
4. Download results

### Example CSV Format

```csv
Text,Aspect
"The new policy is excellent.",environmental_protection
"Food was terrible.",restaurant
```

## 🎨 UI Features

- **Dark Mode**: Professional dark theme
- **Animated Background**: Smooth gradient orbs
- **Glassmorphism**: Modern card designs
- **Responsive**: Works on all devices
- **Icons**: Professional Font Awesome icons
- **Smooth Animations**: Polished interactions

## 📊 Model Information

### Proposed Model
- Architecture: Transformer Encoder
- Output: Valence (1-9) & Arousal (1-9)
- Use Case: Dimensional sentiment analysis

### Baseline Model
- Algorithm: Logistic Regression with TF-IDF
- Output: Category classification
- Use Case: Aspect-based classification

## 🔧 Configuration

### Environment Variables

```bash
PORT=5000                    # Server port
FLASK_ENV=production        # Environment mode
PYTHON_VERSION=3.12.0       # Python version
```

### Production Settings

Edit `gunicorn_config.py` for:
- Worker processes
- Timeout settings
- Logging configuration

## 📁 Project Structure

```
sentiment-analysis-dashboard/
├── app.py                      # Main Flask application
├── templates/
│   └── index.html             # Web interface
├── static/
│   ├── css/style.css          # Styles
│   └── js/main.js             # Frontend logic
├── results/
│   ├── model_proposed.pt      # Trained model
│   ├── baseline_model.pkl     # Baseline model
│   └── vectorizer.pkl         # Text vectorizer
├── requirements_web.txt       # Dependencies
├── Procfile                   # Deployment config
├── gunicorn_config.py         # Server config
└── README.md                  # This file
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- Email: your.email@example.com

## 🙏 Acknowledgments

- SemEval-2026 Dimensional Stance Analysis Task
- Flask and PyTorch communities
- Font Awesome for icons
- Render for hosting

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Review application logs

## 🔄 Updates

### Version 1.0.0 (Current)
- Initial release
- Dual model support
- Professional dark mode UI
- Batch processing
- CSV export

---

**Made with ❤️ and Python**