# sentiment_app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Minimal Sentiment Analysis", layout="wide")
st.title("😊 Minimal Sentiment Analysis ")

# ------------------------
# 1. Load or generate dataset
# ------------------------
def generate_sample_data():
    data = {
        "text": [
            "I love this product, amazing quality!",
            "Terrible experience, very disappointed",
            "Best purchase ever, highly recommend",
            "Worst service, will never buy again",
            "Absolutely fantastic, five stars",
            "Not good, it broke immediately"
        ],
        "sentiment": ["positive", "negative", "positive", "negative", "positive", "negative"]
    }
    return pd.DataFrame(data)

uploaded_file = st.file_uploader("Upload a CSV file (optional)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = generate_sample_data()

st.subheader("Sample Dataset")
st.dataframe(df)

# ------------------------
# 2. Simple rule-based sentiment analysis
# ------------------------
positive_words = ["love", "amazing", "best", "highly recommend", "fantastic", "great", "excellent"]
negative_words = ["terrible", "worst", "disappointed", "broke", "bad", "poor", "awful"]

def predict_sentiment(text):
    text_lower = str(text).lower()
    pos_count = sum(word in text_lower for word in positive_words)
    neg_count = sum(word in text_lower for word in negative_words)
    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    else:
        return "neutral"

df["predicted_sentiment"] = df["text"].apply(predict_sentiment)

st.subheader("Predicted Sentiment on Dataset")
st.dataframe(df)

# ------------------------
# 3. Interactive sentiment prediction
# ------------------------
st.subheader("Try Your Own Text")
user_input = st.text_area("Enter text to analyze sentiment")

if st.button("Predict Sentiment"):
    prediction = predict_sentiment(user_input)
    st.write(f"Predicted Sentiment: **{prediction.upper()}**")
