# Trade Simulator

A real-time cryptocurrency trade simulator using OKX L2 orderbook data.

## Features

- Real-time orderbook ingestion via WebSocket
- Market impact (Almgren-Chriss), slippage regression, maker/taker prediction
- Interactive Dash UI
- Dockerized for easy deployment

## Quick Start

1. Install Docker
2. Build and run:

    docker build -t trade-simulator .
    docker run -d -p 8050:8050 --name trade-sim trade-simulator

3. Open [http://localhost:8050](http://localhost:8050)

## Local Development

    pip install -r requirements.txt
    python main.py

## Project Structure

- `core/`: Backend logic (orderbook, models, websocket)
- `ui/`: Dash UI layout
- `main.py`: Entry point
