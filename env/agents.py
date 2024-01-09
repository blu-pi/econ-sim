import random
from typing import Union, Any
import numpy as np
import statistics

from structs.game_theory import DecisionMatrix

#from program.code.agent_actions_interface import ActionInterface

#interface
class Agent:
    """
    General Interface to define what are/ aren't Agents in general. Mostly used for type comparisons. Stores list containing all sellers and buyers
    in class attributes (sellers_arr, buyers_arr). Agent decision making is done in this class by looping through those lists.
    """

    sellers_arr = []
    buyers_arr = []
    buyer_collections_arr = []


class Seller(Agent):
    """
    Class defining an Individual Seller in the simulation. Seller behaviour can be modified depending on input passed to constructor.
    This is done through the 'arg_dict' dictionary which is an optional parameter in the constructor. valid keys for that dictionary are defined in the
    'valid_args' class attribute. Inherits from Agent.
    """

    valid_args = []

    def __init__(self, arg_dict = {}) -> None:
        self.arg_dict = arg_dict

        #defaults (Must have values even if not passed by arg_dict) !these dicts are totally OPTIONAL to the function of the program!
        self.product_price = 0
        self.price_change_amount = 1
        self.price_steps = 1    

        #overwrite defaults using passed parameters
        for key in arg_dict:
            setattr(self, key, arg_dict[key])

        self.buyers = []
        Agent.sellers_arr.append(self)
        self.arr_pos = len(Agent.sellers_arr) - 1
        self.prices = []
        self.profits = []
        self.action_history = []
        self.buyer_collections = []

    #Sellers are instantiated before buyers so the Buyers that are 'connected' to this Seller must be added retrospectively 
    def setBuyer(self, buyer : Union[Any,list]) -> None:
        '''Method for populating Seller.buyers array which is empty when the Seller objects are first initialised.'''
        if isinstance(buyer, Buyer):
            self.buyers.append(buyer)
        elif isinstance(buyer, list):
            for b in buyer:
                assert(isinstance(b, Buyer))
                self.buyers.append(b)

    def setBuyerCollection(self, collection):
        from env.collection import BuyerCollection
        assert(isinstance(collection, BuyerCollection))
        self.buyer_collections.append(collection)

    def getMoney(self, amount : float) -> None:
        self.profits[-1] += amount
       
    def getOpponents(self) -> list: #supposed to return list of sellers
        """
        Method that returns a Seller object for each Buyer object of the original Seller. This way the Seller can make a Decision Matrix
        to compete with all sellers over each Buyer being competed over. Allows duplicates!
        """
        out = []
        for buyer in self.buyers:
            assert isinstance(buyer, Buyer) #honestly just to get vscode to understand the type
            sellers : list[Seller] = buyer.buys_from.copy()
            sellers.remove(self) #remove seller making the decision from the list
            out.extend(sellers)
        #assert isinstance(out, list[Seller])
        return out
    
    def makeMatrices(self, actions) -> list[DecisionMatrix]:
        """Makes empty decision matrix out of a seller obj and a list of action objs. Utilies aren't entered"""

        #assert isinstance(actions, list[Union[SellerAction,AgentAction]]) #fix
        num_actions = len(actions)
        str_actions = []
        for action in actions:
            str_actions.append(str(action))
        opponents = self.getOpponents()
        matrices = []
        i = 0
        for opp in opponents: 
            decision_matrix = DecisionMatrix(num_actions, str_actions)
            matrices.append(decision_matrix) #technically just an array containing arrays, containing arrays, containing arrays - fun
        return matrices

    def findBestAction(self, isSequential : bool):
        """Returns action object that the Seller can perform which was calculated to be the best. """
        #TODO clean up this method (low priority). It should be split up bc it does to much at once right now. (old todo)
        #TODO use buyer collections to do stuff

        from env.actions import PriceChange, Idle, SellerAction
        from structs.game_theory import DecisionMatrix
        
        #generate possible actions    
        action_obj_arr = [Idle(self)]
        change = 0
        interval : float = self.price_change_amount / self.price_steps #TODO ensure price_change_amount is > 0 as a rule?
        for i in range(self.price_steps):
            change += interval
            action_obj_arr.append(PriceChange(self, change))
            action_obj_arr.append(PriceChange(self, change * -1))     
        assert(len(action_obj_arr) == 1 + (self.price_steps * 2))

        matrices = self.makeMatrices(action_obj_arr) #only needed during simultaneous decision making!
        if not isSequential and "PERFECT_INFORMATION" in self.arg_dict:
            print("ERROR, NOT IMPLEMENTED!")
            exit(0)
        elif isSequential and "PERFECT_INFORMATION" in self.arg_dict:
            max_util = -1 #nothing will be smaller than this
            best_action = None
            for action in action_obj_arr:
                util = action.eval(isSequential)
                if util > max_util:
                    best_action = action
                    max_util = util
            return best_action
        else: #FOR ALL CASES WHERE IMPERFECT INFORMATION IS USED
            pass
            #Uses behaviour
    
    def applyPerformanceMeasure(self, target_data : list[float] = None) -> float:
        """Return desired value representing performance from list containing profits over time"""
        #IMPORTANT, FINAL PROFIT IS ONLY VALID ON DATA OVER TIME GRAPHS!
        if target_data is None:
            target_data = self.profits
        method = self.arg_dict["performance_measure"]
        if method == "final_profit":
            return target_data[-1]
        elif method == "max_profit":
            return max(target_data)
        elif method == "total_profit":
            return(target_data)
        else:
            print("ERROR INVALID SELLER PERFORMANCE MEASURE")
            exit(0)
    
    def __str__(self) -> str:
        return "Seller" + str(self.arr_pos)
        
    @staticmethod
    def getProfits() -> list[int]:
        """Get a target profit value from each Seller which will later be used to determine Seller performance"""
        profits = []
        for seller in Agent.sellers_arr:
            seller : Seller #so vsc understands (not important)
            profits.append(seller.applyPerformanceMeasure())
        return profits

    #---------    SELLER STAT COLLECTION + PROCESSING    ---------

    @staticmethod
    def getClassStats() -> dict:
        """Get data that is the same for all objects across the seller class."""
        rand_obj = Agent.sellers_arr[0]
        out = {
            "information" : rand_obj.arg_dict["PERFECT_INFORMATION"]
        }
        return out
    
    @staticmethod
    def getIndividualStats(get_complex : bool = True) -> list:
        out = []
        for obj in Agent.sellers_arr:
            obj : Seller
            out.append(obj.getStats(get_complex))
        return out
    
    def getStats(self, get_complex : bool = True) -> dict:
        out = {
            "prices" : self.prices,
            "profits" : self.profits,
            "num_customers" : len(self.buyers),
            "num_direct_competitors" : len(self.buyer_collections)
        }
        if get_complex:
            out.update(self._getComplexStats())
        return out
    
    def _getComplexStats(self) -> dict:
        #doesn't work for new output UI
        from env.collection import BuyerCollection
        from structs.data_plot import NamedDataPlot
        combined_plot : NamedDataPlot = BuyerCollection.makeComboPlotFromList(self.buyer_collections)
        out = {
            "price_to_profit_plot" : combined_plot
        }
        return out


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
        self.collection = None #optionally overwritten later. No big deal if it isn't.
        self.setPercievedUtility()
        self.informSellers()
        Agent.buyers_arr.append(self)
        self.arr_pos = len(Agent.buyers_arr) - 1
        self.bought_products = False
        self.action_history = []


    def setPercievedUtility(self, util : float = None, min_util = 1, max_util = 10) -> None:
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
            self.percieved_utility = self.arg_dict["percieved_util"] #user-generated method call (explicit)

        elif util != None: #could be it's own method honestly
            self.percieved_utility = util #implicit call, usually happens when "util_distribution" arg is set to something that isn't "Random".
            
        else:
            temp_min_util = min_util
            temp_max_util = max_util
            if "min_util" in self.arg_dict:
                temp_min_util = self.arg_dict["min_util"]
            if "max_util" in self.arg_dict:
                temp_max_util = self.arg_dict["max_util"]

            if temp_max_util >= temp_min_util:
                max_util = temp_max_util
                min_util = temp_min_util
            
            #used for buyercollections
            self.min_util = min_util
            self.max_util = max_util

            self.percieved_utility = random.randint(min_util, max_util)

    def setCollection(self, collection) -> None:
        """records assignment of Buyer to a designated BuyerCollection"""
        from env.collection import BuyerCollection
        assert(isinstance(collection, BuyerCollection))
        self.collection = collection
    
    def informSellers(self) -> None:
        """Gives seller a direct reference to this obj. Acts as an intention to buy from them."""
        for seller in self.buys_from:
            assert(isinstance(seller,Seller))
            seller.setBuyer(self)

    def findBestAction(self): #No typing because imports are made later
        """Returns action object that the Buyer can perform which was calculated to be the best."""
        from env.actions import Buy, Idle
        action_obj_arr = []
        action_values_arr = []
        buy_action = Buy(self)
        idle_action = Idle(self)
        action_obj_arr.extend([buy_action, idle_action])
        for obj in action_obj_arr:
            action_values_arr.append(obj.eval())
        return action_obj_arr[action_values_arr.index(max(action_values_arr))] #return action object with highest predicted value
    
    #---------    BUYER STAT COLLECTION + PROCESSING    ---------
    @staticmethod
    def getClassStats() -> dict:
        out = {
            "num_buyers" : len(Seller.buyers_arr),
            "num_edges" : len(Seller.buyer_collections_arr),
            "Buyers_per_edge" : len(Agent.buyers_arr) / len(Agent.buyer_collections_arr)
        }
        return out
    
    def getCollectionStats(self) -> dict:
        #TODO implement if going deeper into Buyer behaviour is needed.
        out = {
        }
        return out

    def __str__(self) -> str:
        return "Buyer" + str(self.arr_pos)

    #---------    Random code I may or may not need    ---------
    @staticmethod
    def stringToClassReference(val : str) -> Any:
        """Returns static reference to class given it's string name. May or may not be needed at some point."""
        try:
            return eval(val) #different eval to the methods in Actions class
        except:
            print("Warning: Class name {val} could not be referenced! Either it can't be accessed or it doesn't exist.".format(val=val))
            return None
