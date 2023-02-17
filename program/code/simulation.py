#from program.code.arg_checker import OptArgDict 
from program.code.opt_args import OptArg
from program.code.graphs import *
from program.code.agents import *

class Simulation:
    """
    Class that manages the simulation setup and end. 
    """

    # valid_parameters = {
    #     "num_sellers" : [0,"..",100],
    #     "graph_type" : ["Line"],
    #     "buyer_dist" : ["Vanilla"],
    #     "max_iterations" : [1,"..",100]
    # }

    #'..' is inspired by haskell. Logically serves the same function but simpler.

    def __init__(self, parameters, buyer_args = {}, seller_args = {}) -> None:
        self.parameters = parameters
        self.buyer_args = buyer_args
        self.seller_args = seller_args

        #DEFAULT VALUES, overwritten if value is passed through "parameters" dictionary
        self.max_turn = 50 
        self.num_sellers = 20 
        self.buyer_dist = "Vanilla"
        self.graph_type = "Line"

        self.turn_num = 0
        self.startSim()

    def setupSim(self) -> None:
        """
        Completes simulation setup including parameter verification and Graph creation. 
        Buyer and Seller args are checked later as they are totally optional and thus less important.
        """
        if "max_iterations" in self.parameters:
            self.max_turn = self.parameters["max_iterations"]
    
        args = {
            "buyer_args" : self.buyer_args,
            "seller_args" : self.seller_args
        }
        if "num_sellers" in self.parameters:
            args["num_sellers"] = self.parameters["num_sellers"]
           
        if "graph_type" in self.parameters:
            if self.parameters["graph_type"] == "Line":
                graph = Line(**args)
        #TODO support for more graph types
        

    def startSim(self) -> None:
        """Method that uses entered parameters to start the simulation."""
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
            action = seller.findBestAction(self.parameters["SEQ_DECISIONS"])
        for buyer in Agent.buyers_arr:
            action = buyer.findBestAction()
        action.apply()

    def endSim(self) -> None:
        print("The End.") #TODO Data output
    
    def reachedEquilibrium(self) -> bool:
        return False #TODO implement equilibrium checker

    def run(self) -> None:
        while(True):
            #Agent decisions
            self.agentChoices()
            self.turn_num += 1
            if self.turn_num >= self.max_turn or self.reachedEquilibrium():
                break
        self.endSim() #TODO implement!
                

    

