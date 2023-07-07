import pandas as pd
import random

from program.code.collection import *
from program.code.data_plot import *

class DataHandler:
    """
    Dedicated class for processing collected data in preparation for use in UI output.
    """
    processed_sellers = {}
    processed_buyers = {}
    #seller_performances = {} Could be used for optimisation

    #optional processed data keys. E.g. optional graph output.
    opt_seller_graphs = ["prices_over_time","profits_over_time","price_profit_graph","relative_performance_rating"]
    opt_proc_buyer_keys = []

    def __init__(self, parameters: dict, dir = None) -> None:
        #TODO type limit for directory
        self.parameters = parameters
        self.dir = dir
        if self.dir != None:
            self.loadDataFile()

        self.seller_class_data = Seller.getClassStats()
        self.seller_data = Seller.getIndividualStats(get_complex=False)
        self.buyer_class_data = Buyer.getClassStats()
        #self.buyer_data = Buyer.getCollectionStats()

        #TODO sim data? is it needed? prob not. 

    def process(self, section_name : str, pos : int = None) -> dict:
        if section_name == "Buyer":
            return self._processBuyer()
        if section_name == "Seller":
            if pos != None:
                return self._processSeller()
            return self._processSellerClass() #TODO
        print("Data output error! Can't find data for " + section_name)
        return {}
    
    def _processSeller(self, pos : int = None, excluded_keys = []) -> dict:
        """
        Process data of a single Seller with a given position in the Agent.seller_array in a standardised way. 
        Passing no value will process a random seller. 
        """
        target : Seller = self.seller_data[pos]
        if pos == None:
            pos = random.randint(0,len(self.seller_data)-1)

        out : dict = self.seller_data[pos]
        if "price_profit_graph" not in excluded_keys:
            plot : NamedDataPlot = BuyerCollection.makeComboPlotFromList(target.buyer_collections)
            out["prices_profit_graph"] = plot.getFigure()

        if "prices_over_time" not in excluded_keys:
            plot = NamedDataPlot(x_vals=("time",0), y_vals=("price",target.prices))
            out["prices_over_time"] = plot.getFigure()

        if "profits_over_time" not in excluded_keys:
            plot = NamedDataPlot(x_vals=("time",0), y_vals=("profit",target.profits))
            out["profits_over_time"] = plot.getFigure()

        if "relative_performance_rating" not in excluded_keys:
            out["relative_performance_rating"] = self.calculateSellerPerformance()
            
        return out
    
    def _processSellerClass(self) -> dict:
        pass

    def _processBuyer(self) -> dict:
        """
        Process data of a single Buyer Collection with a given position in the Agent.seller_array in a standardised way. 
        Passing no value will process a random seller. 
        """
        out = {

        }
        return out

    def calculateSellerPerformance(self, pos : int) -> int:
        profits = Seller.getProfits()
        described_profits = pd.Series(profits).describe().to_dict()
        median_profit = described_profits["50%"]
        return profits[pos] / median_profit

    def loadDataFile(self) -> object:
        #TODO try to unpickle from location given
        try:
            return True #return unpickled obj here
        except:
            return None
        