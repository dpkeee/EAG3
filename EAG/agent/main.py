import google.generativeai as genai
from stock_functions import get_top_stocks, get_latest_news
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def analyze_news_with_llm(news_data: dict, model) -> str:
    """
    Analyze news data using LLM
    """
    try:
        analysis_prompt = f"""
        Analyze these news items for each stock:
        {news_data}
        
        For each stock provide:
        1. Key takeaways from the news
        2. Overall sentiment
        3. Potential impact
        
        Keep the response brief and focused.
        """
        
        analysis_response = model.generate_content(contents=analysis_prompt)
        return analysis_response.text
        
    except Exception as e:
        return f"Error in LLM analysis: {str(e)}"

def parse_and_execute_response(response_text, model):
    """
    Parse the model's response and execute appropriate functions
    """
    try:
        if response_text.startswith("FUNCTION_CALL:"):
            # Get stock data
            stocks = get_top_stocks()
            
            # Get news data
            news_data = get_latest_news(stocks)
            
            # Analyze with LLM
            analysis = analyze_news_with_llm(news_data, model)
            
            return analysis
                
        elif response_text.startswith("FINAL_ANSWER:"):
            return response_text
        else:
            raise ValueError("Invalid response format")
            
    except Exception as e:
        return f"Error processing response: {str(e)}"

def main():
    try:
        # Configure the Gemini model
        GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key not found in environment variables")
            
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')

        # Define the system prompt
        system_prompt = '''You are an agent which monitors stock prices continuously. Respond with EXACTLY ONE of these formats:
        1. FUNCTION_CALL: get_top_stocks|website
        2. FUNCTION_CALL: get_latest_news|stock_list
        3. FUNCTION_CALL: get_analyst_recommendations|stock_list
        4. FINAL_ANSWER: [text]

        where python_function_name is one of the following:
        1. get_top_stocks(website) - extracts top 5 performing stocks for the current day
        2. get_latest_news(stock_list) - takes the tickers from get_top_stocks and gets the latest news
        3. get_analyst_recommendations(stock_list) - takes the tickers and gets analyst recommendations
        
        The functions should be called in this order:
        1. First get top stocks
        2. Then get news for those stocks
        3. Then get analyst recommendations
        4. Finally provide analysis
        
        DO NOT include multiple responses. Give ONE response at a time.'''

        # Define the query
        current_query = "Give me today's top performing stocks with complete analysis"
        
        # Format the complete prompt
        prompt = f"{system_prompt}\n\nQuery: {current_query}"

        # Generate initial response
        print("Fetching and analyzing stocks...\n")
        response = model.generate_content(contents=prompt)
        
        # Process the response
        result = parse_and_execute_response(response.text, model)
        
        # Print the result
        print(result)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 