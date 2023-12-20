import pandas as pd
import random

from program.code.collection import *
from program.code.data_plot import *

#Potential for refactor, could move functionality to Seller/Buyer classes.
class DataHandler:
    """
    Dedicated class for processing collected data in preparation for use in UI output.
    """

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

    def priceProfit(target : Seller) -> Figure:
        plot : NamedDataPlot = BuyerCollection.makeComboPlotFromList(target.buyer_collections)
        #plot.trim()
        return plot.getFigure()
    
    def priceTime(target : Seller) -> Figure:
        plot = NamedDataPlot(x_vals=("time",0), y_vals=("price",target.prices))
        return plot.getFigure()
    
    def profitTime(target : Seller) -> Figure:
        plot = NamedDataPlot(x_vals=("time",0), y_vals=("profit",target.profits))
        return plot.getFigure()

    def relativeSellerPerformance(self, target : Seller) -> float:
        """Calculate individual seller performance compared to other Sellers"""
        profits = Seller.getProfits()
        described_profits = pd.Series(profits).describe().to_dict()
        median_profit = described_profits["50%"]
        return target.applyPerformanceMeasure() / median_profit
    
    #TODO test this!
    def absoluteSellerPerformance(self, target : Seller = None) -> float:
        """Calculate Seller performance compared to the theoretical optimum. If no Seller is passed the population as a whole is examined"""
        profits = Seller.getProfits()
        described_profits = pd.Series(profits).describe().to_dict()
        data_plot = Seller.buyer_collections_arr[0].makePlot(show_output=True)
        print(data_plot.y_vals)
        optimum = Seller.sellers_arr[0].applyPerformanceMeasure(data_plot.y_vals)
        if target is None:
            optimum *= len(Agent.buyer_collections_arr)
            return sum(profits) / optimum
        else:
            num_competitors = len(target.buyer_collections)
            profit_per_collection = target.applyPerformanceMeasure() / num_competitors
            return profit_per_collection / optimum
    
    def calculateBuyerPerformace(self, target : Buyer = None) -> float:
        pass

    def loadDataFile(self) -> object:
        #TODO try to unpickle from location given
        try:
            return True #return unpickled obj here
        except:
            return None
        