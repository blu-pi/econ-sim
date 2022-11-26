from program.code.agents import Seller, Buyer

#interface
class Action():

    types = []


#interface
class BuyerAction(Action):

    possible_actions = []

class Buy(BuyerAction):

    def __init__(self, agent : Buyer, seller_ag : Seller) -> None:
        self.agent = agent
        self.seller = seller_ag
        self.price = seller_ag.product_price
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Buy) and self.agent == other.agent and self.seller == other.seller

    def __str__(self) -> str:
        return str(self.agent, "buying from", self.seller, "for price =", self.price)
    
    def apply(self) -> None:
        pass #TODO represent transactions completed vs not completed!

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
        out = str(self.agent, "PriceChannge by", self.amount)
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
class AgentAction(BuyerAction, SellerAction): #both can do these

    possible_actions = []

class Idle(AgentAction):

    def __init__(self) -> None:
        pass

    def apply(self):
        pass