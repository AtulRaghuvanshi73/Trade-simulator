import asyncio
import time
import dash
from dash import Input, Output, State
import dash_bootstrap_components as dbc
import threading
import logging

from core.orderbook import OrderBook
from core.models import AlmgrenChriss, SlippageModel, MakerTakerModel
from core.websocket_client import WebSocketClient
from ui.layout import serve_layout

import numpy as np

# --- Logging ---
logging.basicConfig(level=logging.INFO)

# --- Global State ---
orderbook = OrderBook()
ac_model = AlmgrenChriss()
slippage_model = SlippageModel()
maker_taker_model = MakerTakerModel()
latest_latency = 0
last_latency = None
last_data_time = time.time()
connection_status = "Disconnected"
websocket_connected = False  # Track actual connection status

# --- WebSocket Handler ---
async def on_ws_message(data):
    global orderbook, latest_latency, last_latency, last_data_time, connection_status, websocket_connected
    # Use perf_counter for more precise timing (nanosecond resolution)
    start = time.perf_counter()
    try:
        # Handle connection status updates
        if "connection_status" in data:
            if data["connection_status"] == "connected":
                connection_status = "Connected"
                websocket_connected = True
                logging.info("WebSocket connection established")
                return
            elif data["connection_status"] == "disconnected":
                connection_status = "Disconnected"
                websocket_connected = False
                logging.info("WebSocket disconnected")
                return
                
        # Log message structure to help with debugging
        logging.info(f"WebSocket message received: {list(data.keys())}")
        
        if 'bids' in data and 'asks' in data:
            # Measure the size of the orderbook for context
            bid_ask_size = len(data['bids']) + len(data['asks'])
            
            # Process the orderbook update
            orderbook.update(data['bids'], data['asks'])
            
            # Calculate latency with more precision
            last_data_time = time.time()
            latest_latency = (time.perf_counter() - start) * 1000  # Convert to milliseconds
            last_latency = latest_latency
            connection_status = "Connected"
            logging.info(f"Orderbook updated (size: {bid_ask_size}), latency: {latest_latency:.4f} ms")
        else:
            logging.warning(f"Received data missing 'bids' or 'asks': {data}")
    except Exception as e:
        logging.error(f"Error processing message: {e}")

def start_ws():
    url = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ws_client = WebSocketClient(url, on_ws_message)
    loop.run_until_complete(ws_client.run())

ws_thread = threading.Thread(target=start_ws, daemon=True)
ws_thread.start()

# --- Dash App ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = serve_layout

@app.callback(
    Output('slippage-output', 'children'),
    Output('fees-output', 'children'),
    Output('impact-output', 'children'),
    Output('net-cost-output', 'children'),
    Output('price-chart', 'figure'),
    Output('latency-output', 'children'),
    Output('data-warning', 'children'),
    Output('connection-status', 'children'),
    Input('update-interval', 'n_intervals'),
    State('order-size', 'value'),
    State('fee-tier', 'value')
)
def update_outputs(n, order_size, fee_tier):
    global last_latency, last_data_time, connection_status

    # Fee table
    fee_table = {'VIP0': {'maker': 0.0008, 'taker': 0.001}, 'VIP1': {'maker': 0.0007, 'taker': 0.0009}}
    spread = orderbook.spread()
    volatility = orderbook.volatility()
    imbalance = orderbook.book_imbalance()
    volume = orderbook.market_volume()
    slippage = slippage_model.predict(order_size, spread, volatility, imbalance)
    impact = ac_model.impact(order_size, volume, volatility, spread)
    maker_prob = maker_taker_model.predict(order_size, spread, imbalance)
    fees = order_size * fee_table[fee_tier]['taker']
    net_cost = slippage + impact + fees
    fig = {
        'data': [{'y': orderbook.mid_prices, 'type': 'line', 'name': 'Mid Price'}],
        'layout': {'height': 200, 'margin': {'l': 30, 'r': 10, 't': 20, 'b': 30}}
    }   
    latency = last_latency if last_latency is not None else None
    # Show more decimal places for more precise measurements
    latency_str = f"Processing Latency: {latency:.4f} ms" if latency is not None else "Processing Latency: 0.0 ms"# Data warning if no data in last 5 seconds
    time_since_data = time.time() - last_data_time
    if time_since_data > 5:
        if websocket_connected:
            warning = "⚠️ WebSocket connected but no orderbook data received. Waiting for data..."
            conn_status = "Connected (Waiting for Data)"
        else:
            warning = "⚠️ No live data received in the last 5 seconds. Check your VPN and connection."
            conn_status = "Disconnected"
    else:
        warning = ""
        conn_status = connection_status

    return (
        f"Slippage: ${slippage:.4f}",
        f"Fees: ${fees:.4f}",
        f"Market Impact: ${impact:.4f}",
        f"Net Cost: ${net_cost:.4f}",
        fig,
        latency_str,
        warning,
        f"WebSocket Status: {conn_status}"
    )

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8050, debug=False)
