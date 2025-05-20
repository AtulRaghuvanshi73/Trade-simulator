import pytest
import numpy as np
from core.models import AlmgrenChriss, SlippageModel, MakerTakerModel

def test_almgren_chriss_basic():
    """Test AC model with known parameters"""
    model = AlmgrenChriss(gamma=0.2, eta=0.1)
    
    # Test with zero market volume
    assert model.impact(1000, 0, 0.1, 2.0) == 0.0
    
    # Test normal case
    Q, V, σ, S = 1000, 10000, 0.02, 1.5
    impact = model.impact(Q, V, σ, S)
    
    permanent = 0.2 * σ * np.sqrt(Q/V)
    temporary = S + 0.1 * (Q/V)
    assert impact == pytest.approx(permanent + temporary)

def test_slippage_model_learning():
    """Test online learning capability"""
    model = SlippageModel()
    
    # Before training
    assert model.predict(100, 1.0, 0.02, 0.3) == pytest.approx(0.5)  # default
    
    # Train with synthetic data
    for _ in range(100):
        model.update(
            order_size=100, 
            spread=1.0, 
            volatility=0.02, 
            imbalance=0.3, 
            actual_slippage=0.6
        )
    
    # After training
    pred = model.predict(100, 1.0, 0.02, 0.3)
    assert 0.55 < pred < 0.65  # should approach 0.6

def test_maker_taker_model():
    """Test execution type prediction"""
    model = MakerTakerModel()
    
    # Train with clear pattern: large orders = taker
    for _ in range(100):
        is_maker = np.random.choice([True, False], p=[0.8, 0.2])
        model.update(
            order_size=100 if is_maker else 10000,
            spread=1.0,
            imbalance=0.1,
            is_maker=is_maker
        )
    
    # Verify predictions
    assert model.predict(100, 1.0, 0.1) > 0.7  # likely maker
    assert model.predict(10000, 1.0, 0.1) < 0.3  # likely taker
