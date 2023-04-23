from database.models import db, Users, Portfolios, Stocks, Transactions, Dividends, Cash
import yfinance as yf
import pandas as pd

def init_and_populate_db(username, first, last, email, portfolio, type, market, currency):

	db.create_all()
 
	user = Users(username=username,password='pass', first_name=first, last_name=last, email=email)
	db.session.add(user)
	db.session.commit()

	portfolio = Portfolios(name=portfolio, type=type, market=market, currency=currency, user_id=user.id)
	db.session.add(portfolio)
	db.session.commit()
 
	return user.username,portfolio.name, portfolio.id

def add_cash(portfolio_id, amount, currency):
	cash = Cash(portfolio_id=portfolio_id, amount=amount, currency=currency)
	db.session.add(cash)
	db.session.commit()

def register_dividend(ticker_symbol, amount, ex_dividend_date, payment_date):
    stock = Stocks.query.filter_by(ticker_symbol=ticker_symbol).first()
    print(stock)
    dividend = Dividends(stock_id=stock.id, amount=amount, ex_dividend_date=ex_dividend_date, payment_date=payment_date)
    db.session.add(dividend)
    db.session.commit()

def create_portfolio(username, portfolio_name, portfolio_type=None, market=None, currency=None):
	user = Users.query.filter_by(username=username).first()
	if not user:
		return None

	portfolio = Portfolios.query.filter_by(user_id=user.id, name=portfolio_name).first()

	if not portfolio and all([portfolio_type, market, currency]):
		portfolio = Portfolios(name=portfolio_name, type=portfolio_type, market=market, currency=currency, user_id=user.id)
		db.session.add(portfolio)
		db.session.commit()

	return portfolio

def buy_stock(ticker_symbol, name, shares, price, portfolio_id):
	# Check if the stock exists in the database
	stock = Stocks.query.filter_by(ticker_symbol=ticker_symbol).first()

	# If the stock doesn't exist, create it
	if stock is None:
		stock = Stocks(ticker_symbol=ticker_symbol, name=name, shares=0, portfolio_id=portfolio_id)
	db.session.add(stock)
	db.session.commit()

	# Update the stock's shares
	stock.shares += shares
	db.session.commit()

	# Create a new transaction
	transaction = Transactions(type='buy', price=price, shares=shares, stock_id=stock.id)
	db.session.add(transaction)
	db.session.commit()

  
		# Update the portfolio's cash
		# portfolio = Portfolios.query.get(portfolio_id)
		# portfolio_cash = portfolio.cash
		# portfolio_cash -= price * shares
		# db.session.commit()
	return transaction

def sell_stock(ticker_symbol, shares, price, portfolio_id):
	stock = Stocks.query.filter_by(ticker_symbol=ticker_symbol, portfolio_id=portfolio_id).first()
	print('Hi\n',stock,' What?')
	if stock and stock.shares >= shares:
		stock.shares -= shares
		transaction = Transactions(type='sell', price=price, shares=shares, stock_id=stock.id)
		db.session.add(transaction)
		db.session.commit()
	elif stock.shares == 0:
		db.session.delete(stock)
	else:
		# Handle the case where the user tries to sell more shares than they have
		pass

# Get transactions for a stock
def get_stock_transactions(stock_id):
	transactions = Transactions.query.filter_by(stock_id=stock_id).all()
	return transactions

# Get dividends for a stock
def get_stock_dividends(stock_id):
	dividends = Dividends.query.filter_by(stock_id=stock_id).all()
	return dividends

# Get stocks for a portfolio
def get_portfolio_stocks(portfolio_id):
	stocks = Stocks.query.filter_by(portfolio_id=portfolio_id).all()
	return stocks

def get_stock_details(ticker_symbol):
    # Get the latest data for the given ticker symbol
    print(f'{ticker_symbol}.SR')
    ticker_data = yf.Ticker(f'{ticker_symbol}.SR')
    latest_price = ticker_data.info["currentPrice"]
    
    # Get other details for the stock
    name = ticker_data.info["shortName"]
    # sector = ticker_data.info["sector"]
    # industry = ticker_data.info["industry"]
    
    return {
        "name": name,
        # "sector": sector,
        # "industry": industry,
        "price": latest_price
    }

def export_transactions_and_delete_db(portfolio_id):
    # Get stocks for the portfolio
    stocks = get_portfolio_stocks(portfolio_id)

    # Create a DataFrame for transactions
    transactions_data = []
    for stock in stocks:
        transactions = get_stock_transactions(stock.id)
        for transaction in transactions:
            transactions_data.append({
                "created_datetime": transaction.created_datetime,
                "ticker_symbol": stock.ticker_symbol,
                "name": stock.name,
                "type": transaction.type,
                "shares": transaction.shares,
                "price": transaction.price,
            })
    transactions_df = pd.DataFrame(transactions_data)

    # Create a DataFrame for dividends
    dividends_data = []
    for stock in stocks:
        dividends = get_stock_dividends(stock.id)
        for dividend in dividends:
            dividends_data.append({
                "ticker_symbol": stock.ticker_symbol,
                "amount": dividend.amount,
                "ex_dividend_date": dividend.ex_dividend_date,
                'payment_date': dividend.payment_date
            })
    dividends_df = pd.DataFrame(dividends_data)
    
    db.drop_all()
    db.create_all()
    return transactions_df,dividends_df
