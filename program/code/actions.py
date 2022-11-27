from typing import Union
from program.code.agents import Seller, Buyer

#interface
class Action():

    types = []


#interface
class BuyerAction(Action):

    possible_actions = []

class Buy(BuyerAction):

    def __init__(self, agent : Buyer) -> None:
        self.agent = agent
        self.seller1 : Seller = agent.buys_from[0]
        self.seller2 : Seller = agent.buys_from[1]
        self.cost = self.seller1.product_price + self.seller2.product_price
    
    def __eq__(self, other) -> bool:
        class_check = isinstance(other, Buy) 
        other_sellers = [other.seller1, other.seller2]
        return class_check and self.agent == other.agent and (
            self.seller1 in other_sellers and self.seller2 in other_sellers)

    def __str__(self) -> str:
        return "{0} bought from {1} and {2} for price = {3}".format(self.agent, self.seller1, self.seller2, self.cost)
    
    def apply(self) -> None:
        self.agent.bought_products = True
        self.agent.action_history.append(self)


#interface
class SellerAction(Action):

    possible_actions = []

class PriceChange(SellerAction):

    def __init__(self, agent : Seller, amount, is_percentage : bool = False) -> None:
        assert amount != 0
        self.agent = agent
        self.amount = amount
        self.is_percentage = is_percentage

    def __eq__(self, other) -> bool: #provisional
        return isinstance(other, PriceChange) and (
            self.agent == other.agent and self.amount == other.amount and self.is_percentage == other.is_percentage)
    
    def __str__(self) -> str:
        out = "{0} changed price by {1}".format(self.agent, self.amount)
        if self.is_percentage:
            out += "%"
        return out
    
    def apply(self) -> None:
        if self.is_percentage:
            self.agent.product_price *= 1 + (self.amount / 100)
        else:
            self.agent.product_price += self.amount
        self.agent.action_history.append(self)

#interface
class AgentAction(Action): #both can do these

    possible_actions = []

class Idle(AgentAction):

    def __init__(self, agent : Union[Buyer, Seller]) -> None:
        self.agent = agent

    def __str__(self) -> str:
        return str(self.agent) + " did nothing"

    def apply(self):
        self.agent.action_history.append(self)