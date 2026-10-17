import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from sklearn.model_selection import train_test_split

from src.features import extract_features

df = pd.read_csv("data/clean_phishing_urls.csv")

X = pd.json_normalize(df["url"].apply(extract_features))
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

# Label order:
# 0 = phishing
# 1 = legitimate
report = classification_report(
    y_test,
    y_pred,
    target_names=["Phishing", "Legitimate"],
)

print(f"Accuracy: {accuracy:.4f}")
print(report)

joblib.dump(model, "models/phishing_model.joblib")

cm = confusion_matrix(y_test, y_pred)

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Phishing", "Legitimate"],
)

display.plot()
plt.title("Phishing URL Detector")
plt.savefig("confusion_matrix.png")