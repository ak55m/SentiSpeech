// Main application logic
document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const textForm = document.getElementById('text-form');
    const textInput = document.getElementById('text-input');
    const stopBtn = document.getElementById('stop-btn');
    const enhanceEmotions = document.getElementById('enhance-emotions');
    const resultsCard = document.getElementById('results-card');
    const sentimentIcon = document.getElementById('sentiment-icon');
    const sentimentLabel = document.getElementById('sentiment-label');
    const sentimentScore = document.getElementById('sentiment-score');
    const paragraphResults = document.getElementById('paragraph-results');
    const chartPlaceholder = document.getElementById('chart-placeholder');
    const voiceSelect = document.getElementById('voice-select');
    const rateRange = document.getElementById('rate-range');
    
    // Chart.js instance
    let sentimentChart = null;
    
    // Store analysis results
    let analysisResults = null;
    
    // Initialize speech synthesis
    initSpeechSynthesis();
    
    // Event listeners
    textForm.addEventListener('submit', handleSubmit);
    stopBtn.addEventListener('click', stopSpeaking);
    voiceSelect.addEventListener('change', updateVoiceSettings);
    rateRange.addEventListener('input', updateVoiceSettings);
    
    // Handle form submission
    async function handleSubmit(e) {
        e.preventDefault();
        
        const text = textInput.value.trim();
        if (!text) {
            alert('Please enter some text to analyze.');
            return;
        }
        
        try {
            // Show loading state
            textForm.querySelector('button[type="submit"]').disabled = true;
            textForm.querySelector('button[type="submit"]').innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Analyzing...';
            
            // Call API to analyze text
            analysisResults = await analyzeText(text);
            
            // Display results
            displayResults(analysisResults);
            
            // Enable stop button
            stopBtn.disabled = false;
            
            // Start speaking
            speakText(analysisResults);
            
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while analyzing the text. Please try again.');
        } finally {
            // Reset button state
            textForm.querySelector('button[type="submit"]').disabled = false;
            textForm.querySelector('button[type="submit"]').innerHTML = '<i class="fas fa-magic me-2"></i>Analyze & Read';
        }
    }
    
    // Display analysis results
    function displayResults(results) {
        // Show results card
        resultsCard.style.display = 'block';
        
        // Update overall sentiment
        const overall = results.overall;
        updateSentimentUI(overall.sentiment, overall.score);
        
        // Generate paragraph results
        renderParagraphResults(results.paragraphs);
        
        // Create visualization
        createVisualization(results);
        
        // Scroll to results
        resultsCard.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Update sentiment UI elements
    function updateSentimentUI(sentiment, score) {
        // Update icon
        sentimentIcon.innerHTML = getSentimentIcon(sentiment);
        
        // Update label
        sentimentLabel.textContent = capitalize(sentiment);
        sentimentLabel.className = `badge ${getSentimentClass(sentiment)}`;
        
        // Update score bar
        sentimentScore.style.width = `${score * 100}%`;
        sentimentScore.className = `progress-bar ${getSentimentClass(sentiment)}`;
    }
    
    // Get sentiment icon based on sentiment type
    function getSentimentIcon(sentiment) {
        switch (sentiment) {
            case 'positive':
                return '<i class="fas fa-smile"></i>';
            case 'negative':
                return '<i class="fas fa-frown"></i>';
            default:
                return '<i class="fas fa-meh"></i>';
        }
    }
    
    // Get Bootstrap class based on sentiment type
    function getSentimentClass(sentiment) {
        switch (sentiment) {
            case 'positive':
                return 'bg-success';
            case 'negative':
                return 'bg-danger';
            default:
                return 'bg-secondary';
        }
    }
    
    // Render paragraph results
    function renderParagraphResults(paragraphs) {
        paragraphResults.innerHTML = '';
        
        paragraphs.forEach((para, index) => {
            const paraDiv = document.createElement('div');
            paraDiv.className = `paragraph-item ${para.sentiment}`;
            paraDiv.dataset.index = index;
            paraDiv.onclick = () => speakParagraph(index);
            
            paraDiv.innerHTML = `
                <p class="mb-1">${para.text}</p>
                <div class="paragraph-sentiment">
                    <small>${capitalize(para.sentiment)}</small>
                    <div class="progress">
                        <div class="progress-bar ${getSentimentClass(para.sentiment)}" 
                             role="progressbar" 
                             style="width: ${para.score * 100}%"></div>
                    </div>
                    <small>${Math.round(para.score * 100)}%</small>
                </div>
            `;
            
            paragraphResults.appendChild(paraDiv);
        });
    }
    
    // Create visualization chart
    function createVisualization(results) {
        // Hide placeholder
        chartPlaceholder.style.display = 'none';
        
        // Prepare data
        const sentimentCounts = {
            positive: 0,
            neutral: 0,
            negative: 0
        };
        
        results.paragraphs.forEach(para => {
            sentimentCounts[para.sentiment]++;
        });
        
        // Destroy existing chart if exists
        if (sentimentChart) {
            sentimentChart.destroy();
        }
        
        // Create new chart
        const ctx = document.getElementById('sentiment-chart').getContext('2d');
        sentimentChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Positive', 'Neutral', 'Negative'],
                datasets: [{
                    data: [
                        sentimentCounts.positive,
                        sentimentCounts.neutral,
                        sentimentCounts.negative
                    ],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.7)',
                        'rgba(108, 117, 125, 0.7)',
                        'rgba(220, 53, 69, 0.7)'
                    ],
                    borderColor: [
                        'rgba(40, 167, 69, 1)',
                        'rgba(108, 117, 125, 1)',
                        'rgba(220, 53, 69, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: 'Sentiment Distribution'
                    }
                }
            }
        });
    }
    
    // Helper function to capitalize first letter
    function capitalize(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    async function analyzeText(text) {
        try {
            const response = await fetch('https://akeem5.pythonanywhere.com/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }
});
