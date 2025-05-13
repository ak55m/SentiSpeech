from flask import Flask, render_template, request, jsonify
from sentiment import analyze_sentiment
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')
    
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
    
    return jsonify({
        'overall': analyze_sentiment(text),
        'paragraphs': results
    })

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

# This is the entry point for Vercel
app = app

if __name__ == '__main__':
    print("SentiSpeech server is starting...")
    print("Navigate to http://localhost:8080 to use the application")
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
