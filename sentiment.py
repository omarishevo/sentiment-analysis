# upgraded_sentiment_app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Enhanced Sentiment Analysis", layout="wide")
st.title("😊 Enhanced Sentiment Analysis Dashboard ")

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
            "Not good, it broke immediately",
            "Great value for money, very happy",
            "Awful, never coming back",
            "Excellent product, works perfectly",
            "Poor quality, very bad experience"
        ],
        "sentiment": ["positive", "negative", "positive", "negative", "positive",
                      "negative", "positive", "negative", "positive", "negative"]
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
# 2. Define positive/negative words
# ------------------------
positive_words = ["love", "amazing", "best", "highly recommend", "fantastic", "great", "excellent", "happy", "perfectly"]
negative_words = ["terrible", "worst", "disappointed", "broke", "bad", "poor", "awful", "never"]

# ------------------------
# 3. Sentiment Prediction Functions
# ------------------------
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

def detected_words(text):
    text_lower = str(text).lower()
    pos = [w for w in positive_words if w in text_lower]
    neg = [w for w in negative_words if w in text_lower]
    return pos, neg

# ------------------------
# 4. Apply sentiment prediction to dataset
# ------------------------
df["predicted_sentiment"] = df["text"].apply(predict_sentiment)
df["pos_count"] = df["text"].apply(lambda x: sum(word in x.lower() for word in positive_words))
df["neg_count"] = df["text"].apply(lambda x: sum(word in x.lower() for word in negative_words))

# ------------------------
# 5. Sentiment Distribution Chart
# ------------------------
st.subheader("Sentiment Distribution")
sentiment_counts = df["predicted_sentiment"].value_counts()
st.bar_chart(sentiment_counts)

# ------------------------
# 6. Filter Dataset by Sentiment
# ------------------------
st.subheader("Filter Dataset by Sentiment")
sentiment_filter = st.selectbox("Select Sentiment", ["All", "Positive", "Negative", "Neutral"])
if sentiment_filter != "All":
    st.dataframe(df[df["predicted_sentiment"] == sentiment_filter])
else:
    st.dataframe(df)

# ------------------------
# 7. Top Positive and Negative Reviews
# ------------------------
st.subheader("Top Positive Reviews")
st.dataframe(df.sort_values('pos_count', ascending=False).head(5)[['text', 'predicted_sentiment']])

st.subheader("Top Negative Reviews")
st.dataframe(df.sort_values('neg_count', ascending=False).head(5)[['text', 'predicted_sentiment']])

# ------------------------
# 8. Interactive Prediction
# ------------------------
st.subheader("Try Your Own Text")
user_input = st.text_area("Enter text to analyze sentiment")

if st.button("Predict Sentiment"):
    prediction = predict_sentiment(user_input)
    pos_words, neg_words = detected_words(user_input)
    st.write(f"Predicted Sentiment: **{prediction.upper()}**")
    st.write("Positive words detected:", pos_words)
    st.write("Negative words detected:", neg_words)
