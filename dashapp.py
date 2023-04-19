import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from config import Config
from sqlalchemy.orm import scoped_session, sessionmaker
from database.functions import buy_stock,sell_stock,register_dividend,get_portfolio_stocks,get_stock_dividends,get_stock_transactions, init_and_populate_db
from datetime import datetime
from database.models import Users, Portfolios,Stocks ,db

# DATABASE_URI = 'postgresql://admin:pass@localhost/tasi'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# engine = create_engine(DATABASE_URI)
# db_session = scoped_session(sessionmaker(bind=engine))

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE],suppress_callback_exceptions=True)
with app.server.app_context():
    app.server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alpha.db'
    db.init_app(app.server)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app.server)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='store', storage_type='session')

])

page_1_layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            [
                dbc.Jumbotron(
                    [
                        dbc.Container(
                            [
                                html.H1("Stock Portfolio Manager", className="display-4 text-center mb-4"),
                                html.P(
                                    "Enter your personal and portfolio information:",
                                    className="lead text-center mb-4"
                                ),
                                dbc.Form(
                                    [
                                        dbc.FormGroup(
                                            [
                                                dbc.Label("Username", className="mr-2"),
                                                dbc.Input(
                                                    id="username",
                                                    type="text",
                                                    placeholder="Enter username"
                                                )
                                            ],
                                            row=True,
                                        ),
                                        dbc.FormGroup(
                                            [
                                                dbc.Label("First Name", className="mr-2"),
                                                dbc.Input(
                                                    id="first",
                                                    type="text",
                                                    placeholder="Enter first name"
                                                )
                                            ],
                                            row=True,
                                        ),
                                        dbc.FormGroup(
                                            [
                                                dbc.Label("Last Name", className="mr-2"),
                                                dbc.Input(
                                                    id="last",
                                                    type="text",
                                                    placeholder="Enter last name"
                                                )
                                            ],
                                            row=True,
                                        ),
                                        dbc.FormGroup(
                                            [
                                                dbc.Label("Email", className="mr-2"),
                                                dbc.Input(
                                                    id="email",
                                                    type="email",
                                                    placeholder="Enter email"
                                                )
                                            ],
                                            row=True,
                                        ),
                                        dbc.FormGroup(
                                            [
                                                dbc.Label("Portfolio Name", className="mr-2"),
                                                dbc.Input(
                                                    id="portfolio",
                                                    type="text",
                                                    placeholder="Enter portfolio name"
                                                )
                                            ],
                                            row=True,
                                        ),
                                        dbc.FormGroup(
                                            [
                                                dbc.Label("Portfolio Type", className="mr-2"),
                                                dbc.Input(
                                                    id="type",
                                                    type="text",
                                                    placeholder="type"
                                                )
                                            ],
                                            row=True,
                                        ),
                                        dbc.FormGroup(
                                            [
                                                dbc.Label("Market", className="mr-2"),
                                                dbc.Input(
                                                    id="market",
                                                    type="text",
                                                    placeholder="market"
                                                )
                                            ],
                                            row=True,
                                        ),
                                        dbc.FormGroup(
                                            [
                                                dbc.Label("Portfolio Currency", className="mr-2"),
                                                dbc.Input(
                                                    id="currency",
                                                    type="text",
                                                    placeholder="currency"
                                                )
                                            ],
                                            row=True,
                                        ),
                                        dbc.Button(
                                            "Submit",
                                            id="submit-button",
                                            color="primary",
                                            className="mt-3",
                                        ),
                                    ],
                                ),
                            ],
                            fluid=True,
                        )
                    ]
                )
            ],
            width={"size": 10, "offset": 1},
        )
    ),
    dbc.Row(
        dbc.Col(
            dbc.Alert(
                "Error: Username or Portfolio not found.",
                id="error-alert",
                color="danger",
                is_open=False,
            ),
            width=12,
        )
    ),
], fluid=True)


