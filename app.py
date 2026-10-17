import joblib
import pandas as pd
import streamlit as st

from src.features import extract_features

st.set_page_config(
    page_title="Phishing URL Detector",
    page_icon="🛡️",
    layout="centered",
)

st.title("🛡️ Phishing URL Detector")
st.write("Enter a URL to check whether it looks phishing or legitimate.")

model = joblib.load("models/phishing_model.joblib")

url = st.text_input(
    "URL",
    placeholder="https://example.com/login",
)

if st.button("Check URL", type="primary"):
    if not url.strip():
        st.warning("Please enter a URL.")
        st.stop()

    features = pd.DataFrame([extract_features(url)])

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    # Class order:
    # 0 = phishing
    # 1 = legitimate
    phishing_probability = probabilities[0]
    legitimate_probability = probabilities[1]

    st.subheader("Result")

    if prediction == 0:
        st.error(
            f"⚠️ Likely phishing — {phishing_probability:.1%} confidence"
        )
    else:
        st.success(
            f"✅ Likely legitimate — {legitimate_probability:.1%} confidence"
        )

    st.progress(phishing_probability)

    st.caption(
        "This is a machine-learning demo, not a complete security product. "
        "Do not rely on it as your only protection against phishing."
    )

    with st.expander("Show extracted URL features"):
        st.dataframe(features.T, use_container_width=True)