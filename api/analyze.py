from http.server import BaseHTTPRequestHandler
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize NLTK
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    logger.info("Downloading vader_lexicon...")
    nltk.download('vader_lexicon')

# Initialize sentiment analyzer
sid = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Analyze sentiment and return normalized scores"""
    scores = sid.polarity_scores(text)
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
        'details': scores
    }

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            text = data.get('text', '')
            logger.info(f"Analyzing text: {text[:100]}...")
            
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
                        'rate': 1.1 if sentiment_result['sentiment'] == 'positive' else 0.9,
                        'pitch': 1.1 if sentiment_result['sentiment'] == 'positive' else 0.9,
                        'volume': 1.2 if sentiment_result['sentiment'] == 'positive' and sentiment_result['score'] > 0.7 else 1.0
                    }
                })
            
            response = {
                'overall': analyze_sentiment(text),
                'paragraphs': results
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode())
            logger.info("Analysis complete")
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 