// Handle scheduled tasks and API calls
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'analyzeStocks') {
        performAnalysis().then(sendResponse);
        return true;
    } else if (request.action === 'scheduleAnalysis') {
        scheduleAnalysis();
    }
});

async function performAnalysis() {
    try {
        const stocks = await getTopStocks();
        const [newsData, analystData] = await Promise.all([
            getLatestNews(stocks),
            getAnalystRecommendations(stocks)
        ]);
        
        const analysis = await analyzeWithGemini(stocks, newsData, analystData);
        await sendEmailReport(analysis);
        
        return analysis;
    } catch (error) {
        console.error('Analysis error:', error);
        return `Error: ${error.message}`;
    }
}

function scheduleAnalysis() {
    chrome.alarms.create('dailyAnalysis', {
        periodInMinutes: 1440 // 24 hours
    });
}

chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === 'dailyAnalysis') {
        performAnalysis();
    }
}); 