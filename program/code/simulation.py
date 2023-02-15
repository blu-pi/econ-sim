from program.code.arg_checker import OptArgDict 
from program.code.graphs import *
from program.code.agents import *

class Simulation:
    """
    Class that manages the simulation setup and end. 
    """

    valid_parameters = {
        "num_sellers" : [0,"..",100],
        "graph_type" : ["Line"],
        "buyer_dist" : ["Vanilla"],
        "max_iterations" : [1,"..",100]
    }
    #'..' is inspired by haskell. Logically serves the same function but simpler.

    def __init__(self, parameters, buyer_args = {}, seller_args = {}) -> None:
        self.parameters = parameters
        self.buyer_args = buyer_args
        self.seller_args = seller_args
        self.max_turn = 50 #default, only used if none passed
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
        bad_params = OptArgDict.verifyDictParams(self.parameters,Simulation.valid_parameters)
        if bad_params != None:
            print("Bad params passed to simulation, default values will be used where possible!\n{}".format(bad_params))
        self.setupSim()
        self.run()

    def endSim(self) -> None:
        print("The End.") #TODO Data output
    
    def reachedEquilibrium(self) -> bool:
        return False #TODO implement equilibrium checker

    def run(self) -> None:
        while(True):
            #Agent decisions
            Agent.agentChoices()
            self.turn_num += 1
            if self.turn_num >= self.max_turn or self.reachedEquilibrium():
                break
        self.endSim() #TODO implement!
                

    

