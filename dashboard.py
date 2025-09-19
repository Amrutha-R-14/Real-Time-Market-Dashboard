import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import threading
import time
import random
from datetime import datetime
from collections import deque

# ----------------------
# Market Simulator
# ----------------------
class MarketSimulator:
    def __init__(self):
        self.data = []
        self.bids = []
        self.asks = []
        self.running = False

    def start(self, interval=1):
        """Run simulator in background thread"""
        self.running = True
        thread = threading.Thread(target=self._run, args=(interval,), daemon=True)
        thread.start()

    def _run(self, interval):
        while self.running:
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

            time.sleep(interval)

    def get_latest_data(self):
        return self.data[-1] if self.data else None

    def get_orderbook(self):
        return self.bids, self.asks


# ----------------------
# Analytics
# ----------------------
class MarketAnalytics:
    def __init__(self, simulator, max_points=100):
        self.simulator = simulator
        self.max_points = max_points
        self.prices = deque(maxlen=max_points)
        self.timestamps = deque(maxlen=max_points)
        self.volumes = deque(maxlen=max_points)

    def update(self):
        data = self.simulator.get_latest_data()
        if data:
            self.prices.append(data["price"])
            self.timestamps.append(data["timestamp"])
            self.volumes.append(data["volume"])

    def get_price_series(self):
        return list(self.timestamps), list(self.prices)

    def get_volume_series(self):
        return list(self.timestamps), list(self.volumes)

    def get_orderbook(self):
        return self.simulator.get_orderbook()


# ----------------------
# Setup Simulator + Analytics
# ----------------------
simulator = MarketSimulator()
analytics = MarketAnalytics(simulator)

# Start simulator in background
simulator.start(interval=1)

# ----------------------
# Dash App
# ----------------------
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H2("High-End Real-Time Market Dashboard"),
    dcc.Graph(id="price-graph"),
    dcc.Graph(id="orderbook-graph"),
    dcc.Interval(id="interval-component", interval=1000, n_intervals=0)  # update every 1s
])

@app.callback(
    [Output("price-graph", "figure"),
     Output("orderbook-graph", "figure")],
    [Input("interval-component", "n_intervals")]
)
def update_graph(n):
    # Update analytics with latest data
    analytics.update()

    # Price Graph
    times, prices = analytics.get_price_series()
    fig_price = go.Figure()
    if times and prices:
        fig_price.add_trace(go.Scatter(x=times, y=prices, mode="lines+markers", name="Price"))
    fig_price.update_layout(title="Price over Time", xaxis_title="Time", yaxis_title="Price")

    # Order Book Graph
    bids, asks = analytics.get_orderbook()
    fig_book = go.Figure()
    if bids and asks:
        fig_book.add_trace(go.Bar(x=[b[1] for b in bids], y=[b[0] for b in bids],
                                  name="Bids", orientation="h"))
        fig_book.add_trace(go.Bar(x=[a[1] for a in asks], y=[a[0] for a in asks],
                                  name="Asks", orientation="h"))
    fig_book.update_layout(title="Order Book", barmode="overlay",
                           xaxis_title="Volume", yaxis_title="Price")

    return fig_price, fig_book


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)
