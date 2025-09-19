import pandas as pd
from collections import deque

class MarketAnalytics:
    def __init__(self, simulator, max_points=100):
        self.simulator = simulator
        self.max_points = max_points

        # Store data in memory
        self.prices = deque(maxlen=max_points)
        self.volumes = deque(maxlen=max_points)
        self.timestamps = deque(maxlen=max_points)

    def get_price_data(self):
        """Return price time series as DataFrame"""
        data = self.simulator.get_latest_data()
        if data:
            self.prices.append(data["price"])
            self.volumes.append(data["volume"])
            self.timestamps.append(data["timestamp"])
        return pd.DataFrame({
            "timestamp": list(self.timestamps),
            "price": list(self.prices)
        })

    def get_volume_data(self):
        """Return volume time series as DataFrame"""
        return pd.DataFrame({
            "timestamp": list(self.timestamps),
            "volume": list(self.volumes)
        })

    def get_orderbook_snapshot(self):
        """Return latest order book snapshot (bids, asks)"""
        return self.simulator.get_orderbook()
