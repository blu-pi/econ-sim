import random
from typing import Union, Any
from program.code.game_theory import DecisionMatrix

#from program.code.agent_actions_interface import ActionInterface

#interface
class Agent:
    """
    General Interface to define what are/ aren't Agents in general. Mostly used for type comparisons. Stores list containing all sellers and buyers
    in class attributes (sellers_arr, buyers_arr). Agent decision making is done in this class by looping through those lists.
    """

    #TODO for valid args in buyers and sellers, eiter remove them as functionality is in graph class or use them for more specific arg restrictions (e.g. min/max values or sub parameters etc.)

    sellers_arr = []
    buyers_arr = []

    @staticmethod
    def agentChoices() -> None:
        """
        Loop through all agents in the simulation and have them make choices one at a time. Sellers make choices before buyers. No agent ever has 
        access to the choice another has made in the same cycle, they happen 'simultaniously' for the sake of the simulatoin. This prevents the order 
        in which agents make choices influencing results. Returns whether this was performed successfully.
        """
        if Seller.sequential_decisions:
            random.shuffle(Agent.sellers_arr)#prevents order of agent creation impacting simulation results. Makes simulation non-deterministic!
        for seller in Agent.sellers_arr:
            action = seller.findBestAction()
        for buyer in Agent.buyers_arr:
            action = buyer.findBestAction()
        action.apply()
            

class Seller(Agent):
    """
    Class defining an Individual Seller in the simulation. Seller behaviour can be modified depending on input passed to constructor.
    This is done through the 'arg_dict' dictionary which is an optional parameter in the constructor. valid keys for that dictionary are defined in the
    'valid_args' class attribute. Inherits from Agent.
    """

    sequential_decisions : bool = False #applies to all Sellers TODO change var depending on arg_dict!
    valid_args = []

    def __init__(self, arg_dict = {}) -> None:
        self.arg_dict = arg_dict
        self.product_price = 0
        self.price_change_amount = 1
        self.buyers = []
        Agent.sellers_arr.append(self)
        self.arr_pos = len(Agent.sellers_arr) - 1
        self.action_history = []

    #Sellers are instantiated before buyers so the Buyers that are 'connected' to this Seller must be added retrospectively 
    def setBuyer(self, buyer : Union[Any,list]) -> None:
        '''Method for populating Seller.buyers array which is empty when the Seller objects are first initialised.'''
        if isinstance(buyer, Buyer):
            self.buyers.append(buyer)
        elif isinstance(buyer, list):
            for b in buyer:
                assert(isinstance(b, Buyer))
                self.buyers.append(b)
       
    def getOpponents(self) -> Any: #supposed to return list of sellers
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
        from program.code.actions import SellerAction, AgentAction

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

    def findBestAction(self):
        """Returns action object that the Seller can perform which was calculated to be the best. """
        #TODO clean up this method (low priority). It should be split up bc it does to much at once right now.

        from program.code.actions import PriceChange, Idle, SellerAction
        from program.code.game_theory import DecisionMatrix
        
        #generate possible actions
        num_steps = 1 #default
        if "price_steps" in self.arg_dict:
            if not self.arg_dict["price_steps"] > 0:
                print("ERROR, invalid quantity for argument 'price steps'. {} is below minimum of 1.".format(self.arg_dict["price_steps"]))
                print("Default value of {} used instead.".format(num_steps))
            else:
                num_steps = self.arg_dict["price_steps"] 
        
        action_obj_arr = [Idle(self)]
        change = 0
        interval : float = self.price_change_amount / num_steps #TODO ensure price_change_amount is > 0 as a rule?
        for i in range(num_steps):
            change += interval
            action_obj_arr.append(PriceChange(self, change))
            action_obj_arr.append(PriceChange(self, change * -1))       
        assert(len(action_obj_arr) == 1 + (num_steps * 2))

        matrices = self.makeMatrices(action_obj_arr) #only needed during simultaneous decision making!
        if not Seller.sequential_decisions and "PERFECT_INFORMATION" in self.arg_dict:
            print("ERROR, NOT IMPLEMENTED!")
            exit(0)
        elif Seller.sequential_decisions and "PERFECT_INFORMATION" in self.arg_dict:
            max_util = -1 #nothing will be smaller than this
            best_action = None
            for action in action_obj_arr:
                util = action.eval()
                if util > max_util:
                    best_action = action
                    max_util = util
            return best_action #TODO test this!!!
        else: #FOR ALL CASES WHERE IMPERFECT INFORMATION IS USED
            pass
            #Uses behaviour
    
    #IMPORTANT! ALL sellers are equal before they become a node in a graph! That is because they are only assigned sellers then. 
    #Their prices only change when the simulation starts (even later than being placed in a graph chronologically).
    #So basically don't bother comparing sellers until they become Graph Nodes.
    def __eq__(self, other) -> bool:
        if isinstance(other, Seller):
            return self.buyers == other.buyers and self.product_price == other.product_price
        return False

    def __str__(self) -> str:
        return "Seller" + str(self.arr_pos)

    @staticmethod
    def setSequential() -> None: #TODO actually call this method when nessecary when simulation is being setup. Possibly in simulation class?
        Seller.sequential_decisions = True


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
        self.informSellers()
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
            self.percieved_utility = self.arg_dict["percieved_util"] #user-generated method call (explicit)

        elif util:
            self.percieved_utility = util #probably implicit method call
            
        else:
            if "min_util" in self.arg_dict:
                temp_min_util = self.arg_dict["min_util"]
            if "max_util" in self.arg_dict:
                temp_max_util = self.arg_dict["max_util"]

            if temp_max_util >= temp_min_util:
                max_util = temp_max_util
                min_util = temp_min_util

            self.percieved_utility = random.randint(min_util, max_util)
    
    def informSellers(self) -> None:
        """Gives seller a direct reference to this obj. Acts as an intention to buy from them."""
        for seller in self.buys_from:
            assert(isinstance(seller,Seller))
            seller.setBuyer(self)

    def findBestAction(self): #No typing because imports are made later
        """Returns action object that the Buyer can perform which was calculated to be the best."""
        from program.code.actions import Buy, Idle
        action_obj_arr = []
        action_values_arr = []
        buy_action = Buy(self)
        idle_action = Idle(self)
        action_obj_arr.extend([buy_action, idle_action])
        for obj in action_obj_arr:
            action_values_arr.append(obj.eval())
        return action_obj_arr[action_values_arr.index(max(action_values_arr))] #return action object with highest predicted value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Buyer):
            return self.buys_from == other.buys_from and self.percieved_utility == other.percieved_utility
        return False

    def __str__(self) -> str:
        return "Buyer" + str(self.arr_pos)

    @staticmethod
    def stringToClassReference(val : str) -> Any:
        """Returns static reference to class given it's string name. May or may not be needed at some point."""
        try:
            return eval(val) #different eval to the methods in Actions class
        except:
            print("Warning: Class name {val} could not be referenced! Either it can't be accessed or it doesn't exist.".format(val=val))
            return None
