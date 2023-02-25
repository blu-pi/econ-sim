from program.code.agents import Seller, Buyer, Agent
from program.code.actions import PriceChange
from program.code.distribution import Distribution, Linear, Exponential

import numpy as np
import matplotlib.pyplot as plt

class BuyerCollection:
    """A collection of buyers that all buy from exactly the same Sellers."""

    def __init__(self, buyers : list[Buyer], util_dist : Distribution = None) -> None:
        assert(len(buyers) > 0)

        self.util_dist = util_dist
        if util_dist == "Vanilla":
            self.util_dist = None

        self.buyers = buyers
        self.buys_from = self.buyers[0].buys_from

        if not self._validateCollection():
            print("Collection doesn't contain matching Buyers. Critical error!") #no point catching this, it's over anyway.
            exit()

        self._overrideUtilities(util_dist)

    def _validateCollection(self) -> bool:
        for buyer in self.buyers:
            if buyer.buys_from != self.buys_from:
                return False
        return True

    def _overrideUtilities(self, distribution : Distribution) -> None:
        """
        When applying a distribution to Buyer utility it is done retrospectively. 
        This means an initial value was likely already created. However, it doesn't matter if they weren't.
        """
        assert(distribution.values != None)
        assert(len(self.buyers) == len(distribution.values))

        for buyer,util in zip(self.buyers,distribution.values):
            buyer.setPercievedUtility(util=util)

    def makeGraph(self, show_output : bool = False) -> tuple:
        pass#TODO