class OrderBook:
    def __init__(self, depth=5):
        self.depth = depth
        self.books = {}

    def update(self, symbol, price):
        if symbol not in self.books:
            self.books[symbol] = {"bids": [], "asks": []}
        # fake bid/ask data around current price
        self.books[symbol]["bids"] = [round(price - i, 2) for i in range(self.depth)]
        self.books[symbol]["asks"] = [round(price + i, 2) for i in range(self.depth)]

    def get_book(self, symbol):
        return self.books.get(symbol, {"bids": [], "asks": []})
