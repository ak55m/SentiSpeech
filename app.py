from flask import Flask, render_template, request, jsonify
from sentiment import analyze_sentiment
import os
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    try:
        logger.info("Serving index page")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving index: {str(e)}")
        return str(e), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        logger.info("Received analyze request")
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({"error": "No JSON data received"}), 400
            
        text = data.get('text', '')
        logger.info(f"Analyzing text: {text[:100]}...")  # Log first 100 chars
        
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
        
        logger.info(f"Analysis complete. Results: {results}")
        return jsonify({
            'overall': analyze_sentiment(text),
            'paragraphs': results
        })
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

def calculate_rate(sentiment_result):
    try:
        sentiment = sentiment_result['sentiment']
        score = sentiment_result['score']
        
        if sentiment == 'positive':
            return 1.1 + (score * 0.2)
        elif sentiment == 'negative':
            return 0.9 - (score * 0.1)
        else:
            return 1.0
    except Exception as e:
        logger.error(f"Error calculating rate: {str(e)}")
        return 1.0

def calculate_pitch(sentiment_result):
    try:
        sentiment = sentiment_result['sentiment']
        score = sentiment_result['score']
        
        if sentiment == 'positive':
            return 1.1 + (score * 0.2)
        elif sentiment == 'negative':
            return 0.9 - (score * 0.1)
        else:
            return 1.0
    except Exception as e:
        logger.error(f"Error calculating pitch: {str(e)}")
        return 1.0

def calculate_volume(sentiment_result):
    try:
        sentiment = sentiment_result['sentiment']
        score = sentiment_result['score']
        
        if sentiment == 'positive' and score > 0.7:
            return 1.2
        elif sentiment == 'negative' and score > 0.7:
            return 0.9
        else:
            return 1.0
    except Exception as e:
        logger.error(f"Error calculating volume: {str(e)}")
        return 1.0

# This is the entry point for Vercel
app = app

if __name__ == '__main__':
    print("SentiSpeech server is starting...")
    print("Navigate to http://localhost:8080 to use the application")
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