page_2_layout = layout2 = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2('Enter Transactions'), width=12),
        ]),

        # Buy, sell stock, and dividends forms
        dbc.Row([
            dbc.Col(
                dbc.Form([
                    # Buy Stock Form
                    dbc.FormGroup([
                        dbc.Label('Buy Stock'),
                        dbc.Input(id='buy-ticker-symbol', type='text', placeholder='Ticker Symbol'),
                        dbc.Input(id='buy-name', type='text', placeholder='Stock Name'),
                        dbc.Input(id='buy-shares', type='number', placeholder='Shares', step='any'),
                        dbc.Input(id='buy-price', type='number', placeholder='Price', step='any'),
                        dbc.Button('Submit', id='buy-submit-button', color='primary', n_clicks=0)
                    ])
                ]),
                width=6
            ),   
            dbc.Col(
                dbc.Form([
                    # Sell Stock Form
                    dbc.FormGroup([
                        dbc.Label('Sell Stock'),
                        dbc.Input(id='sell-ticker-symbol', type='text', placeholder='Ticker Symbol'),
                        dbc.Input(id='sell-shares', type='number', placeholder='Shares', step='any'),
                        dbc.Input(id='sell-price', type='number', placeholder='Price', step='any'),
                        dbc.Button('Submit', id='sell-submit-button', color='primary', n_clicks=0)
                    ])
                ]),
                width=6
            ),
            dbc.Col(
                dbc.Form([
                    # Register Dividends Form
                    dbc.FormGroup([
                        dbc.Label('Register Dividends'),
                        dbc.Input(id='div-ticker-symbol', type='text', placeholder='Ticker Symbol'),
                        dbc.Input(id='div-amount', type='number', placeholder='Amount', step='any'),
                        dbc.Input(id='div-ex-date', type='date', placeholder='Ex-Dividend Date'),
                        dbc.Input(id='div-payment-date', type='date', placeholder='Payment Date'),
                        dbc.Button('Submit', id='div-submit-button', color='primary', n_clicks=0)
                    ])
                ]),
                width=6
            ),
            dbc.Col(
                dbc.Form([
                    # Add Cash Form
                    dbc.FormGroup([
                        dbc.Label('Add Cash'),
                        dbc.Input(id='add-portfoilio-name', type='text', placeholder='Portfolio Name', disabled=True),
                        dbc.Input(id='add-cash-amount', type='number', placeholder='Amount', step='any', disabled=True),
                        dbc.Input(id='add-cash-currency', type='text', placeholder='Currency',disabled=True),
                        dbc.Button('Submit', id='add-cash-submit', color='primary', n_clicks=0, disabled=True)
                    ])
                ]),
                width=6
            )
        ]),
        
        dbc.Row([
            # Stock Details header
            dbc.Col(html.H2('Stock Details'), width=12),

            # DataTable for displaying stock details
            dbc.Col(
                dash_table.DataTable(
                    id='stock-details-table',
                    columns=[
                        {'name': 'Stock Name', 'id': 'name'},
                        {'name': 'Ticker Symbol', 'id': 'ticker_symbol'},
                        {'name': 'Shares', 'id': 'shares'},
                        {'name': 'Price', 'id': 'price'},
                        {'name': 'Average', 'id': 'average'},
                        {'name': 'Buy/Sell Average', 'id': 'buy_sell_average'},
                        {'name': 'Buy/Sell/Dividends Average', 'id': 'buy_sell__div_average'},
                        {'name': 'Unrealized Gain/Loss', 'id': 'unrealized'},
                    ],
                    data=[],
                    style_table={'overflowX': 'auto'}
                ),
                width=12
            ),
        ]),

        dbc.Row([
            # Transactions Summary header
            dbc.Col(html.H2('Transactions Summary'), width=12),
            dbc.Col(html.Div(id='transactions-summary'), width=12),
        ]),
    ])
])


###### Callbacks #######

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/transactions':
        return page_2_layout
    else:
        return page_1_layout


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
            init_and_populate_db(username, first, last, email, portfolio, type, market, currency)
            user = Users.query.filter_by(username=username).first()
            if user:
                user_portfolio = Portfolios.query.filter_by(user_id=user.id, name=portfolio).first()
                if user_portfolio:
                    return False, {'username': username, 'portfolio': portfolio, 'portfolio_id': user_portfolio.id}, '/transactions'
            else:
                user = Users.query.filter_by(username=username).first()
                if user:
                    user_portfolio = Portfolios.query.filter_by(user_id=user.id, name=portfolio).first()
                    if user_portfolio:
                        return False, {'username': username, 'portfolio': portfolio, 'portfolio_id': user_portfolio.id}, '/transactions'

        return True, None, None

    return False, None, None


# Callback for the buy stock form
@app.callback(
    Output('buy-ticker-symbol', 'value'),
    Output('buy-name', 'value'),
    Output('buy-shares', 'value'),
    Output('buy-price', 'value'),
    Input('buy-submit-button', 'n_clicks'),
    State('buy-ticker-symbol', 'value'),
    State('buy-name', 'value'),
    State('buy-shares', 'value'),
    State('buy-price', 'value'),
    State('store', 'data')
)
def handle_buy_stock(n_clicks, ticker_symbol, name, shares, price, store_data):
    if n_clicks is not None and n_clicks > 0:
        with app.server.app_context():
            # Get the portfolio_id for the given username and portfolio_name
            username,portfolio_id = store_data['username'],store_data['portfolio_id']
            if username:
                buy_stock(ticker_symbol, name, shares, price, portfolio_id)
            return '', '', '', ''
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update


# Callback for the sell stock form
@app.callback(
    Output('sell-ticker-symbol', 'value'),
    Output('sell-shares', 'value'),
    Output('sell-price', 'value'),
    Input('sell-submit-button', 'n_clicks'),
    State('sell-ticker-symbol', 'value'),
    State('sell-shares', 'value'),
    State('sell-price', 'value'),
    State('store', 'data')
)
def handle_sell_stock(n_clicks, ticker_symbol, shares, price, store_data):
    if n_clicks is not None and n_clicks > 0:
        with app.server.app_context():
            # Get the portfolio_id for the given username and portfolio_name
            username,portfolio_id = store_data['username'],store_data['portfolio_id']
            if username:
                sell_stock(ticker_symbol, shares, price, portfolio_id)
            return '', '', ''
    return dash.no_update, dash.no_update, dash.no_update


# Callback for the add dividends form
@app.callback(
    Output('div-ticker-symbol', 'value'),
    Output('div-amount', 'value'),
    Output('div-ex-date', 'value'),
    Output('div-payment-date', 'value'),
    Input('div-submit-button', 'n_clicks'),
    State('div-ticker-symbol', 'value'),
    State('div-amount', 'value'),
    State('div-ex-date', 'value'),
    State('div-payment-date', 'value')
)
def handle_add_dividends(n_clicks, ticker_symbol, amount, ex_dividend_date, payment_date):
    if n_clicks is not None and n_clicks > 0:
        with app.server.app_context():
            stock = Stocks.query.filter_by(ticker_symbol=ticker_symbol).first()
            print(ex_dividend_date)
            ex_dividend_date = datetime.strptime(ex_dividend_date, '%Y-%m-%d').date()
            payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
            register_dividend(stock.id, amount, ex_dividend_date, payment_date)
            return '', '', '', ''
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update


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


# @app.server.teardown_request
# def teardown_request(exception=None):
#     db.session.remove()

if __name__ == "__main__":
    app.run_server(debug=True)
