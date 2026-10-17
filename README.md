# Phishing URL Detector

A small machine-learning project that predicts whether a URL is likely phishing or legitimate.

## Features

- Extracts URL-based security features
- Trains a Random Forest classifier
- Shows accuracy, precision, recall, and F1-score
- Includes a simple Streamlit web UI
- Saves the trained model with joblib

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Train

```bash
python clean_data.py
python train.py
```

## Run the app

```bash
streamlit run app.py
```

## Important

This project is for learning and demonstration only. It should not be used as a complete phishing-protection solution.
