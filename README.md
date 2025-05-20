# Trade Simulator

A high-performance, real-time cryptocurrency trade simulator using OKX L2 orderbook data. This project provides accurate estimates of market impact, slippage, and execution costs for trading strategies.

## Features

- **Real-time Data Processing**: WebSocket connection to OKX L2 orderbook with efficient reconnection logic
- **Advanced Financial Models**:
  - Almgren-Chriss market impact model for execution cost estimation
  - Dynamic slippage regression model that learns from simulated trades
  - Maker/taker prediction for fee calculation
- **Performance Optimized**:
  - Sub-millisecond orderbook updates and model inference
  - Memory-efficient rolling statistics
  - Vectorized calculations
- **Interactive Dash UI**:
  - Real-time visualization of orderbook data
  - Dynamic cost estimation based on user parameters
  - Performance metrics and connection status
- **Comprehensive Testing**:
  - Unit tests for all components
  - Performance benchmarks
  - UI integration tests
- **Production Ready**:
  - Fully Dockerized for consistent deployment
  - Modular architecture for maintainability and extensibility

## Quick Start

1. Install Docker
2. Build and run:

```bash
docker build -t trade-simulator .
docker run -d -p 8050:8050 --name trade-sim trade-simulator
```

3. Open [http://localhost:8050](http://localhost:8050) in your browser

## Local Development

```bash
pip install -r requirements.txt
python main.py
```

## Project Architecture

The project is structured for clarity, modularity, and scalability:

- **core/**: Backend logic and algorithms
  - `orderbook.py`: L2 orderbook processing and statistics
  - `models.py`: Financial models for impact, slippage, and execution prediction
  - `websocket_client.py`: Async WebSocket client for real-time data
- **ui/**: User interface components
  - `layout.py`: Dash layout and component definitions
- **tests/**: Comprehensive test suite
  - Unit tests for all components
  - Benchmark tests for performance validation
  - UI integration tests
- **main.py**: Application entry point
- **Dockerfile & requirements.txt**: For containerization and reproducible environments

## Key Components

### Orderbook Processing

The `OrderBook` class provides:
- Fast bid/ask updates with dictionary-based storage
- Spread calculation
- Mid-price tracking with efficient rolling buffer
- Market volume and imbalance metrics
- Rolling volatility calculation

### Financial Models

1. **Almgren-Chriss Market Impact Model**
   - Estimates execution cost based on order size, market volume, volatility, and spread
   - Accounts for both permanent and temporary market impact

2. **Slippage Regression Model**
   - Learns from simulated trades to predict price slippage
   - Features include order size, spread, volatility, and orderbook imbalance
   - Online learning with adaptive retraining

3. **Maker/Taker Execution Prediction**
   - Logistic regression to predict passive vs. aggressive fills
   - Used to estimate fee impact on total cost

### WebSocket Data Ingestion

Robust, asynchronous client with:
- Automatic reconnection with exponential backoff
- Latency measurement
- Connection status tracking

### Interactive UI

Built with Dash and Bootstrap:
- User-configurable parameters (order size, fee tier)
- Real-time output metrics
- Connection status and performance indicators

## Testing and Benchmarking

The test suite ensures reliability and performance:

```bash
# Run all tests
pytest

# Run benchmark tests
pytest tests/test_benchmarks.py -v
```

Benchmark results validate:
- Orderbook update speed: <1ms
- Model inference time: <1ms
- End-to-end latency: <500ms


