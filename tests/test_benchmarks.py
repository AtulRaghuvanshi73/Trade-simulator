import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.models import AlmgrenChriss
from core.orderbook import OrderBook

@pytest.mark.benchmark(group="models")
def test_impact_model_speed(benchmark):
    """Benchmark Almgren-Chriss model inference speed"""
    model = AlmgrenChriss()
    benchmark(model.impact, 1000, 10000, 0.02, 1.5)
    
    # Verify sub-millisecond performance
    assert benchmark.stats['mean'] < 0.001  # 1ms

@pytest.mark.benchmark(group="orderbook")
def test_orderbook_update_speed(benchmark):
    """Benchmark orderbook update throughput"""
    ob = OrderBook()
    bids = [[100 - i*0.1, 1.0] for i in range(10)]
    asks = [[100 + i*0.1, 1.0] for i in range(10)]
    
    benchmark(ob.update, bids, asks)
    
    # Verify <100μs per update
    assert benchmark.stats['mean'] < 0.0001  # 100μs
