from typing import Union, Any

from program.code.agents import Seller, Buyer
from program.code.opt_args import OptArg

#interface
class Action():
    """
    General Interface to define what are/ aren't Actions in general. Mostly used for type comparisons. 
    All Actions have some way to evaluate (eval) their predicted utility. Sometimes there is also a split between Objective and Estimated eval options.
    Perfect (Objective) eval will calculate a 100% accurate evaluation based on perfect information. Imperfect eval will estimate using limited information.
    The type of eval used depends on preconditions selected during the simulation set-up by the user. All Actions also have an apply method that applies a 
    prospective Action to a given Agent.
    """

    types = []


#interface
class BuyerAction(Action):
    """
    Interface to categorise different action types. In this case to define Buyer-specific Actions.
    Stores all implemented Actions for Buyers in posible_actions list (class attribute). Inherits from Action.
    """

    possible_actions = ["Buy"]

class Buy(BuyerAction):
    """Class which defines the buying Action for a Buyer object. Inherits from BuyerAction."""

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
        for seller in self.agent.buys_from:
            seller.getMoney(self.cost / 2)

    def eval(self) -> int:
        return self.agent.percieved_utility - self.cost

#interface
class SellerAction(Action):
    """
    Interface to categorise different action types. In this case to define Seller-specific Actions.
    Stores all implemented Actions for Sellers in posible_actions list (class attribute). Inherits from Action.
    """

class PriceChange(SellerAction):
    """Class which defines the price change Action for a Seller object. Inherits from SellerAction."""

    def __init__(self, agent : Seller, amount, is_percentage : bool = False) -> None:
        #assert amount != 0
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
        """Perform the specified action in the simulation"""
        if self.is_percentage:
            self.agent.product_price *= 1 + (self.amount / 100)
        else:
            self.agent.product_price += self.amount
        self.agent.action_history.append(self)

    def eval(self, isSequential : bool) -> Union[int,list[int]]:
        if isSequential:
            return self.seqEval()
        else:
            return self.simulEval()

    def simulEval(self) -> list[int]:     
        util = [0]
        if self.agent.arg_dict["PERFECT_INFORMATION"]: #if true
            print("1 ERROR, NOT IMPLEMENTED!")
            exit(0) #not implemented and very hard
        else:
            print("2 ERROR, NOT IMPLEMENTED!")
            exit(0) #TODO
        return util

    def seqEval(self) -> int:
        from program.code.collection import BuyerCollection
        util = 0
        if self.agent.arg_dict["PERFECT_INFORMATION"]: #if true
            #by far the easiest
            if self.is_percentage:
                new_price = self.agent.product_price * self.amount
            else:
                new_price = self.agent.product_price + self.amount

            for collection in self.agent.buyer_collections:
                assert(isinstance(collection, BuyerCollection))
                opponent : Seller = collection.getOpponent(self.agent)
                assert(opponent is not None)
                for buyer in collection.buyers:
                    assert(isinstance(buyer, Buyer))
                    if (opponent.product_price + new_price) <= buyer.percieved_utility:
                        util += new_price
                        
        else: #imperfect info
            print("3 ERROR, NOT IMPLEMENTED!")
            exit(0) #TODO
        #print("Checked {action} and found util of: {util}".format(action=self,util=util)) #this is debug output
        return util
    

#interface
class AgentAction(Action): #both can do these
    """
    Interface to categorise different action types. In this case to define Actions any type of Agent may perform.
    Stores all implemented non-type-specific (Any Agent) Actions in posible_actions list (class attribute). Inherits from Action.
    """

    possible_actions = ["Idle"]

class Idle(AgentAction):
    """Class which defines the idle (do nothing) Action for a Buyer or Seller object. Inherits from AgentAction."""

    def __init__(self, agent : Union[Buyer, Seller]) -> None:
        self.agent = agent

    def __str__(self) -> str:
        return str(self.agent) + " did nothing"

    def apply(self):
        self.agent.action_history.append(self)
    
    def eval(self, isSequential : bool = None) -> int:
        if isinstance(self.agent, Buyer):
            return 0
        else:
            temp_action = PriceChange(self.agent, 0)
            if isSequential:
                return temp_action.seqEval()