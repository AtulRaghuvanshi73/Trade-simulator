import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression

class AlmgrenChriss:
    def __init__(self, gamma=0.1, eta=0.1):
        self.gamma = gamma
        self.eta = eta

    def impact(self, order_size, market_volume, volatility, spread):
        if market_volume == 0:
            return 0.0
        permanent = self.gamma * volatility * np.sqrt(order_size / market_volume)
        temporary = spread + self.eta * (order_size / market_volume)
        return float(permanent + temporary)

class SlippageModel:
    def __init__(self):
        self.model = LinearRegression()
        self.X = []
        self.y = []
        self.trained = False

    def update(self, order_size, spread, volatility, imbalance, actual_slippage):
        self.X.append([order_size, spread, volatility, imbalance])
        self.y.append(actual_slippage)
        if len(self.X) > 30:
            self.model.fit(self.X, self.y)
            self.trained = True
            if len(self.X) > 1000:
                self.X = self.X[-1000:]
                self.y = self.y[-1000:]

    def predict(self, order_size, spread, volatility, imbalance):
        if not self.trained:
            return spread * 0.5
        return float(self.model.predict([[order_size, spread, volatility, imbalance]])[0])

class MakerTakerModel:
    def __init__(self):
        self.model = LogisticRegression()
        self.X = []
        self.y = []
        self.trained = False

    def update(self, order_size, spread, imbalance, is_maker):
        self.X.append([order_size, spread, imbalance])
        self.y.append(int(is_maker))
        if len(self.X) > 30:
            self.model.fit(self.X, self.y)
            self.trained = True
            if len(self.X) > 1000:
                self.X = self.X[-1000:]
                self.y = self.y[-1000:]

    def predict(self, order_size, spread, imbalance):
        if not self.trained:
            return 0.5
        return float(self.model.predict_proba([[order_size, spread, imbalance]])[0][1])
