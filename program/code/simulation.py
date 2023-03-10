#from program.code.arg_checker import OptArgDict 
from program.code.opt_args import OptArg
from program.code.graphs import *
from program.code.agents import *

class Simulation:
    """
    Class that manages the simulation setup and end. 
    """

    def __init__(self, parameters, buyer_args = {}, seller_args = {}) -> None:
        self.parameters = parameters
        self.buyer_args = buyer_args
        self.seller_args = seller_args

        #DEFAULT VALUES, overwritten if value is passed through "parameters" dictionary
        self.max_turn = 50 
        self.num_sellers = 20 
        self.buyer_dist = "Random"
        self.graph_type = "Line"

        #overwrite defaults using passed parameters
        for key in parameters:
            setattr(self, key, parameters[key])

        self.turn_num = 0
        self.startSim()

    def setupSim(self) -> None:
        """
        Completes simulation setup including parameter verification and Graph creation. 
        Buyer and Seller args are checked later as they are totally optional and thus less important.
        """
        args = {
            "buyer_args" : self.buyer_args,
            "seller_args" : self.seller_args,
            "graph_args" : self.parameters,
            "num_sellers" : self.num_sellers
        } #passing sim args as graph args for now.
           
        if self.graph_type == "Line":
            graph = Line(**args)
        if self.graph_type == "Circle":
            graph = Line(**args, isCircle=True)
        if self.graph_type == "Tree":
            graph = Tree(**args)
        #TODO support for more graph types
        

    def startSim(self) -> None:
        """Method that uses entered parameters to start the simulation."""
        #!IMPORTANT! all opt_dicts must pass through a .verify method! They will not be verified otherwise and can pass illegal parameters!
        bad_sim_params = OptArg.verifyDictParams(self.parameters,OptArg.sim_parameters)
        bad_buyer_params = OptArg.verifyDictParams(self.buyer_args,OptArg.buyer_parameters)
        bad_seller_params = OptArg.verifyDictParams(self.seller_args,OptArg.seller_parameters)
        bad_list = [bad_sim_params,bad_buyer_params,bad_seller_params]
        if bad_list != [None] * len(bad_list):
            print("Bad params passed to simulation, default values will be used where possible!\n{}".format(bad_list))
        self.setupSim()
        self.run()

    def agentChoices(self) -> None:
        """
        Loop through all agents in the simulation and have them make choices one at a time. Sellers make choices before buyers. No agent ever has 
        access to the choice another has made in the same cycle, they happen 'simultaniously' for the sake of the simulatoin. This prevents the order 
        in which agents make choices influencing results. Returns whether this was performed successfully.
        """

        if self.parameters["SEQ_DECISIONS"]: #if true
            random.shuffle(Agent.sellers_arr)#prevents order of agent creation impacting simulation results. Makes simulation non-deterministic!
        for seller in Agent.sellers_arr:
            assert(isinstance(seller,Seller))
            seller.profits.append(0)
            action = seller.findBestAction(self.parameters["SEQ_DECISIONS"])
            seller.prices.append(seller.product_price)
        for buyer in Agent.buyers_arr:
            assert(isinstance(buyer,Buyer))
            action = buyer.findBestAction()
        action.apply()

    def endSim(self) -> None:
        print("The End.") #TODO Data output
        general_buyer_stats : dict = Buyer.getClassStats()
        general_seller_stats : dict = Seller.getClassStats()
        unique_seller_stats : list[dict] = Seller.getIndividualStats() #chuck em all in a list
        seller_averages_stats = Seller.getAveragedStats() #TODO implement (mean,mode,median,percentile of sellers)
        #TODO somehow compare how each seller performed compared to neighbours
        self.stats = self.getStats()

    def getStats(self) -> dict:
        out = {}
        #TODO complete
        return out
    
    def reachedEquilibrium(self) -> bool:
        return False #TODO implement equilibrium checker

    def run(self) -> None:
        while(True):
            #Agent decisions
            self.agentChoices()
            self.turn_num += 1
            if self.turn_num >= self.max_turn or self.reachedEquilibrium():
                break
        self.endSim() 
                

    

