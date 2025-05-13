"""
Netlify serverless function for SentiSpeech sentiment analysis
"""

import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import warnings

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize NLTK components
try:
    nltk.data.find('vader_lexicon')
except (LookupError, OSError):
    nltk.download('vader_lexicon', quiet=True)

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Analyze the sentiment of the given text."""
    if not text.strip():
        return {'sentiment': 'neutral', 'score': 0.5}
    
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        sentiment = 'positive'
        score = 0.5 + (compound - 0.05) * 0.5 / 0.95
    elif compound <= -0.05:
        sentiment = 'negative'
        score = 0.5 + (abs(compound) - 0.05) * 0.5 / 0.95
    else:
        sentiment = 'neutral'
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
    """Calculate speech rate based on sentiment."""
    sentiment = sentiment_result['sentiment']
    score = sentiment_result['score']
    
    if sentiment == 'positive':
        return 1.1 + (score * 0.2)  # Slightly faster for positive
    elif sentiment == 'negative':
        return 0.9 - (score * 0.1)  # Slightly slower for negative
    else:
        return 1.0  # Neutral rate

def calculate_pitch(sentiment_result):
    """Calculate speech pitch based on sentiment."""
    sentiment = sentiment_result['sentiment']
    score = sentiment_result['score']
    
    if sentiment == 'positive':
        return 1.1 + (score * 0.2)  # Higher pitch for positive
    elif sentiment == 'negative':
        return 0.9 - (score * 0.1)  # Lower pitch for negative
    else:
        return 1.0  # Neutral pitch

def calculate_volume(sentiment_result):
    """Calculate speech volume based on sentiment."""
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
    try:
        # Check for correct HTTP method
        if event['httpMethod'] != 'POST':
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        # Parse request body
        body = json.loads(event['body'])
        text = body.get('text', '')
        
        # Split into paragraphs
        paragraphs = [p for p in text.split('\n') if p.strip()]
        
        # Process each paragraph
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
        
        # Create response
        response_data = {
            'overall': analyze_sentiment(text),
            'paragraphs': results
        }
        
        # Return success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        # Return error response
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }