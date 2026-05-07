// API Base URL
const API_BASE = '';

// Example texts
const examples = {
    1: {
        text: "The new environmental protection policy is absolutely fantastic and will help save our planet for future generations.",
        aspect: "environmental_protection"
    },
    2: {
        text: "The food at this restaurant was terrible and the service was extremely slow.",
        aspect: "restaurant"
    },
    3: {
        text: "This laptop has amazing performance and the battery life is incredible.",
        aspect: "laptop"
    }
};

// Load example text
function loadExample(num) {
    const example = examples[num];
    document.getElementById('textInput').value = example.text;
    document.getElementById('aspectInput').value = example.aspect;
}

// Check model status on page load
async function checkModelStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/model_info`);
        const data = await response.json();
        
        const proposedStatus = document.getElementById('proposedStatus');
        const baselineStatus = document.getElementById('baselineStatus');
        
        if (data.proposed_model) {
            proposedStatus.textContent = '✓ Active';
            proposedStatus.className = 'status-indicator active';
        } else {
            proposedStatus.textContent = '✗ Inactive';
            proposedStatus.className = 'status-indicator inactive';
        }
        
        if (data.baseline_model) {
            baselineStatus.textContent = '✓ Active';
            baselineStatus.className = 'status-indicator active';
        } else {
            baselineStatus.textContent = '✗ Inactive';
            baselineStatus.className = 'status-indicator inactive';
        }
    } catch (error) {
        console.error('Error checking model status:', error);
        showAlert('Failed to check model status', 'error');
    }
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE}/api/statistics`);
        const data = await response.json();
        
        const statsContent = document.getElementById('statsContent');
        
        if (Object.keys(data).length === 0) {
            statsContent.innerHTML = '<p class="info-text">No statistics available</p>';
            return;
        }
        
        let html = '<div class="stat-grid">';
        
        if (data.total_samples) {
            html += `
                <div class="stat-card">
                    <div class="stat-value">${data.total_samples}</div>
                    <div class="stat-label">Total Samples</div>
                </div>
            `;
        }
        
        if (data.avg_text_length) {
            html += `
                <div class="stat-card">
                    <div class="stat-value">${data.avg_text_length.toFixed(1)}</div>
                    <div class="stat-label">Avg. Text Length</div>
                </div>
            `;
        }
        
        html += '</div>';
        
        if (data.label_distribution) {
            html += '<h3>Label Distribution</h3>';
            html += '<table class="results-table"><thead><tr><th>Label</th><th>Count</th></tr></thead><tbody>';
            
            for (const [label, count] of Object.entries(data.label_distribution)) {
                html += `<tr><td>${label}</td><td>${count}</td></tr>`;
            }
            
            html += '</tbody></table>';
        }
        
        statsContent.innerHTML = html;
    } catch (error) {
        console.error('Error loading statistics:', error);
        document.getElementById('statsContent').innerHTML = 
            '<p class="info-text">Failed to load statistics</p>';
    }
}

// Show/hide aspect input based on model selection
document.getElementById('modelSelect').addEventListener('change', function() {
    const aspectGroup = document.getElementById('aspectGroup');
    if (this.value === 'proposed') {
        aspectGroup.style.display = 'block';
    } else {
        aspectGroup.style.display = 'none';
    }
});

// Analyze button click handler
document.getElementById('analyzeBtn').addEventListener('click', async function() {
    const text = document.getElementById('textInput').value.trim();
    const aspect = document.getElementById('aspectInput').value.trim();
    const model = document.getElementById('modelSelect').value;
    
    if (!text) {
        showAlert('Please enter text to analyze', 'error');
        return;
    }
    
    if (model === 'proposed' && !aspect) {
        showAlert('Please enter an aspect for the proposed model', 'error');
        return;
    }
    
    // Show loading state
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
    this.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text, aspect, model })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Analysis failed');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        showAlert(error.message, 'error');
    } finally {
        // Reset button state
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        this.disabled = false;
    }
});

