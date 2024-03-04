from typing import Dict, List

class OrderDepth:
    def __init__(self):
        self.buy_orders: Dict[int, int] = {}
        self.sell_orders: Dict[int, int] = {}

orderBook = OrderDepth()

orderBook.buy_orders = {9: 5, 10: 4}
orderBook.sell_orders = {12: -3, 11: -2}

weighted_buy_sum = 0
total_buy_units = 0
for buy_order in orderBook.buy_orders:
    weighted_buy_sum += buy_order * orderBook.buy_orders[buy_order]
    total_buy_units += orderBook.buy_orders[buy_order]
print("Buy avg: ", weighted_buy_sum / total_buy_units)

weighted_sell_sum = 0
total_sell_units = 0
for sell_order in orderBook.sell_orders:
    weighted_sell_sum += sell_order * -orderBook.sell_orders[sell_order]
    total_sell_units += -orderBook.sell_orders[sell_order]
print("Sell avg: ", weighted_sell_sum / total_sell_units)

