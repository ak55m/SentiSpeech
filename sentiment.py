import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import os
import warnings

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize NLTK components - updated for newer Python compatibility
def initialize_nltk():
    try:
        nltk.data.find('vader_lexicon')
    except (LookupError, OSError):
        nltk.download('vader_lexicon', quiet=True)

# Initialize the sentiment analyzer
initialize_nltk()
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text.
    Returns a dictionary with sentiment label and score.
    """
    if not text.strip():
        return {'sentiment': 'neutral', 'score': 0.5}
    
    scores = sia.polarity_scores(text)
    
    # Determine sentiment based on compound score
    compound = scores['compound']
    
    if compound >= 0.05:
        sentiment = 'positive'
        # Normalize score for positive sentiment (0.05 to 1 -> 0.5 to 1)
        score = 0.5 + (compound - 0.05) * 0.5 / 0.95
    elif compound <= -0.05:
        sentiment = 'negative'
        # Normalize score for negative sentiment (-0.05 to -1 -> 0.5 to 1)
        score = 0.5 + (abs(compound) - 0.05) * 0.5 / 0.95
    else:
        sentiment = 'neutral'
        # Normalize score for neutral sentiment (-0.05 to 0.05 -> 0 to 0.5)
        score = 0.5 * (compound + 0.05) / 0.1
    
    return {
        'sentiment': sentiment,
        'score': round(score, 2),
        'details': {
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'compound': scores['compound']
        }
    }

# For more advanced implementations:
# Uncomment if you want to use a transformer model instead
"""
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

# This would normally be in a setup function or done at startup
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def analyze_sentiment_with_transformer(text):
    if not text.strip():
        return {'sentiment': 'neutral', 'score': 0.5}
    
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    
    scores = torch.nn.functional.softmax(outputs.logits, dim=-1)
    scores = scores.numpy()[0]
    
    # DistilBERT model gives negative=0, positive=1
    neg_score = scores[0]
    pos_score = scores[1]
    
    if pos_score > neg_score:
        sentiment = 'positive'
        score = pos_score
    else:
        sentiment = 'negative'
        score = neg_score
    
    # If scores are close, consider it neutral
    if abs(pos_score - neg_score) < 0.3:
        sentiment = 'neutral'
        score = 0.5
    
    return {
        'sentiment': sentiment,
        'score': float(score),
        'details': {
            'positive': float(pos_score),
            'negative': float(neg_score)
        }
    }
"""

# Testing the module
if __name__ == '__main__':
    test_texts = [
        "I love this product! It's amazing and works perfectly.",
        "This is terrible. I'm very disappointed and angry.",
        "The weather today is cloudy with some sunshine."
    ]
    
    for text in test_texts:
        result = analyze_sentiment(text)
        print(f"Text: '{text}'")
        print(f"Sentiment: {result['sentiment']}, Score: {result['score']}")
        print("Details:", result['details'])
        print("-" * 50)
