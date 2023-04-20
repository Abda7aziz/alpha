import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table


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

