"""
Quick start script for the Sentiment Analysis Web Application
Checks dependencies and models before launching
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    print("=" * 60)
    print("Checking dependencies...")
    print("=" * 60)
    
    required_packages = [
        'flask',
        'flask_cors',
        'torch',
        'pandas',
        'numpy',
        'sklearn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print("\n" + "=" * 60)
        print("Missing packages detected!")
        print("=" * 60)
        print("\nPlease install missing packages:")
        print("pip install -r requirements_web.txt")
        return False
    
    print("\n✓ All dependencies are installed!")
    return True

def check_models():
    """Check if models are available"""
    print("\n" + "=" * 60)
    print("Checking models...")
    print("=" * 60)
    
    models_found = False
    
    # Check proposed model
    if os.path.exists("results/model_proposed.pt"):
        print("✓ Proposed model found (results/model_proposed.pt)")
        models_found = True
    else:
        print("✗ Proposed model NOT found")
        print("  To train: python model_proposed.py")
    
    # Check baseline model
    if os.path.exists("results/baseline_model.pkl") and os.path.exists("results/vectorizer.pkl"):
        print("✓ Baseline model found (results/baseline_model.pkl)")
        models_found = True
    else:
        print("✗ Baseline model NOT found")
        print("  To train: python save_baseline_model.py")
    
    if not models_found:
        print("\n" + "=" * 60)
        print("WARNING: No models found!")
        print("=" * 60)
        print("\nYou need at least one model to use the web application.")
        print("\nOptions:")
        print("1. Train the proposed model: python model_proposed.py")
        print("2. Train the baseline model: python save_baseline_model.py")
        
        response = input("\nDo you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            return False
    
    return True

def check_dataset():
    """Check if dataset is available"""
    print("\n" + "=" * 60)
    print("Checking dataset...")
    print("=" * 60)
    
    if os.path.exists("main/csv/loaded_data.csv"):
        print("✓ Dataset found (main/csv/loaded_data.csv)")
        return True
    else:
        print("⚠ Dataset NOT found (main/csv/loaded_data.csv)")
        print("  Statistics feature will not be available")
        print("  To create: python data_loader.py")
        return True  # Not critical, continue anyway

def start_app():
    """Start the Flask application"""
    print("\n" + "=" * 60)
    print("Starting Sentiment Analysis Web Application...")
    print("=" * 60)
    print("\nThe application will be available at:")
    print("  → http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    try:
        # Import and run the app
        import app
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("Server stopped by user")
        print("=" * 60)
    except Exception as e:
        print(f"\n\nError starting application: {e}")
        print("\nPlease check the error message above and try again.")
        sys.exit(1)

def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("SENTIMENT ANALYSIS WEB APPLICATION")
    print("Quick Start Script")
    print("=" * 60 + "\n")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check models
    if not check_models():
        sys.exit(1)
    
    # Check dataset (optional)
    check_dataset()
    
    # Start the application
    start_app()

if __name__ == "__main__":
    main()
