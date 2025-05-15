from dash import dcc, html
import dash_bootstrap_components as dbc

def serve_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Trade Simulator", className="text-center mb-4"),
                dbc.Card([
                    dbc.CardHeader("Input Parameters"),
                    dbc.CardBody([
                        dbc.Form([
                            dbc.Label("Order Size (USD)"),
                            dbc.Input(id="order-size", type="number", value=100),
                            dbc.Label("Fee Tier"),
                            dcc.Dropdown(
                                id="fee-tier",
                                options=[
                                    {"label": "VIP0", "value": "VIP0"},
                                    {"label": "VIP1", "value": "VIP1"}
                                ],
                                value="VIP0"
                            )
                        ])
                    ])
                ])
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Simulation Output"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(html.Div(id="slippage-output"), width=6),
                            dbc.Col(html.Div(id="fees-output"), width=6)
                        ]),
                        dbc.Row([
                            dbc.Col(html.Div(id="impact-output"), width=6),
                            dbc.Col(html.Div(id="net-cost-output"), width=6)
                        ]),
                        dcc.Graph(id="price-chart"),
                        html.Div(id="latency-output")
                    ])
                ])
            ], width=8)
        ]),
        dcc.Interval(id="update-interval", interval=1000)
    ], fluid=True)
