import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Text preprocessing
def preprocess(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return ' '.join(words)

# Train a Naive Bayes sentiment model (placeholder for now)
def train_sentiment_model():
    # Sample data for illustration
    texts = ["Stock is going up", "I'm selling everything", "This is a great buy", "Stock is crashing"]
    labels = [1, 0, 1, 0]  # 1 for positive, 0 for negative

    processed_texts = [preprocess(text) for text in texts]
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(processed_texts)

    model = MultinomialNB()
    model.fit(X, labels)
    
    # Save the model and vectorizer
    joblib.dump(model, "sentiment_model.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")
    print("Sentiment model trained and saved.")

# Analyze sentiment
def analyze_sentiment(text):
    vectorizer = joblib.load("vectorizer.pkl")
    model = joblib.load("sentiment_model.pkl")
    processed_text = preprocess(text)
    vectorized_text = vectorizer.transform([processed_text])
    sentiment = model.predict(vectorized_text)
    return "positive" if sentiment[0] == 1 else "negative"
