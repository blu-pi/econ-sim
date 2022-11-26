import random

#interface
class Agent:

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

    valid_args = []

    def __init__(self, arg_dict = {}) -> None:
        self.arg_dict = arg_dict
        self.product_price = 0
        self.buyers = []
        Agent.sellers_arr.append(self)
        self.arr_pos = len(Agent.sellers_arr) - 1
        self.action_history = []

    def setBuyer(self, buyer) -> bool:
        if isinstance(buyer, Buyer):
            self.buyers.append(buyer)
            return True
        return False

    def findBestAction(self):
        pass
    
    #IMPORTANT! ALL sellers are equal before they become a node in a graph! That is because they are only assigned sellers then. 
    #Their prices only change when the simulation starts (even later chronologically).
    #So basically don't bother comparing sellers until they become Graph Nodes.
    def __eq__(self, other) -> bool:
        if isinstance(other, Seller):
            return self.buyers == other.buyers and self.product_price == other.product_price
        return False

    def __str__(self) -> str:
        return "Seller" + str(self.arr_pos)


class Buyer(Agent):

    valid_args = []

    def __init__(self, buys_from_arr, arg_dict = {}) -> None:
        self.buys_from = buys_from_arr
        self.arg_dict = arg_dict
        self.setPercievedUtility()
        Agent.buyers_arr.append(self)
        self.arr_pos = len(Agent.buyers_arr) - 1
        self.action_history = []

    def setPercievedUtility(self, util = False, min_util = 1, max_util = 10) -> None:
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
        pass
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Buyer):
            return self.buys_from == other.buys_from and self.percieved_utility == other.percieved_utility
        return False

    def __str__(self) -> str:
        return "Buyer" + str(self.arr_pos)
