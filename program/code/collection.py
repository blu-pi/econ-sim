from program.code.agents import Seller, Buyer, Agent
from program.code.actions import PriceChange
from program.code.distribution import Distribution, Linear, Exponential

import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple

class BuyerCollection:
    """A collection of buyers that all buy from exactly the same Sellers."""

    def __init__(self, buyers : list[Buyer], util_dist : Distribution = None) -> None:
        assert(len(buyers) > 0)

        if isinstance(util_dist,str): #idk why the code lets this even happen but it does
            util_dist = None

        self.buyers = buyers
        self.buys_from = self.buyers[0].buys_from

        self.util_dist = util_dist
        if util_dist == None and len(buyers) > 1: #if len buyers is 1 then Random is forced.
            dist_str = self.buyers[0].arg_dict["util_distribution"]
            args = {
                "start" : self.buyers[0].min_util,
                "end" : self.buyers[0].max_util,
                "steps" : len(buyers)
            }
            if dist_str == "Exponential":
                self.util_dist = Exponential(**args)
            elif dist_str == "Linear":
                self.util_dist = Linear(**args)

        if not self._validateCollection():
            print("Collection doesn't contain matching Buyers. Critical error!") #no point catching this, it's over anyway.
            exit()

        if self.util_dist != None:
            self._overrideUtilities()

    def _validateCollection(self) -> bool:
        for buyer in self.buyers:
            if buyer.buys_from != self.buys_from:
                return False
        return True

    def _overrideUtilities(self) -> None:
        """
        When applying a distribution to Buyer utility it is done retrospectively. 
        This means an initial value was likely already created. However, it doesn't matter if they weren't.
        """
        assert(len(self.buyers) == len(self.util_dist.values))

        for buyer,util in zip(self.buyers,self.util_dist.values):
            buyer.setPercievedUtility(util=util)

    def getSellerUtil(self, price : float) -> float:
        """Returns total seller (plural) utility gained from this collection at given price."""
        total = 0
        for buyer in self.buyers:
            if price <= buyer.percieved_utility:
                total += price
        return total

    def makeGraph(self, price_limits : Tuple[float,float] = (0,100), interval : float = 1, show_output : bool = False) -> tuple:
        """Get values for utility returned for a given range of prices"""
        total_price = 0
        prices = []
        utilities = []
        for total_price in np.arange(price_limits[0], price_limits[1], interval, dtype=float):      
            prices.append(total_price)
            utilities.append(self.getSellerUtil(total_price))
        
        if show_output: 
            plt.xlim(0, max(prices))
            plt.ylim(0, max(utilities))

            plt.grid()

            plt.xlabel("Product price")
            plt.ylabel("Seller utility")

            #for i in range(len(prices)):
            plt.plot(prices, utilities)
            plt.show()

        return prices, utilities