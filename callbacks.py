from database.functions import buy_stock,sell_stock,register_dividend,get_portfolio_stocks,get_stock_dividends,get_stock_transactions, init_and_populate_db,export_transactions_and_delete_db
from layouts import tab_upload_layout, tab_manual_layout
from database.models import Stocks
from dash.dependencies import Input, Output, State
from flask import send_file
import dash_bootstrap_components as dbc
from datetime import datetime
from dash import dcc
import pandas as pd
import layouts
import base64
import json
import time
import dash
import io

from app import app


@app.callback(
    Output("error-alert", "is_open"),
    Output('store', 'data'),
    Output('url', 'pathname'),
    State("username", "value"),
    State("first", "value"),
    State("last", "value"),
    State("email", "value"),
    State("portfolio", "value"),
    State("type", "value"),
    State("market", "value"),
    State("currency", "value"),
    Input("submit-button", "n_clicks"),
)
def handle_submit(n_clicks, username, first, last, email, portfolio, type, market, currency):
    if n_clicks is not None:
        with app.server.app_context():
            username,portfolio,portfolio_id = init_and_populate_db(username, first, last, email, portfolio, type, market, currency)
            return False, {'username': username, 'portfolio': portfolio, 'portfolio_id': portfolio_id}, '/transactions'
    return False, None, '/'

@app.callback(Output('tab-content', 'children'),
              Input('tabs', 'active_tab'))
def render_tab_content(active_tab):
    if active_tab == 'tab-upload':
        return tab_upload_layout
    elif active_tab == 'tab-manual':
        return tab_manual_layout


# Callback for the buy stock form
@app.callback(Output('page-content', 'children',allow_duplicate=True),
    Output('buy-ticker-symbol', 'value'),
    Output('buy-name', 'value'),
    Output('buy-shares', 'value'),
    Output('buy-price', 'value'),
    Input('buy-submit-button', 'n_clicks'),
    State('buy-ticker-symbol', 'value'),
    State('buy-name', 'value'),
    State('buy-shares', 'value'),
    State('buy-price', 'value'),
    State('store', 'data'),
    prevent_initial_call='True'
)
def handle_buy_stock(n_clicks, ticker_symbol, name, shares, price, store_data):
    if n_clicks is not None and n_clicks > 0:
        with app.server.app_context():
            # Get the portfolio_id for the given username and portfolio_name
            username,portfolio_id = store_data['username'],store_data['portfolio_id']
            if username:
                buy_stock(ticker_symbol, name, shares, price, portfolio_id)
            return layouts.page_2_layout,'', '', '', ''
    return dash.no_update,dash.no_update, dash.no_update, dash.no_update, dash.no_update


# Callback for the sell stock form
@app.callback(Output('page-content', 'children',allow_duplicate=True),
    Output('sell-ticker-symbol', 'value'),
    Output('sell-shares', 'value'),
    Output('sell-price', 'value'),
    Input('sell-submit-button', 'n_clicks'),
    State('sell-ticker-symbol', 'value'),
    State('sell-shares', 'value'),
    State('sell-price', 'value'),
    State('store', 'data'),
    prevent_initial_call='True'
)
def handle_sell_stock(n_clicks, ticker_symbol, shares, price, store_data):
    if n_clicks is not None and n_clicks > 0:
        with app.server.app_context():
            # Get the portfolio_id for the given username and portfolio_name
            username,portfolio_id = store_data['username'],store_data['portfolio_id']
            if username:
                sell_stock(ticker_symbol, shares, price, portfolio_id)
            return layouts.page_2_layout,'', '', ''
    return dash.no_update,dash.no_update, dash.no_update, dash.no_update


