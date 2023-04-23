import yfinance as yf

def get_stock_details(ticker_symbol):
    # Get the latest data for the given ticker symbol
    print(f'{ticker_symbol}.SR')
    ticker_data = yf.Ticker(f'{ticker_symbol}.SR')
    latest_price = ticker_data.info["currentPrice"]
    print(type(latest_price))
    # Get other details for the stock
    name = ticker_data.info["shortName"]
    sector = ticker_data.info["sector"]
    industry = ticker_data.info["industry"]
    
    return {
        "name": name,
        "sector": sector,
        "industry": industry,
        "price": latest_price
    }
    
print(get_stock_details('7010'))

