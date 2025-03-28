document.addEventListener('DOMContentLoaded', function() {
    // Load saved settings
    chrome.storage.sync.get(['alphaVantageKey', 'geminiKey', 'emailRecipient'], function(data) {
        if(data.alphaVantageKey) document.getElementById('alphaVantageKey').value = data.alphaVantageKey;
        if(data.geminiKey) document.getElementById('geminiKey').value = data.geminiKey;
        if(data.emailRecipient) document.getElementById('emailRecipient').value = data.emailRecipient;
    });

    // Save API keys
    document.getElementById('saveKeys').addEventListener('click', function() {
        const alphaVantageKey = document.getElementById('alphaVantageKey').value;
        const geminiKey = document.getElementById('geminiKey').value;
        
        chrome.storage.sync.set({
            alphaVantageKey: alphaVantageKey,
            geminiKey: geminiKey
        }, function() {
            alert('API keys saved!');
        });
    });

    // Save email
    document.getElementById('saveEmail').addEventListener('click', function() {
        const email = document.getElementById('emailRecipient').value;
        chrome.storage.sync.set({
            emailRecipient: email
        }, function() {
            alert('Email saved!');
        });
    });

    // Analyze stocks
    document.getElementById('analyzeStocks').addEventListener('click', async function() {
        const results = document.getElementById('analysisResults');
        const spinner = document.getElementById('loadingSpinner');
        
        spinner.classList.remove('hidden');
        results.innerHTML = '';

        try {
            const analysis = await chrome.runtime.sendMessage({action: 'analyzeStocks'});
            results.innerHTML = analysis;
        } catch (error) {
            results.innerHTML = `Error: ${error.message}`;
        } finally {
            spinner.classList.add('hidden');
        }
    });

    // Schedule analysis
    document.getElementById('scheduleAnalysis').addEventListener('click', function() {
        chrome.runtime.sendMessage({action: 'scheduleAnalysis'});
        alert('Daily analysis scheduled!');
    });
}); 