import random

from program.code.actions import *

#interface
class Agent:
    """
    General Interface to define what are/ aren't Agents in general. Mostly used for type comparisons. Stores list containing all sellers and buyers
    in class attributes (sellers_arr, buyers_arr). Agent decision making is done in this class by looping through those lists.
    """

    sellers_arr = []
    buyers_arr = []

    @staticmethod
    def agentChoices() -> bool:
        seller_index, buyer_index = 0
        for seller in Agent.sellers_arr:
            action = seller.findBestAction()
        for buyer in Agent.buyers_arr:
            action = buyer.findBestAction()
        return True


class Seller(Agent):
    """
    Class defining an Individual Seller in the simulation. Seller behaviour can be modified depending on input passed to constructor.
    This is done through the 'arg_dict' dictionary which is an optional parameter in the constructor. valid keys for that dictionary are defined in the
    'valid_args' class attribute. Inherits from Agent.
    """

    valid_args = []

    def __init__(self, arg_dict = {}) -> None:
        self.arg_dict = arg_dict
        self.product_price = 0
        self.buyers = []
        Agent.sellers_arr.append(self)
        self.arr_pos = len(Agent.sellers_arr) - 1
        self.action_history = []

    #Sellers are instantiated before buyers so the Buyers that are 'connected' to this Seller must be added retrospectively 
    def setBuyer(self, buyer) -> bool:
        if isinstance(buyer, Buyer):
            self.buyers.append(buyer)
            return True
        return False

    def findBestAction(self):
        #done on 2 lines to preserve original lists in their classes
        actions = SellerAction.possible_actions
        actions.append(AgentAction.possible_actions)
        #TODO carry on
    
    #IMPORTANT! ALL sellers are equal before they become a node in a graph! That is because they are only assigned sellers then. 
    #Their prices only change when the simulation starts (even later than being placed in a graph chronologically).
    #So basically don't bother comparing sellers until they become Graph Nodes.
    def __eq__(self, other) -> bool:
        if isinstance(other, Seller):
            return self.buyers == other.buyers and self.product_price == other.product_price
        return False

    def __str__(self) -> str:
        return "Seller" + str(self.arr_pos)


class Buyer(Agent):
    """
    Class defining an Individual Buyer in the simulation. Buyer behaviour can be modified depending on input passed to constructor.
    This is done through the 'arg_dict' dictionary which is an optional parameter in the constructor. valid keys for that dictionary are defined in the
    'valid_args' class attribute. Inherits from Agent.
    """

    valid_args = []

    def __init__(self, buys_from_arr, arg_dict = {}) -> None:
        self.buys_from = buys_from_arr
        self.arg_dict = arg_dict
        self.setPercievedUtility()
        Agent.buyers_arr.append(self)
        self.arr_pos = len(Agent.buyers_arr) - 1
        self.bought_products = False
        self.action_history = []

    def setPercievedUtility(self, util = False, min_util = 1, max_util = 10) -> None:
        """
        Each buyer must have a percieved utility of owning both products they demand for the simulation to work. 
        It's a representation of how much they value those 2 goods in a bundle.
        This method assigns a random value in the default range 1 - 10.
        The range can be specified using the optional args 'min_util' and 'max_util'.
        If a specific util value is provided in the optional args for the Buyer's constructor then that value is used instead.
        If a specific util value can be provided using optional argument 'util' but it won't be used if a value is specified in the
        previously mentioned case.
        """

        if "percieved_util" in self.arg_dict:
            self.percieved_utility = self.arg_dict["percieved_util"]
        elif util:
            self.percieved_utility = util
        else:
            if "min_util" in self.arg_dict:
                min_util = self.arg_dict["min_util"]
            if "max_util" in self.arg_dict:
                min_util = self.arg_dict["max_util"]
            self.percieved_utility = random.randint(min_util, max_util)

    def findBestAction(self):
        actions = BuyerAction.possible_actions
        actions.append(AgentAction.possible_actions)
        #TODO carry on
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Buyer):
            return self.buys_from == other.buys_from and self.percieved_utility == other.percieved_utility
        return False

    def __str__(self) -> str:
        return "Buyer" + str(self.arr_pos)
