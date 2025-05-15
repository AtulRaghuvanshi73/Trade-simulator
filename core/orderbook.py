import numpy as np

class OrderBook:
    def __init__(self):
        self.bids = {}
        self.asks = {}
        self.mid_prices = []

    def update(self, bids, asks):
        self.bids = {float(price): float(size) for price, size in bids}
        self.asks = {float(price): float(size) for price, size in asks}
        if self.bids and self.asks:
            mid = (max(self.bids.keys()) + min(self.asks.keys())) / 2
            self.mid_prices.append(mid)
            if len(self.mid_prices) > 200:
                self.mid_prices.pop(0)

    def spread(self):
        if not self.bids or not self.asks:
            return 0
        return min(self.asks.keys()) - max(self.bids.keys())

    def market_volume(self, levels=10):
        return sum(list(self.bids.values())[:levels]) + sum(list(self.asks.values())[:levels])

    def book_imbalance(self, levels=5):
        bid_vol = sum(list(self.bids.values())[:levels])
        ask_vol = sum(list(self.asks.values())[:levels])
        total = bid_vol + ask_vol
        return (bid_vol - ask_vol) / total if total else 0

    def volatility(self, window=60):
        if len(self.mid_prices) < window:
            return 0.0
        return float(np.std(self.mid_prices[-window:]))
