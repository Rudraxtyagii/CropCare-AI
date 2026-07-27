document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    
    const uploadPanel = document.getElementById('upload-panel');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeImgBtn = document.getElementById('remove-img-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    
    const valError = document.getElementById('validation-error');
    const valErrorText = document.getElementById('error-text');
    
    const loadingState = document.getElementById('loading-state');
    const resultSection = document.getElementById('result-section');
    const newAnalysisBtn = document.getElementById('new-analysis-btn');
    
    // Result Elements
    const resPlantName = document.getElementById('res-plant-name');
    const resDiseaseName = document.getElementById('res-disease-name');
    const resConfBadge = document.getElementById('res-confidence-badge');
    const resConfBar = document.getElementById('res-confidence-bar');
    const resConfPercent = document.getElementById('res-confidence-percent');
    const resDescription = document.getElementById('res-description');
    const resCauses = document.getElementById('res-causes');
    const resTreatment = document.getElementById('res-treatment');
    const resPrevention = document.getElementById('res-prevention');
    const mockWarning = document.getElementById('mock-warning');

    // Stats & History Elements
    const statTotal = document.getElementById('stat-total');
    const statAvgConf = document.getElementById('stat-avg-conf');
    const statFrequent = document.getElementById('stat-frequent');
    const statLastTime = document.getElementById('stat-last-time');
    const historyList = document.getElementById('history-list');
    const clearHistoryBtn = document.getElementById('clear-history-btn');

    let currentFile = null;
    const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

    // Initialize Dashboard
    updateDashboard();

    // -- File Upload Logic --
    browseBtn.addEventListener('click', (e) => {
        e.preventDefault();
        fileInput.click();
    });

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) { e.preventDefault(); e.stopPropagation(); }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('drag-active'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('drag-active'), false);
    });

    dropZone.addEventListener('drop', (e) => {
        handleFiles(e.dataTransfer.files);
    });

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        valError.classList.add('hidden');
        if (files.length > 0) {
            const file = files[0];
            
            // Validate Type
            if (!file.type.startsWith('image/') || !(file.type.includes('jpeg') || file.type.includes('png') || file.type.includes('jpg'))) {
                showError("Invalid file type. Please upload a JPG or PNG image.");
                return;
            }
            
            // Validate Size
            if (file.size > MAX_FILE_SIZE) {
                showError("File is too large. Maximum size is 5MB.");
                return;
            }

            currentFile = file;
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                dropZone.classList.add('hidden');
                previewContainer.classList.remove('hidden');
            }
            reader.readAsDataURL(file);
        }
    }

    function showError(msg) {
        valErrorText.textContent = msg;
        valError.classList.remove('hidden');
        currentFile = null;
        fileInput.value = '';
    }

    removeImgBtn.addEventListener('click', () => {
        resetUpload();
    });

    newAnalysisBtn.addEventListener('click', () => {
        resultSection.classList.add('hidden');
        resetUpload();
    });

    function resetUpload() {
        currentFile = null;
        fileInput.value = '';
        imagePreview.src = '#';
        previewContainer.classList.add('hidden');
        dropZone.classList.remove('hidden');
        uploadPanel.classList.remove('hidden');
        valError.classList.add('hidden');
        resConfBar.style.width = '0%'; // reset bar
    }

    // -- Analysis Logic --
    analyzeBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        // UI transitions
        uploadPanel.classList.add('hidden');
        loadingState.classList.remove('hidden');

        const formData = new FormData();
        formData.append('file', currentFile);

        try {
            const response = await fetch('http://localhost:8000/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Analysis failed. Server error.');
            }

            const data = await response.json();
            
            if (data.success) {
                displayResults(data.prediction);
                saveToHistory(data.prediction, imagePreview.src);
            }

        } catch (error) {
            console.error('API Error:', error);
            alert(`Error: ${error.message}`);
            loadingState.classList.add('hidden');
            uploadPanel.classList.remove('hidden');
        }
    });

    function displayResults(prediction) {
        loadingState.classList.add('hidden');
        resultSection.classList.remove('hidden');

        resPlantName.textContent = prediction.plant;
        resDiseaseName.textContent = prediction.disease;
        
        // Confidence
        resConfPercent.textContent = `${prediction.confidence}%`;
        
        // Animate progress bar (delay for transition effect)
        setTimeout(() => {
            resConfBar.style.width = `${prediction.confidence}%`;
        }, 100);

        // Badge styling
        resConfBadge.textContent = prediction.confidence_level;
        resConfBadge.className = `badge ${prediction.confidence_level.toLowerCase()}`;
        
        // Mock warning
        if (prediction.is_mock) mockWarning.classList.remove('hidden');
        else mockWarning.classList.add('hidden');

        // Rich Info
        resDescription.textContent = prediction.description;
        populateList(resCauses, prediction.causes);
        populateList(resTreatment, prediction.treatment);
        populateList(resPrevention, prediction.prevention);
    }

    function populateList(element, items) {
        element.innerHTML = '';
        if (!items || items.length === 0 || items[0] === 'N/A') {
            element.innerHTML = '<li>Information not available.</li>';
            return;
        }
        items.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            element.appendChild(li);
        });
    }

    // -- History & Stats Logic --
    function saveToHistory(prediction, imgSrc) {
        let history = JSON.parse(localStorage.getItem('cropcare_history')) || [];
        const record = {
            id: Date.now(),
            disease: prediction.disease,
            confidence: prediction.confidence,
            img: imgSrc,
            timestamp: new Date().toISOString()
        };
        history.unshift(record); // Add to beginning
        
        // Keep only last 50 to prevent huge local storage
        if (history.length > 50) history = history.slice(0, 50);
        
        localStorage.setItem('cropcare_history', JSON.stringify(history));
        updateDashboard();
    }

    function updateDashboard() {
        const history = JSON.parse(localStorage.getItem('cropcare_history')) || [];
        
        // Render History List
        historyList.innerHTML = '';
        if (history.length === 0) {
            historyList.innerHTML = '<div class="empty-state">No predictions yet.</div>';
        } else {
            history.forEach(item => {
                const date = new Date(item.timestamp).toLocaleDateString();
                const div = document.createElement('div');
                div.className = 'history-item';
                div.innerHTML = `
                    <img src="${item.img}" class="hist-thumb" alt="thumb">
                    <div class="hist-info">
                        <div class="hist-disease">${item.disease}</div>
                        <div class="hist-meta">
                            <span>${item.confidence}%</span>
                            <span>${date}</span>
                        </div>
                    </div>
                `;
                historyList.appendChild(div);
            });
        }

        // Calculate Stats
        statTotal.textContent = history.length;
        
        if (history.length > 0) {
            const sumConf = history.reduce((acc, curr) => acc + curr.confidence, 0);
            statAvgConf.textContent = (sumConf / history.length).toFixed(1) + '%';
            
            // Last time
            const lastDate = new Date(history[0].timestamp);
            statLastTime.textContent = lastDate.toLocaleDateString() + ' ' + lastDate.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            // Most frequent
            const counts = {};
            let maxDisease = history[0].disease;
            let maxCount = 0;
            history.forEach(item => {
                counts[item.disease] = (counts[item.disease] || 0) + 1;
                if (counts[item.disease] > maxCount) {
                    maxCount = counts[item.disease];
                    maxDisease = item.disease;
                }
            });
            statFrequent.textContent = maxDisease;
        } else {
            statAvgConf.textContent = '0%';
            statLastTime.textContent = 'Never';
            statFrequent.textContent = '-';
        }
    }

    clearHistoryBtn.addEventListener('click', () => {
        if (confirm("Clear all prediction history?")) {
            localStorage.removeItem('cropcare_history');
            updateDashboard();
        }
    });
});
