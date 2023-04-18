import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database.functions import buy_stock,sell_stock,register_dividend
from datetime import datetime
from database.models import Users, Portfolios,Stocks ,db

# DATABASE_URI = 'postgresql://admin:pass@localhost/tasi'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# engine = create_engine(DATABASE_URI)
# db_session = scoped_session(sessionmaker(bind=engine))

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
app.server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:pass@localhost/tasi'
app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app.server)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='store', storage_type='session')

])


page_1_layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Form([
                dbc.FormGroup([
                    dbc.Label("Username:", className="mr-2"),
                    dbc.Input(id="username", type="text", placeholder="Enter username")
                ], className="mr-3"),
                dbc.FormGroup([
                    dbc.Label("Portfolio Name:", className="mr-2"),
                    dbc.Input(id="portfolio", type="text", placeholder="Enter portfolio name")
                ], className="mr-3"),
                dbc.Button("Submit", id="submit-button", color="primary")
            ], inline=True),
            className="my-4"
        )
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Alert("Error: Username or Portfolio not found.", id="error-alert", color="danger", is_open=False),
            width=12
        )
    ]),
    dbc.Row(id="transactions-row", style={"display": "none"}),
], fluid=True)


page_2_layout = html.Div([
    # Top 20% of the page for registering transactions
    html.Div([
        html.H3("Register Transactions"),

        # Buy stock form
        html.Div([
            html.H4("Buy Stock"),
            dcc.Input(id='buy-ticker-symbol', type='text', placeholder='Ticker Symbol'),
            dcc.Input(id='buy-name', type='text', placeholder='Name'),
            dcc.Input(id='buy-shares', type='number', placeholder='Shares'),
            dcc.Input(id='buy-price', type='number', placeholder='Price'),
            html.Button(id='buy-submit-button', children='Buy'),
        ], style={'width': '33%'}),

        # Sell stock form
        html.Div([
            html.H4("Sell Stock"),
            dcc.Input(id='sell-ticker-symbol', type='text', placeholder='Ticker Symbol'),
            dcc.Input(id='sell-shares', type='number', placeholder='Shares'),
            dcc.Input(id='sell-price', type='number', placeholder='Price'),
            html.Button(id='sell-submit-button', children='Sell'),
        ], style={'width': '33%'}),

        # Add dividends form
        html.Div([
            html.H4("Add Dividends"),
            dcc.Input(id='div-ticker-symbol', type='text', placeholder='Ticker Symbol'),
            dcc.Input(id='div-amount', type='number', placeholder='Amount'),
            dcc.Input(id='div-ex-date', type='text', placeholder='Ex-dividend Date'),
            dcc.Input(id='div-payment-date', type='text', placeholder='Payment Date'),
            html.Button(id='div-submit-button', children='Add Dividend'),
        ], style={'width': '33%'}),

    ], style={'height': '20%', 'width': '100%', 'display': 'flex', 'justify-content': 'space-around'}),

    # The rest of the page (80%)
    html.Div([], style={'height': '80%', 'width': '100%'})
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
    Output("transactions-row", "style"),
    Output('store', 'data'),
    Output('url', 'pathname'),
    Input("submit-button", "n_clicks"),
    State("username", "value"),
    State("portfolio", "value")
)
def handle_submit(n_clicks, username, portfolio):
    if n_clicks is not None and n_clicks > 0:
        with app.server.app_context():
            user = Users.query.filter_by(username=username).first()
            if user:
                user_portfolio = Portfolios.query.filter_by(user_id=user.id, name=portfolio).first()
                if user_portfolio:
                    return False, {"display": "block"},{'username': username, 'portfolio': portfolio, 'portfolio_id' : user_portfolio.id} ,'/transactions'
            
            return True, {"display": "none"},None, None

    return False, {"display": "none"},None ,None

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
            ex_dividend_date = datetime.strptime(ex_dividend_date, '%d-%m-%Y').date()
            payment_date = datetime.strptime(payment_date, '%d-%m-%Y').date()
            register_dividend(stock.id, amount, ex_dividend_date, payment_date)
            return '', '', '', ''
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update


@app.server.teardown_request
def teardown_request(exception=None):
    db.session.remove()

if __name__ == "__main__":
    app.run_server(debug=True)
