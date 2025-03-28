import requests
from typing import List, Dict
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def get_top_stocks(limit: int = 5) -> List[str]:
    """
    Get top performing stocks using Alpha Vantage API.
    
    Args:
        limit (int): Number of top stocks to return (default: 5)
        
    Returns:
        List[str]: List of top stock tickers
    """
    try:
        # Alpha Vantage API key from environment variables
        ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
        
        if not ALPHA_VANTAGE_API_KEY:
            print("Alpha Vantage API key not found in environment variables")
            return get_default_stocks()
        
        url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={ALPHA_VANTAGE_API_KEY}'
        
        print("Fetching top stocks from Alpha Vantage...")
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        top_gainers = data.get('top_gainers', [])
        
        if top_gainers:
            sorted_gainers = sorted(
                top_gainers,
                key=lambda x: float(x['change_percentage'].strip('%')),
                reverse=True
            )
            
            stocks = [stock['ticker'] for stock in sorted_gainers[:limit]]
            print(f"\nTop {limit} performing stocks: {stocks}")
            
            # Add LLM analysis for top stocks
            analysis_prompt = f"""
            Analyze these top performing stocks: {stocks}
            Explain in 2-3 sentences why these stocks might be trending today.
            """
            analysis = model.generate_content(contents=analysis_prompt)
            print("\nMarket Analysis:")
            print(analysis.text)
            
            return stocks
        else:
            print("No data received from Alpha Vantage, using default stocks...")
            return get_default_stocks()
            
    except Exception as e:
        print(f"Error getting top stocks from Alpha Vantage: {str(e)}")
        return get_default_stocks()

def get_default_stocks() -> List[str]:
    """
    Return default major stocks if API method fails
    """
    default_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
    print(f"\nUsing default stocks: {default_stocks}")
    return default_stocks

def get_latest_news(stocks: List[str], items_per_stock: int = 3) -> Dict[str, List[Dict]]:
    """
    Get latest news for a list of stocks using Alpha Vantage News API.
    
    Args:
        stocks (List[str]): List of stock tickers
        items_per_stock (int): Number of news items per stock (default: 3)
        
    Returns:
        Dict[str, List[Dict]]: Dictionary with stock tickers as keys and news lists as values
    """
    try:
        ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
        
        if not ALPHA_VANTAGE_API_KEY:
            print("Alpha Vantage API key not found in environment variables")
            return {}
            
        news_by_stock = {}
        
        for ticker in stocks:
            url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={ALPHA_VANTAGE_API_KEY}'
            
            print(f"\nFetching news for {ticker}...")
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            feed = data.get('feed', [])
            
            if feed:
                news_items = []
                for item in feed[:items_per_stock]:
                    news_items.append({
                        'title': item.get('title', 'No title'),
                        'time_published': item.get('time_published', 'No date'),
                        'summary': item.get('summary', 'No summary'),
                        'url': item.get('url', 'No URL'),
                        'sentiment': item.get('overall_sentiment_label', 'No sentiment')
                    })
                    print(f"Found: {item.get('title', 'No title')}")
                
                news_by_stock[ticker] = news_items
                
                # Add LLM analysis for news
                if news_items:
                    news_prompt = f"""
                    Analyze these news items for {ticker}:
                    {news_items}
                    Provide a brief sentiment summary and key takeaways in 2-3 sentences.
                    """
                    news_analysis = model.generate_content(contents=news_prompt)
                    print(f"\nNews Analysis for {ticker}:")
                    print(news_analysis.text)
            else:
                print(f"No news found for {ticker}")
                news_by_stock[ticker] = []
                
        return news_by_stock
        
    except Exception as e:
        print(f"Error getting news: {str(e)}")
        return {}

def get_analyst_recommendations(stocks: List[str]) -> Dict[str, Dict]:
    """
    Get analyst recommendations and metrics for stocks
    """
    try:
        ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
        
        if not ALPHA_VANTAGE_API_KEY:
            print("Alpha Vantage API key not found in environment variables")
            return {}
            
        recommendations = {}
        
        for ticker in stocks:
            url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}'
            
            print(f"\nFetching analyst recommendations for {ticker}...")
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            if data:
                recommendations[ticker] = {
                    'TargetPrice': data.get('AnalystTargetPrice', 'N/A'),
                    'PERatio': data.get('PERatio', 'N/A'),
                    'PEGRatio': data.get('PEGRatio', 'N/A'),
                    'Beta': data.get('Beta', 'N/A'),
                    'EPS': data.get('EPS', 'N/A'),
                    '52WeekHigh': data.get('52WeekHigh', 'N/A'),
                    '52WeekLow': data.get('52WeekLow', 'N/A')
                }
                
                # Add LLM analysis for analyst data
                metrics_prompt = f"""
                Analyze these metrics for {ticker}:
                {recommendations[ticker]}
                Provide a brief analysis of the stock's valuation and risk metrics in 2-3 sentences.
                """
                metrics_analysis = model.generate_content(contents=metrics_prompt)
                print(f"\nMetrics Analysis for {ticker}:")
                print(metrics_analysis.text)
                
            else:
                print(f"No analyst data found for {ticker}")
                recommendations[ticker] = {}
                
        return recommendations
        
    except Exception as e:
        print(f"Error getting analyst recommendations: {str(e)}")
        return {}