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

    #optional processed data keys. E.g. optional graph output.
    opt_seller_graphs = ["prices_over_time","profits_over_time","price_profit_graph","relative_performance_rating"]
    opt_proc_buyer_keys = []

    def __init__(self, args: dict, dir = None) -> None:
        #TODO type limit for directory
        self.args = args
        self.dir = dir
        if self.dir != None:
            self.loadDataFile()

        self.seller_class_data = Seller.getClassStats()
        self.seller_data = Seller.getIndividualStats(get_complex=False)
        self.buyer_class_data = Buyer.getClassStats()
        self.buyer_data = Buyer.getCollectionStats()

        self.seller_ratings = self.calc_seller_performance()

        #TODO sim data? is it needed? prob not. 

    
    def processSeller(self, pos : int = None, excluded_keys = []) -> dict:
        """
        Process data of a single Seller with a given position in the Agent.seller_array in a standardised way. 
        Passing no value will process a random seller. 
        """
        target : Seller = self.seller_data[pos]
        if pos == None:
            pos = random.randint(0,len(self.seller_data)-1)

        out : dict = self.seller_data[pos]
        if "price_profit_graph" not in excluded_keys:
            out["prices_profit_graph"] = BuyerCollection.makeComboPlotFromList(target.buyer_collections).getFigure()
        if "prices_over_time" not in excluded_keys:
            out["prices_over_time"] = NamedDataPlot(x_vals=("time",0), y_vals=("price",target.prices)).getFigure()
        if "profits_over_time" not in excluded_keys:
            out["profits_over_time"] = NamedDataPlot(x_vals=("time",0), y_vals=("profit",target.profits)).getFigure()
        if "relative_performance_rating" not in excluded_keys:
            pass #TODO implement

        return out


    def processBuyer(self, ) -> dict:
        """
        Process data of a single Buyer Collection with a given position in the Agent.seller_array in a standardised way. 
        Passing no value will process a random seller. 
        """
        pass

    def loadDataFile(self) -> object:
        #TODO try to unpickle from location given
        try:
            return True #return unpickled obj here
        except:
            return None
        

    def makeGeneralOutput(self) -> None:
        pass


    def makeSpecificOutput(self) -> None:
        pass
