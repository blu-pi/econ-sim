import networkx as nx
import matplotlib.pyplot as plt
from random import Random

from program.code.agents import Seller, Buyer

#interface, not to be confuced with nx.Graph!
class Graph:
    """
    General Interface to define what are/ aren't Graphs in general. Mostly used for type comparisons.
    Stores all actively used graphs in a current simulation in 'total_graphs' class attribute. (There may be more than 1 graph in some cases)
    """
    
    total_graphs = []
    
    @staticmethod
    def joinSellers(buys_from : list[Seller], graph : nx.Graph, buyer_dist : str = "Vanilla", buyer_args : dict = {},  num_buyers : int = 1) -> None:
        if buyer_dist == "Vanilla":
            for i in range(num_buyers):
                buyer = Buyer([buys_from[0], buys_from[1]], buyer_args)
                graph.add_edge(str(buys_from[0]), str(buys_from[1]), obj = buyer) #add edge between previous and seller. Give buyer object as reference.

    def display(graph_obj) -> None:
        nx.draw_networkx(graph_obj) #just to test correct shape
        # Set margins for the axes so that nodes aren't clipped
        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        plt.show()
        return graph_obj

class Line(Graph):
    """
    Class to define and create a line graph with given properties. Uses networkx library to represent the graph.
    Graph properties can be specified through optional argument 'graph_args'. 
    Inherits from Graph.
    """

    def __init__(self, num_sellers = 20, graph_args = {}, buyer_args = {}, seller_args = {}) -> None:
        self.num_sellers = num_sellers
        self.buyer_args = buyer_args
        self.seller_args = seller_args
        self.graph_args = graph_args #clone of sim args so many params won't be used.
        self.graph_obj = self.makeGraph()

    def makeGraph(self, show_result : bool = True) -> nx.Graph:
        G = nx.Graph()
        Graph.total_graphs.append(G)
        previous = None
        for i in range(self.num_sellers):
            seller = Seller(self.seller_args)
            G.add_node(str(seller), obj = seller)
            if i > 0:
                Graph.joinSellers([previous, seller], G, self.graph_args["buyer_dist"], self.buyer_args)
            previous = seller
        if show_result:
            Graph.display(G)
        return G

class Circle(Graph):
    """
    Class to define and create a tree graph with given properties. Uses networkx library to represent the graph.
    Graph properties can be specified through optional argument 'graph_args'. 
    Inherits from Graph.
    """    
    def __init__(self, num_sellers = 20, graph_args = {}, buyer_args = {}, seller_args = {}) -> None:
        self.num_sellers = num_sellers
        self.buyer_args = buyer_args
        self.seller_args = seller_args
        self.graph_args = graph_args
        self.graph_obj = self.makeGraph()
    
    def makeGraph(self, show_result : bool = True) -> nx.Graph:
        G = nx.Graph()
        Graph.total_graphs.append(G)
        first = Seller(self.seller_args)
        previous = first
        num_buyers = 1 #default
        if "buyers_per_seller_pair" in self.graph_args:
            num_buyers = self.graph_args["buyers_per_seller_pair"]
        for i in range(self.num_sellers - 1):
            seller = Seller(self.seller_args)
            G.add_node(str(seller), obj = seller)
            Graph.joinSellers([previous, seller], G, self.graph_args["buyer_dist"], self.buyer_args, num_buyers)
            previous = seller
        Graph.joinSellers([previous, first], G, self.graph_args["buyer_dist"], self.buyer_args, num_buyers)
        
        if show_result:
            Graph.display(G)
        return G


class Tree(Graph):
    """
    Class to define and create a tree graph with given properties. Uses networkx library to represent the graph.
    Graph properties can be specified through optional argument 'graph_args'. 
    Inherits from Graph.
    """

    def __init__(self, num_sellers, graph_args = {}, buyer_args = {}, seller_args = {}) -> None:
        self.num_sellers = num_sellers
        self.buyer_args = buyer_args
        self.seller_args = seller_args
        self.graph_args = graph_args
    #TODO makeGraph implementation
