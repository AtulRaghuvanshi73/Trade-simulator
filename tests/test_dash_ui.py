import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

@pytest.mark.parametrize("order_size", [100, 500, 1000])
def test_slippage_output_updates(dash_duo, order_size):
    dash_duo.start_server(app)
    input_box = dash_duo.find_element("#order-size")
    input_box.clear()
    input_box.send_keys(str(order_size))
    dash_duo.wait_for_text_to_equal("#slippage-output", dash_duo.find_element("#slippage-output").text, timeout=10)
    assert "Slippage:" in dash_duo.find_element("#slippage-output").text

def test_latency_output_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal("#latency-output", dash_duo.find_element("#latency-output").text, timeout=10)
    assert "Latency" in dash_duo.find_element("#latency-output").text
