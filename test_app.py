from sentiment import analyze_sentiment
from flask import Flask, request, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test sentiment analysis
test_text = "I love this product! It's amazing and works perfectly."
logger.info("Testing sentiment analysis...")
result = analyze_sentiment(test_text)
logger.info(f"Sentiment result: {result}")

# Test Flask app
app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test_analyze():
    try:
        data = request.get_json()
        text = data.get('text', '')
        result = analyze_sentiment(text)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in test_analyze: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting test server...")
    app.run(port=8080, debug=True) 