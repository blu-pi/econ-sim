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

    def priceProfit(self, target : Seller) -> Figure:
        plot : NamedDataPlot = BuyerCollection.makeComboPlotFromList(target.buyer_collections)
        #plot.trim()
        return plot.getFigure()
    
    def priceTime(self, target : Seller) -> Figure:
        plot = NamedDataPlot(x_vals=("time",0), y_vals=("price",target.prices))
        return plot.getFigure()
    
    def profitTime(self, target : Seller) -> Figure:
        plot = NamedDataPlot(x_vals=("time",0), y_vals=("profit",target.profits))
        return plot.getFigure()

    def relativeSellerPerformance(self, target : Seller) -> float:
        """Calculate individual seller performance compared to other Sellers"""
        profits = Seller.getProfits()
        described_profits = pd.Series(profits).describe().to_dict()
        median_profit = described_profits["50%"]
        return target.applyPerformanceMeasure() / median_profit
    
    #TODO test this!
    def absoluteSellerPerformance(self, target : Seller) -> float:
        """Calculate Seller performance compared to the theoretical optimum"""
        data_plot = BuyerCollection.makeComboPlotFromList(target.buyer_collections)
        optimum = target.applyPerformanceMeasure(data_plot.y_vals)
        return target.applyPerformanceMeasure() / optimum
    
    def sellerClassPerformance(self) -> float:
        """Calculate absolute performance value for the entire population of sellers asa whole"""
        individual_performance = []
        for seller in Seller.sellers_arr:
            individual_performance.append(self.absoluteSellerPerformance(seller))
        return sum(individual_performance) / len(individual_performance)
    
    def calculateBuyerPerformace(self, target : Buyer = None) -> float:
        """Not implemented yet; might be pointless"""
        pass

    def loadDataFile(self) -> object:
        #TODO try to unpickle from location given
        try:
            return True #return unpickled obj here
        except:
            return None
        