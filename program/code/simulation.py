from typing import Tuple
import pandas as pd

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

    def endSim(self) -> None:
        print("The End.") #TODO Data output
        #-------- STAT PROCESSING --------
        general_buyer_stats : dict = Buyer.getClassStats()
        general_seller_stats : dict = Seller.getClassStats()
        merged_seller_stats : dict = self.unifyDicts(Seller.getIndividualStats())
        merged_analysis, averaged_merged_seller_stats = Simulation.describeDataDict(merged_seller_stats)
        self.stats : dict = self.getClassStats()
        #TODO test and then pass to output UI
        #TODO finish output UI to automatically create output depending on passed data

    @staticmethod
    def getAveragedStats(target : dict) -> dict:
        out = {}
        for key,data in target.items():
            if all(isinstance(n, float) for n in data):
                data = pd.Series(data)
                avg_data = data.describe().to_dict() #more familiar with dict rather than series.
            new_key = key + "_averages"
            out.update({new_key : avg_data}) #dict in a dict... 
        return out
    
    def unifyDicts(self, dictionaries : list[dict]) -> dict:
        """
        Merge passed dictionaries into 1 only using intersect of keys.
        """
        out = {}
        key_sets = [set(d.keys()) for d in dictionaries]
        common_keys = set.intersection(*key_sets)
        for key in common_keys:
            values = [d[key] for d in dictionaries]
            new_key = "merged_" + key
            out[new_key] = values
        return out

    def describeDataDict(target : dict) -> Tuple[dict,dict]:
        """
        Get pandas.describe data from a dictionary. Made specifically for a unified dict.
        Also outputs modified input dictionary. This is only different from input dict
        if it contains a nested list which is changed to an element-wise mean of the lists.
        This needs to be returned to give the new values that were described.
        Usually used as data for a pyplot in output.
        """
        temp = target
        analysis_dict = {}
        for key,data in target.items():
            if all(isinstance(n, list) for n in data):
                temp.update({key:[np.mean(k) for k in zip(*data)]}) #element wise mean of lists
                data = temp[key]
            if all(isinstance(n, float) for n in data): #other data doesn't need to be analysed
                new_key = "described_" + key
                data_series = pd.Series(data)
                analysis_dict.update({new_key : data_series.describe().to_dict()})
        return analysis_dict, temp

    def getClassStats(self) -> dict:
        out = {}
        #TODO complete
        return out
                

    

