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

        self.informSellers() #give corresponding seller objects a reference to this obj

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

    def informSellers(self) -> None:
        """Give corresponding seller objects a reference to this object for future use"""
        for seller in self.buys_from:
            assert(isinstance(seller,Seller))
            seller.setBuyerCollection(self)

    def getSellerUtil(self, price : float) -> float:
        """Returns total seller (plural) utility gained from this collection at given price."""
        total = 0
        for buyer in self.buyers:
            if price <= buyer.percieved_utility:
                total += price
        return total
    
    @staticmethod
    def _show_output(prices, utilities) -> None:
        """Create pyplot for given prices and utilities."""
        plt.xlim(0, max(prices))
        plt.ylim(0, max(utilities))

        plt.grid()

        plt.xlabel("Product price")
        plt.ylabel("Seller utility")

        plt.plot(prices, utilities)
        plt.show()
        

    def makeGraph(self, price_limits : Tuple[float,float] = (0,100), interval : float = 1, show_output : bool = False) -> Tuple[float,float]:
        """Get values for utility returned for a given range of prices."""
        total_price = 0
        prices = []
        utilities = []
        for total_price in np.arange(price_limits[0], price_limits[1], interval, dtype=float):      
            prices.append(total_price)
            utilities.append(self.getSellerUtil(total_price))
        
        if show_output: 
            BuyerCollection._show_output(prices, utilities)

        return prices, utilities
    
    def makeComboGraph(self, others : list['BuyerCollection'], price_limits : Tuple[float,float] = (0,100), interval : float = 1, show_output : bool = False) -> Tuple[float,float]:
        """
        Make a combined price/util graph for at least 2 collections joined. Only really useful if collections share 1 common Seller.
        """
        sellers = self.buys_from.copy()
        prices, utilities = self.makeGraph(price_limits, interval) #never show output here
        for obj in others:
            other_prices, other_utilities = obj.makeGraph(price_limits, interval)
            other_sellers = obj.buys_from 

            #FeelsHaskellMan       
            sellers = [x for x in other_sellers if x in sellers]
            prices = [sum(x) for x in zip(prices, other_prices)]
            utilities = [sum(x) for x in zip(utilities, other_utilities)]

        if sellers == []:
            print("Warning, combined data of unrelated BuyerCollections!")

        if show_output: 
            BuyerCollection._show_output(prices, utilities)
        
        return prices, utilities
    
    @staticmethod
    def makeComboGraphFromList(list_in : list['BuyerCollection'], price_limits : Tuple[float,float] = (0,100), interval : float = 1, show_output : bool = False) -> Tuple[float,float]:
        """Use makeComboGraph using just a list of BuyerCollections"""
        assert(len(list_in) > 0)
        if len(list_in) > 1:
            temp_in = list_in.copy()
            obj_ref = temp_in.pop(0)
            others = temp_in #doesn't need top be done but is more readable. Point is .pop already removes that 1st element. This makes it clear that temp_in changes in contents to fulfill role as 'others' parameter.
            return obj_ref.makeComboGraph(others,price_limits, interval, show_output)
        if len(list_in) == 1:
            return list_in[0].makeGraph(price_limits, interval, show_output)