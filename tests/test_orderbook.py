import pytest
import numpy as np
from core.orderbook import OrderBook

def test_orderbook_initialization():
    """Test empty orderbook state"""
    ob = OrderBook()
    assert len(ob.bids) == 0
    assert len(ob.asks) == 0
    assert ob.spread() == 0

def test_orderbook_update_logic():
    """Test bid/ask update and mid-price calculation"""
    ob = OrderBook()
    
    # Test basic update
    ob.update([[100.0, 1.0], [99.9, 2.0]], [[100.1, 0.5], [100.2, 1.5]])
    
    # Verify best bid/ask
    assert max(ob.bids.keys()) == 100.0
    assert min(ob.asks.keys()) == 100.1
    
    # Verify spread
    assert ob.spread() == pytest.approx(0.1)
    
    # Verify mid-price
    assert ob.mid_prices[-1] == pytest.approx((100.0 + 100.1)/2)

def test_market_metrics():
    """Test volume and imbalance calculations"""
    ob = OrderBook()
    ob.update(
        [[100.0, 1.0], [99.9, 2.0], [99.8, 3.0]],  # bids
        [[100.1, 0.5], [100.2, 1.5], [100.3, 2.0]]  # asks
    )
    
    # Test market volume (top 2 levels)
    assert ob.market_volume(levels=2) == pytest.approx((1.0+2.0) + (0.5+1.5))
    
    # Test orderbook imbalance
    bid_vol = 1.0 + 2.0 + 3.0
    ask_vol = 0.5 + 1.5 + 2.0
    expected_imbalance = (bid_vol - ask_vol) / (bid_vol + ask_vol)
    assert ob.book_imbalance() == pytest.approx(expected_imbalance)

def test_volatility_calculation():
    """Test rolling volatility calculation"""
    ob = OrderBook()
    prices = np.random.normal(100, 0.5, 200).tolist()
    for p in prices:
        ob.update([[p-0.1, 1.0]], [[p+0.1, 1.0]])
    
    # Volatility should match numpy's stddev
    expected_vol = np.std(prices[-60:])
    assert ob.volatility(window=60) == pytest.approx(expected_vol, rel=0.01)
