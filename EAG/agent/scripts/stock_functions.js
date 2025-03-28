async function getTopStocks() {
    const {alphaVantageKey} = await chrome.storage.sync.get('alphaVantageKey');
    // Implementation similar to Python version but in JavaScript
}

async function getLatestNews(stocks) {
    // Implementation similar to Python version but in JavaScript
}

async function getAnalystRecommendations(stocks) {
    // Implementation similar to Python version but in JavaScript
}

async function analyzeWithGemini(stocks, newsData, analystData) {
    const {geminiKey} = await chrome.storage.sync.get('geminiKey');
    // Implementation using Gemini API
} 