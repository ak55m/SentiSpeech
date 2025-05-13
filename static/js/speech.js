// Speech synthesis functionality
let synth = null;
let currentUtterance = null;
let speechQueue = [];
let currentParagraphIndex = -1;

// Initialize speech synthesis
function initSpeechSynthesis() {
    synth = window.speechSynthesis;
    
    // Populate voice selector
    setTimeout(loadVoices, 100);
    
    // Some browsers need a listener for voiceschanged
    if (synth.onvoiceschanged !== undefined) {
        synth.onvoiceschanged = loadVoices;
    }
}

// Load available voices
function loadVoices() {
    const voiceSelect = document.getElementById('voice-select');
    voiceSelect.innerHTML = '';
    
    const voices = synth.getVoices();
    
    // Filter for English voices first
    const englishVoices = voices.filter(voice => /en(-|_)/.test(voice.lang));
    const otherVoices = voices.filter(voice => !/en(-|_)/.test(voice.lang));
    
    // Sort voices
    const sortedVoices = [...englishVoices, ...otherVoices];
    
    // Add options to select
    sortedVoices.forEach(voice => {
        const option = document.createElement('option');
        option.textContent = `${voice.name} (${voice.lang})`;
        option.setAttribute('data-name', voice.name);
        option.setAttribute('data-lang', voice.lang);
        voiceSelect.appendChild(option);
    });
    
    // Try to select a good default voice
    const preferredVoices = [
        'Google US English',
        'Microsoft David',
        'Microsoft Zira',
        'Daniel',
        'Samantha'
    ];
    
    // Find the first preferred voice that exists
    for (const preferredVoice of preferredVoices) {
        const option = Array.from(voiceSelect.options).find(
            opt => opt.getAttribute('data-name').includes(preferredVoice)
        );
        
        if (option) {
            voiceSelect.value = option.value;
            break;
        }
    }
    
    // If no preferred voice found, just use the first one
    if (voiceSelect.value === '') {
        voiceSelect.selectedIndex = 0;
    }
}

// Update voice settings
function updateVoiceSettings() {
    // If currently speaking, update the utterance
    if (currentUtterance && synth.speaking) {
        // We can't modify a running utterance, so we need to stop and restart
        const currentText = currentUtterance.text;
        const currentIndex = currentParagraphIndex;
        
        stopSpeaking();
        
        // Speak the text again with new settings
        if (currentIndex >= 0) {
            speakParagraph(currentIndex);
        }
    }
}

// Speak the analyzed text
function speakText(results) {
    // Clear any previous speech
    stopSpeaking();
    
    // Create a queue of paragraphs to speak
    speechQueue = results.paragraphs.map((para, index) => ({
        text: para.text,
        sentiment: para.sentiment,
        score: para.score,
        speechParams: para.speechParams,
        index: index
    }));
    
    // Start speaking
    speakNextInQueue();
}

// Speak a specific paragraph
function speakParagraph(index) {
    // Clear any current speech
    stopSpeaking();
    
    // Check if we have analysis results
    if (!window.analysisResults || !window.analysisResults.paragraphs) {
        return;
    }
    
    const para = window.analysisResults.paragraphs[index];
    
    // Add this paragraph to the queue
    speechQueue = [{
        text: para.text,
        sentiment: para.sentiment,
        score: para.score,
        speechParams: para.speechParams,
        index: index
    }];
    
    // Start speaking
    speakNextInQueue();
}

// Speak the next item in the queue
function speakNextInQueue() {
    if (speechQueue.length === 0 || synth.speaking) {
        return;
    }
    
    const item = speechQueue.shift();
    currentParagraphIndex = item.index;
    
    // Create utterance
    const utterance = new SpeechSynthesisUtterance(item.text);
    
    // Set voice
    const voiceSelect = document.getElementById('voice-select');
    const selectedOption = voiceSelect.selectedOptions[0];
    const voices = synth.getVoices();
    
    if (selectedOption) {
        const voiceName = selectedOption.getAttribute('data-name');
        const voice = voices.find(v => v.name === voiceName);
        if (voice) {
            utterance.voice = voice;
        }
    }
    
    // Set base rate from user control
    const rateRange = document.getElementById('rate-range');
    utterance.rate = parseFloat(rateRange.value);
    
    // Apply emotion enhancement if enabled
    const enhanceEmotions = document.getElementById('enhance-emotions');
    if (enhanceEmotions.checked) {
        // Apply sentiment-specific parameters
        applyEmotionToUtterance(utterance, item.sentiment, item.score, item.speechParams);
    }
    
    // Set event handlers
    utterance.onstart = () => highlightCurrentParagraph(item.index, true);
    utterance.onend = () => {
        highlightCurrentParagraph(item.index, false);
        currentUtterance = null;
        currentParagraphIndex = -1;
        
        // Enable stop button only if there's more to speak
        document.getElementById('stop-btn').disabled = speechQueue.length === 0;
        
        // Speak next item if any
        setTimeout(speakNextInQueue, 250);
    };
    
    // Store current utterance
    currentUtterance = utterance;
    
    // Speak
    synth.speak(utterance);
}

// Apply emotional parameters to utterance
function applyEmotionToUtterance(utterance, sentiment, score, speechParams) {
    // Basic adjustments already calculated by the backend
    if (speechParams) {
        utterance.rate *= speechParams.rate;
        utterance.pitch = speechParams.pitch;
        utterance.volume = speechParams.volume;
    } else {
        // Fallback if backend didn't provide parameters
        switch (sentiment) {
            case 'positive':
                utterance.rate *= 1.1 + (score * 0.2); // Faster for positive
                utterance.pitch = 1.1 + (score * 0.3); // Higher pitch for positive
                break;
                
            case 'negative':
                utterance.rate *= 0.9 - (score * 0.1); // Slower for negative
                utterance.pitch = 0.9 - (score * 0.2); // Lower pitch for negative
                break;
                
            default: // neutral
                utterance.pitch = 1.0;
                // Rate is already set from user input
        }
    }
    
    // Ensure parameters are within reasonable ranges
    utterance.rate = Math.max(0.5, Math.min(2, utterance.rate));
    utterance.pitch = Math.max(0.5, Math.min(2, utterance.pitch));
    utterance.volume = Math.max(0.5, Math.min(1, utterance.volume || 1));
}

// Highlight the paragraph currently being spoken
function highlightCurrentParagraph(index, isActive) {
    const paragraphs = document.querySelectorAll('.paragraph-item');
    
    // Remove highlighting from all paragraphs
    paragraphs.forEach(p => p.classList.remove('is-speaking'));
    
    // Add highlighting to current paragraph if active
    if (isActive) {
        const currentPara = document.querySelector(`.paragraph-item[data-index="${index}"]`);
        if (currentPara) {
            currentPara.classList.add('is-speaking');
            currentPara.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
}

// Stop speaking
function stopSpeaking() {
    synth.cancel();
    currentUtterance = null;
    speechQueue = [];
    currentParagraphIndex = -1;
    
    // Disable stop button
    document.getElementById('stop-btn').disabled = true;
    
    // Remove highlights
    const paragraphs = document.querySelectorAll('.paragraph-item');
    paragraphs.forEach(p => p.classList.remove('is-speaking'));
}
