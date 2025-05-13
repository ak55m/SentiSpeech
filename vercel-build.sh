#!/bin/bash
set -e  # Exit on error

echo "Starting build process..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Download NLTK data
echo "Downloading NLTK data..."
python -m nltk.downloader vader_lexicon

# Verify NLTK data
echo "Verifying NLTK data..."
python -c "import nltk; nltk.data.find('vader_lexicon')"

echo "Build completed successfully!" 