# Callback for the add dividends form
@app.callback(Output('page-content', 'children',allow_duplicate=True),
    Output('div-ticker-symbol', 'value'),
    Output('div-amount', 'value'),
    Output('div-ex-date', 'value'),
    Output('div-payment-date', 'value'),
    Input('div-submit-button', 'n_clicks'),
    State('div-ticker-symbol', 'value'),
    State('div-amount', 'value'),
    State('div-ex-date', 'value'),
    State('div-payment-date', 'value'),
    prevent_initial_call='True'
)
def handle_add_dividends(n_clicks, ticker_symbol, amount, ex_dividend_date, payment_date):
    if n_clicks is not None and n_clicks > 0:
        with app.server.app_context():
            stock = Stocks.query.filter_by(ticker_symbol=ticker_symbol).first()
            ex_dividend_date = datetime.strptime(ex_dividend_date, '%Y-%m-%d').date()
            payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
            register_dividend(stock.id, amount, ex_dividend_date, payment_date)
            return layouts.page_2_layout,'', '', '', ''
    return dash.no_update,dash.no_update, dash.no_update, dash.no_update, dash.no_update

###########################
###########################
####### Upload File #######
###########################
###########################

@app.callback(Output('page-content', 'children',allow_duplicate=True),
              Output('output-upload-file', 'children'),
              Input('upload-file', 'contents'),
              State('upload-file', 'filename'),
              State('store','data'),
                  prevent_initial_call=True)
def handle_file_upload(contents, filename,data):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        if filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif filename.endswith('.xlsx'):
            df_t = pd.read_excel(io.BytesIO(decoded),sheet_name='Transactions')
            df_d = pd.read_excel(io.BytesIO(decoded),sheet_name='Dividends')

        # Replace 'stock_id' column with 'ticker_symbol' and 'stock_name'
        # df = df.rename(columns={'stock_id': 'ticker_symbol'})

        # Here, you can process the DataFrame 'df' and insert the transactions into the database
        with app.server.app_context():
            portfolio_id = data['portfolio_id']
            print(df_t)
            for c,row in df_t.iterrows():
                if row['type'] == 'buy':
                    transaction = buy_stock(row['ticker_symbol'],row['name'],row['shares'],row['price'],portfolio_id)
                    print(transaction)
                else:
                    print(row['ticker_symbol'])
                    sell_stock(row['ticker_symbol'],row['shares'],row['price'],portfolio_id)
            for c,row in df_d.iterrows():    
                register_dividend(transaction.stock.id,row['amount'],row['ex_dividend_date'],row['payment_date'])

        # table = dash_table.DataTable(
        #     data=df.to_dict('records'),
        #     columns=[{'name': i, 'id': i} for i in df.columns],
        #     style_table={'overflowX': 'auto'})
        # ]
        print(filename)
        return layouts.page_2_layout,f'File "{filename}" uploaded and processed successfully.'
    else:
        return dash.no_update,dash.no_update


