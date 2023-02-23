import sys
sys.path.append("./")

from program.code.agents import Seller, Buyer, Agent
from program.code.actions import PriceChange

import numpy as np
import matplotlib.pyplot as plt

#Visualise Local minima/maxima problem for Sellers. May later be used to explain concept to user. Can be used to try to verify if given args suffer from the problem or not. 

def currentUtil(seller : Seller) -> float:
    total = 0
    for buyer in seller.buyers:
        assert(isinstance(buyer,Buyer))
        if buyer.percieved_utility >= seller.product_price:
            total += seller.product_price
    return total

def linearDist(num_buyers : int, val_range = (0.0,10.0), buyer_args : dict = {}) -> None:
    assert(val_range[0] < val_range[1])
    assert(val_range[0] >= 0)
    assert(val_range[1] <= 100)
    seller = Seller()
    current_val = val_range[0]
    val_gradient = (val_range[1] - val_range[0]) / (num_buyers-1)
    for i in range(num_buyers):
        buyer_args.update({"percieved_util":current_val})
        print(current_val)
        buyer = Buyer([seller], buyer_args)
        current_val += val_gradient
    last_eval = None
    counter = 0
    prices = [0]
    utilities = [0]
    while seller.product_price * 1.1 < val_range[1]:
        action = PriceChange(seller,seller.price_change_amount)
        action.apply()
        prices.append(seller.product_price)
        utilities.append(currentUtil(seller))
    
    plt.xlim(0, max(prices))
    plt.ylim(0, max(utilities))

    plt.grid()

    plt.xlabel("Product price")
    plt.ylabel("Seller utility")

    #for i in range(len(prices)):
    plt.plot(prices, utilities)
    plt.show()


num_buyers = int(input("Enter number of Buyers: "))
min_util = int(input("Enter minimum Buyer util: "))
max_util = int(input("Enter maximum Buyer util: "))
linearDist(num_buyers,(min_util,max_util))

# x = np.arange(0, 5, 0.1)
# y = np.sin(x)
# fig, ax = plt.subplots()
# ax.plot(x, y)
# plt.show()