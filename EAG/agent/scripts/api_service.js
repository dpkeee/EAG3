class StockAPI {
    constructor() {
        this.baseUrl = 'https://www.alphavantage.co/query';
    }

    async getApiKey() {
        const result = await chrome.storage.sync.get(['alphaVantageKey']);
        return result.alphaVantageKey;
    }

    async getTopStocks() {
        const apiKey = await this.getApiKey();
        const response = await fetch(
            `${this.baseUrl}?function=TOP_GAINERS_LOSERS&apikey=${apiKey}`
        );
        const data = await response.json();
        return data.top_gainers || [];
    }

    async getStockNews(symbol) {
        const apiKey = await this.getApiKey();
        const response = await fetch(
            `${this.baseUrl}?function=NEWS_SENTIMENT&symbol=${symbol}&apikey=${apiKey}`
        );
        return await response.json();
    }

    async getAnalystRecommendations(symbol) {
        const apiKey = await this.getApiKey();
        const response = await fetch(
            `${this.baseUrl}?function=OVERVIEW&symbol=${symbol}&apikey=${apiKey}`
        );
        return await response.json();
    }
} 