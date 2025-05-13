#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python download_nltk.py

# Create a symlink to ensure NLTK can find the data
mkdir -p /tmp/nltk_data
ln -s /vercel/path0/nltk_data/* /tmp/nltk_data/

echo "Build completed successfully!" 