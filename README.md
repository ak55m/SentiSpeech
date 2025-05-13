# SentiSpeech: Tone-Aware Text Reader

![SentiSpeech Logo](https://github.com/ahritik/SentiSpeech/blob/main/static/assets/logo.svg)

## 🚀 Overview

SentimentSpeech is a powerful web application that analyzes text sentiment and reads content aloud with emotionally appropriate tone. By combining natural language processing with speech synthesis, SentimentSpeech bridges the gap between written text and emotional speech.

**Try it live:** [sentispeech.netlify.app](https://sentispeech.netlify.app) (demo version)

[![GitHub stars](https://img.shields.io/github/stars/ahritik/SentiSpeech?style=social)](https://github.com/ahritik/SentiSpeech)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Key Features

- **Paragraph-Level Sentiment Analysis**: Breaks down emotional tone by paragraph
- **Emotion-Enhanced Speech**: Dynamically adjusts speech parameters based on detected sentiment
- **Interactive Visualization**: See the emotional composition of your content
- **Voice Customization**: Select from available voices and adjust parameters
- **Lightweight & Fast**: Analyzes text and generates speech in real-time
- **Browser-Based Speech**: No external API keys or services required
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🎥 Demo Video

[![SentiSpeech Demo Video]()]()

## 💻 Technology Stack

- **Backend**: Python 3.13, Flask, NLTK
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Data Visualization**: Chart.js
- **Speech Synthesis**: Web Speech API
- **Deployment Options**: 
  - Local (Flask)
  - Netlify (Serverless)
  - Surge (Static frontend)
  - Docker container

## 🌟 Use Cases

- **Content Creators**: Test how written content sounds with emotional context
- **Accessibility**: Enhanced reading experience for visually impaired users
- **Education**: Help language learners understand emotional nuances
- **Public Speaking**: Practice and improve delivery of speeches
- **Content Review**: Quickly assess the emotional tone of articles and blog posts

## 🔧 Installation & Setup

### Local Development

```bash
# Clone the repository
git clone https://github.com/ahritik/SentiSpeech.git
cd SentiSpeech

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Then visit `http://localhost:8080` in your browser.

### Docker Deployment

```bash
# Build the Docker image
docker build -t SentiSpeech .

# Run the container
docker run -p 8080:8080 SentiSpeech
```

Then visit `http://localhost:8080` in your browser.

### Netlify Deployment

1. Fork/clone this repository
2. Connect your GitHub repo to Netlify
3. Netlify will automatically deploy using the `netlify.toml` config

### Surge Deployment (Frontend Only)

```bash
# Generate static site
python generate_static.py

# Deploy with Surge
cd surge_dist
npx surge
```

## 📊 How It Works

1. **Text Analysis**: NLTK's VADER sentiment analyzer evaluates emotional content
2. **Sentiment Mapping**: Emotional scores are mapped to speech parameters
3. **Speech Synthesis**: Web Speech API adjusts tone based on sentiment
4. **Interactive UI**: Results are presented with visualizations and controls

### Sentiment-to-Speech Mapping

| Sentiment | Description | Speech Adjustments |
|-----------|-------------|-------------------|
| 😀 Positive | Happy, enthusiastic, optimistic | Slightly faster rate, higher pitch, increased volume |
| 😐 Neutral | Factual, balanced, informative | Standard rate, pitch, and volume |
| 😟 Negative | Sad, critical, pessimistic | Slightly slower rate, lower pitch, decreased volume |

## 🔬 Technical Innovations

1. **Dynamic Parameter Mapping**: Rather than using fixed values, we create a continuous spectrum of speech adjustments based on sentiment intensity.

2. **Paragraph-Level Analysis**: Most sentiment analyzers work at the document level, but we break down content by paragraph for more nuanced understanding.

3. **Real-Time Synchronization**: UI elements are synchronized with speech playback, highlighting the current paragraph being read.

4. **Hybrid Control System**: Combines automatic sentiment-based adjustments with manual user controls for customization.

## 📈 Performance

- **Analysis Speed**: Text analysis completes in under 300ms for typical paragraphs
- **Browser Support**: Works in Chrome, Edge, Firefox, and Safari
- **Mobile Compatibility**: Responsive design works on all modern smartphones
- **Offline Capability**: Static version can function without an internet connection

## 🧪 User Testing Results

SentimentSpeech has been tested with 5 diverse users:

- Content creators found it helpful for proofreading emotional tone
- Educators appreciated the paragraph-specific reading for teaching
- Non-native English speakers used it to understand emotional contexts
- Technical writers used it to check documentation tone
- Marketing professionals used it to review advertising copy

Common feedback included praise for the paragraph-level analysis and the intuitive visualization of sentiment distribution.

## 💡 Future Improvements

- **Enhanced Emotional Range**: Expand beyond positive/negative to include specific emotions (fear, joy, anger)
- **Multi-language Support**: Add sentiment analysis for languages beyond English
- **Audio Export**: Save analyzed text as MP3 files with emotional inflection
- **Customizable Emotional Mappings**: Allow users to define their own emotion-to-speech parameters
- **Document Upload**: Direct analysis of PDF, DOCX, and other document formats

## 📊 Technical Challenges

SentimentSpeech overcomes several technical challenges:

1. **Browser Speech Limitations**: Working around cross-browser differences in the Web Speech API
2. **Sentiment Granularity**: Balancing between document and sentence-level sentiment
3. **Parameter Tuning**: Finding the right degree of speech modification that sounds natural
4. **State Management**: Coordinating the analysis, visualization, and speech components

## 💰 Monetization Potential

- **SaaS API**: Offering the service as an API for content platforms
- **Premium Features**: Advanced analytics, audio export, additional voices
- **Enterprise Solution**: Custom integration for content management systems
- **Accessibility Tool**: Licensing for education and accessibility applications

## 📋 Project Structure

```
SentiSpeech/
├── app.py                  # Flask application
├── sentiment.py            # Sentiment analysis module
├── static/                 # Frontend assets
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── app.js         # Main application logic
│   │   └── speech.js      # Speech synthesis
│   └── assets/
│       └── logo.svg
├── templates/
│   └── index.html         # Main page template
├── netlify/
│   └── functions/         # Serverless functions
│       └── analyze.py
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container definition
├── netlify.toml           # Netlify configuration
├── generate_static.py     # Static site generator
├── REPORT.md              # Detailed project report
└── README.md              # This file
```

## 👥 Contributors

- Hritik Arasu - Project Lead
- Ardahan Dogru - Backend Developer
- Akeem Mohammed - Frontend Developer

