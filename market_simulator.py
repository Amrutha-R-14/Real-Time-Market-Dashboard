import asyncio
import random
from datetime import datetime

class MarketSimulator:
    def __init__(self):
        self.data = []
        self.bids = []
        self.asks = []

    async def stream_data(self, interval=1):
        """Generate synthetic market data every `interval` seconds"""
        while True:
            price = round(random.uniform(90, 110), 2)
            volume = random.randint(100, 1000)
            timestamp = datetime.now()

            self.data.append({
                "timestamp": timestamp,
                "price": price,
                "volume": volume
            })

            # Simulate bids and asks
            self.bids = [(price - i, random.randint(10, 100)) for i in range(5)]
            self.asks = [(price + i, random.randint(10, 100)) for i in range(5)]

            await asyncio.sleep(interval)

    def get_latest_data(self):
        """Return the latest data point"""
        return self.data[-1] if self.data else None

    def get_orderbook(self):
        """Return current bids and asks"""
        return self.bids, self.asks
