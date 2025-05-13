import nltk
import os

# Get the absolute path to the project directory
project_dir = os.path.dirname(os.path.abspath(__file__))
nltk_data_dir = os.path.join(project_dir, 'nltk_data')

# Create nltk_data directory if it doesn't exist
os.makedirs(nltk_data_dir, exist_ok=True)

# Download the VADER lexicon
print(f"Downloading VADER lexicon to {nltk_data_dir}")
nltk.download('vader_lexicon', download_dir=nltk_data_dir)

print("NLTK data download complete!")
