import yfinance as yf

def fetch_financial_data(company_symbol):
    """Fetches live financial data for a given company symbol."""
    try:
        stock = yf.Ticker(company_symbol)
        info = stock.info
        return {
            "Company Name": info.get("longName"),
            "Current Price": info.get("currentPrice"),
            "Market Cap": info.get("marketCap"),
            "PE Ratio": info.get("trailingPE"),
            "52-Week High": info.get("fiftyTwoWeekHigh"),
            "52-Week Low": info.get("fiftyTwoWeekLow"),
        }
    except Exception as e:
        return {"error": f"Error fetching data: {str(e)}"}
