import sys
import joblib
import pandas as pd

from src.features import extract_features

model = joblib.load("models/phishing_model.joblib")

url = sys.argv[1] if len(sys.argv) > 1 else input("Enter a URL: ")

features = pd.DataFrame([extract_features(url)])

prediction = model.predict(features)[0]
probabilities = model.predict_proba(features)[0]

# Class order:
# 0 = phishing
# 1 = legitimate
phishing_probability = probabilities[0]
legitimate_probability = probabilities[1]

print("\nURL:", url)

if prediction == 0:
    print(f"⚠️ Likely phishing — {phishing_probability:.1%} confidence")
else:
    print(f"✅ Likely legitimate — {legitimate_probability:.1%} confidence")

print("\nExtracted features:")
print(features.T)