// Display results
function displayResults(data) {
    const resultsCard = document.getElementById('resultsCard');
    const resultsContent = document.getElementById('resultsContent');
    
    let html = '';
    
    // Display input text
    html += `
        <div class="result-item">
            <div class="result-label">Input Text:</div>
            <div class="result-value">${data.text}</div>
        </div>
    `;
    
    if (data.aspect) {
        html += `
            <div class="result-item">
                <div class="result-label">Aspect:</div>
                <div class="result-value">${data.aspect}</div>
            </div>
        `;
    }
    
    html += `
        <div class="result-item">
            <div class="result-label">Model Used:</div>
            <div class="result-value">${data.model}</div>
        </div>
    `;
    
    // Display prediction results
    if (data.prediction.valence !== undefined) {
        // Valence & Arousal results
        html += `
            <div class="result-item">
                <div class="result-label">Sentiment:</div>
                <span class="sentiment-badge ${getSentimentClass(data.prediction.sentiment)}">
                    ${data.prediction.sentiment}
                </span>
            </div>
        `;
        
        html += '<div class="va-scores">';
        
        // Valence
        html += `
            <div class="va-score">
                <div class="va-score-label">Valence</div>
                <div class="va-score-value">${data.prediction.valence.toFixed(2)}</div>
                <div class="va-score-bar">
                    <div class="va-score-fill" style="width: ${(data.prediction.valence / 9) * 100}%"></div>
                </div>
                <small style="color: #6b7280; margin-top: 5px; display: block;">
                    ${data.prediction.valence >= 6.5 ? 'Positive' : data.prediction.valence <= 3.5 ? 'Negative' : 'Neutral'}
                </small>
            </div>
        `;
        
        // Arousal
        html += `
            <div class="va-score">
                <div class="va-score-label">Arousal</div>
                <div class="va-score-value">${data.prediction.arousal.toFixed(2)}</div>
                <div class="va-score-bar">
                    <div class="va-score-fill" style="width: ${(data.prediction.arousal / 9) * 100}%"></div>
                </div>
                <small style="color: #6b7280; margin-top: 5px; display: block;">
                    ${data.prediction.arousal >= 6.5 ? 'High Energy' : 'Low Energy'}
                </small>
            </div>
        `;
        
        html += '</div>';
        
    } else if (data.prediction.prediction !== undefined) {
        // Classification results
        html += `
            <div class="result-item">
                <div class="result-label">Prediction:</div>
                <div class="result-value">${data.prediction.prediction}</div>
            </div>
        `;
        
        html += `
            <div class="result-item">
                <div class="result-label">Confidence:</div>
                <div class="result-value">${(data.prediction.confidence * 100).toFixed(2)}%</div>
                <div class="va-score-bar" style="margin-top: 10px;">
                    <div class="va-score-fill" style="width: ${data.prediction.confidence * 100}%"></div>
                </div>
            </div>
        `;
        
        if (data.prediction.probabilities) {
            html += '<h3>Class Probabilities</h3>';
            html += '<table class="results-table"><thead><tr><th>Class</th><th>Probability</th></tr></thead><tbody>';
            
            for (const [label, prob] of Object.entries(data.prediction.probabilities)) {
                html += `<tr><td>${label}</td><td>${(prob * 100).toFixed(2)}%</td></tr>`;
            }
            
            html += '</tbody></table>';
        }
    }
    
    resultsContent.innerHTML = html;
    resultsCard.style.display = 'block';
    
    // Smooth scroll to results
    resultsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Get sentiment class for styling
function getSentimentClass(sentiment) {
    if (sentiment.includes('Happy') || sentiment.includes('Content') || sentiment.includes('Excited')) {
        return 'sentiment-positive';
    } else if (sentiment.includes('Angry') || sentiment.includes('Sad') || sentiment.includes('Anxious')) {
        return 'sentiment-negative';
    } else {
        return 'sentiment-neutral';
    }
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const mainContent = document.querySelector('.main-content');
    mainContent.insertBefore(alertDiv, mainContent.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Batch analysis
document.getElementById('batchAnalyzeBtn').addEventListener('click', async function() {
    const fileInput = document.getElementById('csvInput');
    const file = fileInput.files[0];
    
    if (!file) {
        showAlert('Please select a CSV file', 'error');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = async function(e) {
        try {
            const csv = e.target.result;
            const lines = csv.split('\n');
            const headers = lines[0].split(',').map(h => h.trim());
            
            const textIndex = headers.indexOf('Text');
            const aspectIndex = headers.indexOf('Aspect');
            
            if (textIndex === -1) {
                showAlert('CSV must contain a "Text" column', 'error');
                return;
            }
            
            const texts = [];
            const aspects = [];
            
            for (let i = 1; i < lines.length; i++) {
                if (lines[i].trim()) {
                    const values = lines[i].split(',');
                    texts.push(values[textIndex]);
                    if (aspectIndex !== -1) {
                        aspects.push(values[aspectIndex]);
                    }
                }
            }
            
            const model = document.getElementById('modelSelect').value;
            
            const response = await fetch(`${API_BASE}/api/batch_analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ texts, aspects, model })
            });
            
            if (!response.ok) {
                throw new Error('Batch analysis failed');
            }
            
            const data = await response.json();
            displayBatchResults(data);
            
        } catch (error) {
            console.error('Error:', error);
            showAlert(error.message, 'error');
        }
    };
    
    reader.readAsText(file);
});

// Display batch results
function displayBatchResults(data) {
    const batchResults = document.getElementById('batchResults');
    const batchResultsContent = document.getElementById('batchResultsContent');
    
    let html = `<p class="info-text">Processed ${data.count} samples</p>`;
    html += '<table class="results-table"><thead><tr><th>Text</th>';
    
    if (data.results[0].aspect) {
        html += '<th>Aspect</th>';
    }
    
    if (data.results[0].prediction.valence !== undefined) {
        html += '<th>Valence</th><th>Arousal</th><th>Sentiment</th>';
    } else {
        html += '<th>Prediction</th><th>Confidence</th>';
    }
    
    html += '</tr></thead><tbody>';
    
    for (const result of data.results) {
        html += '<tr>';
        html += `<td>${result.text.substring(0, 50)}...</td>`;
        
        if (result.aspect) {
            html += `<td>${result.aspect}</td>`;
        }
        
        if (result.prediction.valence !== undefined) {
            html += `<td>${result.prediction.valence.toFixed(2)}</td>`;
            html += `<td>${result.prediction.arousal.toFixed(2)}</td>`;
            html += `<td>${result.prediction.sentiment}</td>`;
        } else {
            html += `<td>${result.prediction.prediction}</td>`;
            html += `<td>${(result.prediction.confidence * 100).toFixed(2)}%</td>`;
        }
        
        html += '</tr>';
    }
    
    html += '</tbody></table>';
    
    batchResultsContent.innerHTML = html;
    batchResults.style.display = 'block';
    
    // Store results for download
    window.batchResultsData = data;
}

// Download batch results
document.getElementById('downloadBtn').addEventListener('click', function() {
    if (!window.batchResultsData) return;
    
    const data = window.batchResultsData;
    let csv = '';
    
    // Headers
    if (data.results[0].aspect) {
        csv += 'Text,Aspect,';
    } else {
        csv += 'Text,';
    }
    
    if (data.results[0].prediction.valence !== undefined) {
        csv += 'Valence,Arousal,Sentiment\n';
    } else {
        csv += 'Prediction,Confidence\n';
    }
    
    // Data
    for (const result of data.results) {
        csv += `"${result.text}",`;
        
        if (result.aspect) {
            csv += `"${result.aspect}",`;
        }
        
        if (result.prediction.valence !== undefined) {
            csv += `${result.prediction.valence},${result.prediction.arousal},"${result.prediction.sentiment}"\n`;
        } else {
            csv += `"${result.prediction.prediction}",${result.prediction.confidence}\n`;
        }
    }
    
    // Download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'sentiment_analysis_results.csv';
    a.click();
    window.URL.revokeObjectURL(url);
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    checkModelStatus();
    loadStatistics();
});
