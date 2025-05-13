"""
Deployment script for Netlify Functions
This file sets up the Netlify function to handle sentiment analysis
"""

import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import warnings

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize NLTK components - updated for newer Python compatibility
def initialize_nltk():
    try:
        nltk.data.find('vader_lexicon')
    except (LookupError, OSError):
        nltk.download('vader_lexicon', quiet=True)

# Initialize
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

def calculate_rate(sentiment_result):
    # Adjust speech rate based on sentiment
    sentiment = sentiment_result['sentiment']
    score = sentiment_result['score']
    
    if sentiment == 'positive':
        return 1.1 + (score * 0.2)  # Slightly faster for positive
    elif sentiment == 'negative':
        return 0.9 - (score * 0.1)  # Slightly slower for negative
    else:
        return 1.0  # Neutral rate

def calculate_pitch(sentiment_result):
    # Adjust pitch based on sentiment
    sentiment = sentiment_result['sentiment']
    score = sentiment_result['score']
    
    if sentiment == 'positive':
        return 1.1 + (score * 0.2)  # Higher pitch for positive
    elif sentiment == 'negative':
        return 0.9 - (score * 0.1)  # Lower pitch for negative
    else:
        return 1.0  # Neutral pitch

def calculate_volume(sentiment_result):
    # Adjust volume based on sentiment
    sentiment = sentiment_result['sentiment']
    score = sentiment_result['score']
    
    if sentiment == 'positive' and score > 0.7:
        return 1.2  # Louder for very positive
    elif sentiment == 'negative' and score > 0.7:
        return 0.9  # Softer for very negative
    else:
        return 1.0  # Neutral volume

def handler(event, context):
    """Netlify Function handler for SentiSpeech."""
    # Parse request body
    try:
        if event['httpMethod'] != 'POST':
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        body = json.loads(event['body'])
        text = body.get('text', '')
        
        # Split into paragraphs
        paragraphs = [p for p in text.split('\n') if p.strip()]
        
        results = []
        for paragraph in paragraphs:
            sentiment_result = analyze_sentiment(paragraph)
            results.append({
                'text': paragraph,
                'sentiment': sentiment_result['sentiment'],
                'score': sentiment_result['score'],
                'speechParams': {
                    'rate': calculate_rate(sentiment_result),
                    'pitch': calculate_pitch(sentiment_result),
                    'volume': calculate_volume(sentiment_result)
                }
            })
        
        response_data = {
            'overall': analyze_sentiment(text),
            'paragraphs': results
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
