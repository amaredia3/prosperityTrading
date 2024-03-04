from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import math
import string

class Trader:

    def moving_avg(self, days_back, historical_price):
        """
        Given a products historical price, calculate moving averages for X days
        """
        return 10
    
    def fair_market_value(self, order_depth):
        """
        Given a product's order book, evaluate fair value per unit based on open buy/sell orders.
        """
        weighted_buy_sum = 0
        total_buy_units = 0
        for buy_order in order_depth.buy_orders:
            weighted_buy_sum += buy_order * order_depth.buy_orders[buy_order]
            total_buy_units += order_depth.buy_orders[buy_order]
        weighted_sell_sum = 0
        total_sell_units = 0
        for sell_order in order_depth.sell_orders:
            weighted_sell_sum += sell_order * -order_depth.sell_orders[sell_order]
            total_sell_units += -order_depth.sell_orders[sell_order]
        return (weighted_buy_sum / total_buy_units) + abs((weighted_buy_sum / total_buy_units) - (weighted_sell_sum / total_sell_units))
    
    def buy_order(acceptable_price, sell_orders):
        num_units = 0
        for ask in sell_orders:
            if ask < acceptable_price:
                num_units += sell_orders[ask]
        return num_units
    
    def sell_order(acceptable_price, buy_orders):
        num_units = 0
        for bid in buy_orders:
            if bid > acceptable_price:
                num_units += buy_orders[bid]
        return num_units
    
    def run(self, state: TradingState):
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

				# Orders to be placed on exchange matching engine
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            # Initialize the list of Orders to be sent as an empty list
            orders: List[Order] = []
            # Define a fair value for the PRODUCT. Might be different for each tradable item
            # Note that this value of 10 is just a dummy value, you should likely change it!
            acceptable_price = self.fair_market_value(order_depth)
            buy_quantity = self.buy_order(acceptable_price, order_depth.sell_orders)
            if buy_quantity > 0:
                orders.append(Order(product, math.floor(acceptable_price), buy_quantity))
            sell_quantity = self.sell_order(acceptable_price, order_depth.buy_orders)
            if sell_quantity > 0:
                orders.append(Order(product, math.ceil(acceptable_price), -sell_quantity))
						# All print statements output will be delivered inside test results
            # print("Acceptable price : " + str(acceptable_price))
            # print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
            # print("Matching sell orders : " + str())
						# Order depth list come already sorted. 
						# We can simply pick first item to check first item to get best bid or offer
            # if len(order_depth.sell_orders) != 0:
            #     best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
            #     if int(best_ask) < acceptable_price:
            #         # In case the lowest ask is lower than our fair value,
            #         # This presents an opportunity for us to buy cheaply
            #         # The code below therefore sends a BUY order at the price level of the ask,
            #         # with the same quantity
            #         # We expect this order to trade with the sell order
            #         print("BUY", str(-best_ask_amount) + "x", best_ask)
            #         orders.append(Order(product, best_ask, -best_ask_amount))
    
            # if len(order_depth.buy_orders) != 0:
            #     best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
            #     if int(best_bid) > acceptable_price:
			# 							# Similar situation with sell orders
            #         print("SELL", str(best_bid_amount) + "x", best_bid)
            #         orders.append(Order(product, best_bid, -best_bid_amount))
            
            result[product] = orders
    
		    # String value holding Trader state data required. 
				# It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE" 
        
				# Sample conversion request. Check more details below. 
        conversions = 0
        return result, conversions, traderData