# Callback for updating stock details table and transactions summary
@app.callback(
    Output('stock-details-table', 'data'),
    Output('transactions-summary', 'children'),
    Input('store', 'data')
)
def update_stock_details(store_data):
    # Check if username and portfolio name data are not empty
    username,portfolio_id = store_data['username'],store_data['portfolio_id']
    if not username or not portfolio_id:
        return [], None

    with app.server.app_context():

        # Get stocks for the given portfolio
        stocks = get_portfolio_stocks(portfolio_id)

        # Calculate and update stock details
        stock_details = []
        summary_details = []
        for stock in stocks:
            # Fetch transactions and dividends for each stock
            transactions = get_stock_transactions(stock.id)
            dividends = get_stock_dividends(stock.id)

            # Sort transactions by timestamp (assuming the transaction object has a `timestamp` attribute)
            transactions = sorted(transactions, key=lambda x: x.created_datetime)

            # Initialize variables for calculations
            weighted_buy_sum = 0
            weighted_sell_sum = 0
            buy_shares = 0
            sell_shares = 0
            sell_gains = 0
            dividends_sum = sum([dividend.amount for dividend in dividends])

            # Process transactions to calculate buy and sell sums and shares
            for transaction in transactions:
                if transaction.type == 'buy':
                    weighted_buy_sum += transaction.price * transaction.shares
                    buy_shares += transaction.shares
                elif transaction.type == 'sell':
                    sell_gains += (transaction.price * transaction.shares) - (weighted_buy_sum / buy_shares if buy_shares > 0 else 0) * transaction.shares
                    weighted_sell_sum += transaction.price * transaction.shares
                    sell_shares += transaction.shares

            # Calculate buy average, buy/sell average, buy/sell/dividends average
            buy_avg = weighted_buy_sum / buy_shares if buy_shares > 0 else 0
            buy_sell_avg = (weighted_buy_sum - weighted_sell_sum) / (buy_shares - sell_shares) if buy_shares - sell_shares > 0 else 0
            buy_sell_dividends_avg = (weighted_buy_sum - weighted_sell_sum - dividends_sum) / (buy_shares - sell_shares) if buy_shares - sell_shares > 0 else 0
            # Calculate unrealized gain/loss (assuming you have the current price of the stock)
            current_price = 42  # Replace this with the actual current price of the stock
            unrealized_gain_loss = (current_price - buy_avg) * (buy_shares - sell_shares)

            # Append the calculated values to the stock_data list
            stock_details.append({
                'name': stock.name,
                'ticker_symbol': stock.ticker_symbol,
                'shares': stock.shares,
                'price': f'{current_price:,.2f}',
                'average': f'{buy_avg:,.2f}',
                'buy_sell_average': f'{buy_sell_avg:,.2f}',
                'buy_sell__div_average': f'{buy_sell_dividends_avg:,.2f}',
                'unrealized': f'{unrealized_gain_loss:,.2f}'
                # 'dividends_sum': dividends_sum,
            })

            # # Add the stock details to the list
            # stock_details.append({
            #     'name': stock.name,
            #     'ticker_symbol': stock.ticker_symbol,
            #     # ... (add other values as needed)
            # })

        # Calculate transactions summary (gained sum from selling and dividends)
            summary_details.append({
                'name':stock.name,
                'sell gains':sell_gains,
                'dividends sum':dividends_sum,
            })
        if len(stock_details) == 0:
            return stock_details,summary_details
        print(summary_details)
        sell_gains_ = sum([s['sell gains'] for s in summary_details])
        dividends_sum_ = sum([s['dividends sum'] for s in summary_details])
        
        # Create a list of children components to display the transactions summary
        summary_children = [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Label("Total Sell Value: "),
                            dbc.Label(f" SAR {sell_gains_:,.2f}", className="summary-value"),
                        ],
                        className="summary-item",
                    ),
                    dbc.Col(
                        [
                            dbc.Label("Total Dividends: "),
                            dbc.Label(f" SAR {dividends_sum_:,.2f}", className="summary-value"),
                        ],
                        className="summary-item",
                    ),
                    dbc.Col(
                        [
                            dbc.Label("Realized Gain/Loss: "),
                            dbc.Label(
                                f" SAR {sell_gains_ + dividends_sum_:,.2f}",
                                className="summary-value",
                                style={"color": "red" if (sell_gains + dividends_sum) < 0 else "green"},
                            ),
                        ],
                        className="summary-item",
                    ),
                ],
                className="summary-row",
            ),
        ]

        # Return the stock details data and transactions summary components
        return stock_details, summary_children


@app.callback(
    Output("download", "data"),
    Input("export-delete-button", "n_clicks"),
    State("store", "data"),
)
def on_export_delete_button_click(n_clicks, store_data):
    print(n_clicks)
    if n_clicks is not None:
        print('clicked')
        portfolio_id = store_data["portfolio_id"]
        transactions_df, dividends_df = export_transactions_and_delete_db(portfolio_id)
        
        df = pd.DataFrame()
        # excel_filename = "stocks_data.xlsx"
        excel_file = io.BytesIO()
        with pd.ExcelWriter(excel_file) as writer:
            transactions_df.to_excel(writer, sheet_name="Transactions", index=False)
            dividends_df.to_excel(writer, sheet_name="Dividends", index=False)
        
        # Return the file as a base64-encoded string
        return dict(content=base64.b64encode(excel_file.read()).decode(), 
                    filename='stocks_data.xlsx')
        
        # return send_file(response["content"], response["filename"])
        # return dcc.send_file(excel_filename, "my_stocks.xlsx")
    return None

if __name__ == "__main__":
    app.run_server(debug=True)
