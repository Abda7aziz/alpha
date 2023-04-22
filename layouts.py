import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
# from dash_extensions import Download


page_1_layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H1("Stock Portfolio Manager", className="display-4 text-center mb-4"),
                                html.P(
                                    "Enter your personal and portfolio information:",
                                    className="lead text-center mb-4"
                                ),
                                dbc.Form(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Label("Username", className="mr-2"),
                                                dbc.Input(
                                                    id="username",
                                                    type="text",
                                                    placeholder="Enter username"
                                                )
                                            ],
                                            
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Label("First Name", className="mr-2"),
                                                dbc.Input(
                                                    id="first",
                                                    type="text",
                                                    placeholder="Enter first name"
                                                )
                                            ],
                                            
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Label("Last Name", className="mr-2"),
                                                dbc.Input(
                                                    id="last",
                                                    type="text",
                                                    placeholder="Enter last name"
                                                )
                                            ],
                                            
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Label("Email", className="mr-2"),
                                                dbc.Input(
                                                    id="email",
                                                    type="email",
                                                    placeholder="Enter email"
                                                )
                                            ],
                                            
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Label("Portfolio Name", className="mr-2"),
                                                dbc.Input(
                                                    id="portfolio",
                                                    type="text",
                                                    placeholder="Enter portfolio name"
                                                )
                                            ],
                                            
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Label("Portfolio Type", className="mr-2"),
                                                dbc.Input(
                                                    id="type",
                                                    type="text",
                                                    placeholder="type"
                                                )
                                            ],
                                            
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Label("Market", className="mr-2"),
                                                dbc.Input(
                                                    id="market",
                                                    type="text",
                                                    placeholder="market"
                                                )
                                            ],
                                            
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Label("Portfolio Currency", className="mr-2"),
                                                dbc.Input(
                                                    id="currency",
                                                    type="text",
                                                    placeholder="currency"
                                                )
                                            ],
                                            
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


page_2_layout = dbc.Container([
    dbc.Tabs(
        [
            dbc.Tab(label='Upload Transactions', tab_id='tab-upload'),
            dbc.Tab(label='Enter Transactions Manually', tab_id='tab-manual')
        ],
        id='tabs',
        active_tab='tab-upload',
        className="mb-3"
    ),
    dbc.Container(id='tab-content', fluid=True),
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
    dcc.Store('upload-store',storage_type='local')
]),

dbc.Row([
    # Transactions Summary header
    dbc.Col(html.H2('Transactions Summary'), width=12),
    dbc.Col(html.Div(id='transactions-summary'), width=12),
]),
# Export and Delete database button
dbc.Button("Export & Delete", id="export-delete-button", color="danger", className="mt-3"),
], fluid=True)


tab_upload_layout = dbc.Row([
    dbc.Col([
        html.Div([
    dbc.Alert(
        [
            html.H4("Instructions"),
            html.P(
                "Upload an Excel file with two sheets: 'Transactions' and 'Dividends'.",
                className="mb-2"
            ),
            html.Br(),
            html.P(
                "The Transactions sheet should include the following columns: datetime, Ticker Symbol, Stock Name, Transaction Type, Shares and Price.",
                className="mb-2"
            ),
            html.P(
                "The Dividends sheet should include the following columns: Ticker Symbol, Amount, ex_dividend_date,payment_date",
                className="mb-2"
            ),
            html.Br(),
            html.P(
                "Make sure that the column names are spelled correctly and in the same order as listed above.",
                className="mb-2"
            ),
            html.P(
                "Make sure the Transaction_Type column only include one of two types only, 'Buy' and 'Sell'.",
                className="mb-2"
            ),
            html.P(
                "Make sure the datetime format in the 'Transactions' sheet is in the format of 'YYYY-MM-DD HH:mm:ss' (e.g. 2022-05-20 13:15:00) and the two date columns in the 'Dividends' sheets is in the format of 'YYYY-MM-DD' (e.g. 2022-05-20), otherwise the data may not be imported correctly.",
                className="mb-2"
            ),
        ],
        id='instructions',
        color="info",
        dismissable=True,
    ),
        dcc.Upload(
            id='upload-file',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select File')
    ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
        html.Div(html.H5(id='output-upload-file')),
        dcc.Download(id="download"),
            ])
        ])
])

tab_manual_layout = dbc.Row([
    dbc.Col([
        html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2('Enter Transactions'), width=12),
        ]),

        # Buy, sell stock, and dividends forms
        dbc.Row([
            dbc.Col(
                dbc.Form([
                    # Buy Stock Form
                    dbc.Col([
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
                    dbc.Col([
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
                    dbc.Col([
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
                    dbc.Col([
                        dbc.Label('Add Cash'),
                        dbc.Input(id='add-portfoilio-name', type='text', placeholder='Portfolio Name', disabled=True),
                        dbc.Input(id='add-cash-amount', type='number', placeholder='Amount', step='any', disabled=True),
                        dbc.Input(id='add-cash-currency', type='text', placeholder='Currency',disabled=True),
                        dbc.Button('Submit', id='add-cash-submit', color='primary', n_clicks=0, disabled=True)
                    ])
                ]),
                width=6
            )
        ])
    ])
])

    ]),
])
