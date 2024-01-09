import networkx as nx
import matplotlib.pyplot as plt

import math
from random import Random

from env.agents import Seller, Buyer, Agent
from env.collection import BuyerCollection

#interface, not to be confuced with nx.Graph!
#Kinda ugly code but I'm not about to spend hours rewriting this just to make it marginally more efficient. #TODO eventually rewrite
class Graph:
    """
    General Interface to define what are/ aren't Graphs in general. Mostly used for type comparisons.
    Stores all actively used graphs in a current simulation in 'total_graphs' class attribute. (There may be more than 1 graph in some cases)
    """
    
    total_graphs = []
    
    @staticmethod
    def joinSellers(buys_from : list[Seller], graph : nx.Graph, buyer_args : dict = {},  num_buyers : int = 1) -> None:
        buyers = []
        for i in range(num_buyers):
            buyer = Buyer(buys_from, buyer_args)
            buyers.append(buyer)
            graph.add_edge(str(buys_from[0]), str(buys_from[1]), obj = buyer) #add edge between previous and seller. Give buyer object as reference.
        Agent.buyer_collections_arr.append(BuyerCollection(buyers))

    def display(self, graph_obj) -> None:
        layout = self.get_layout()
        nx.draw(graph_obj, pos= layout, with_labels=True)
        plt.show()
    
    def get_layout(self):
        return nx.spring_layout(self.graph_obj)

class Line(Graph):
    """
    Class to define and create a line graph with given properties. Uses networkx library to represent the graph.
    Can also be used to make a circle.
    Inherits from Graph.
    """

    def __init__(self, num_sellers = 20, graph_args = {}, buyer_args = {}, seller_args = {}, isCircle : bool = False) -> None:
        self.num_sellers = num_sellers
        self.buyer_args = buyer_args
        self.seller_args = seller_args
        self.graph_args = graph_args #clone of sim args so many params won't be used.
        self.isCircle = isCircle
        self.graph_obj = self.makeGraph()

    def makeGraph(self) -> nx.Graph:
        G = nx.Graph()
        Graph.total_graphs.append(G)
        first = Seller(self.seller_args)
        G.add_node(str(first), obj = first)
        previous = first
        num_buyers = 1 #default
        if "buyers_per_seller_pair" in self.graph_args:
            num_buyers = self.graph_args["buyers_per_seller_pair"]
        for i in range(self.num_sellers - 1):
            seller = Seller(self.seller_args)
            G.add_node(str(seller), obj = seller)
            Graph.joinSellers([previous, seller], G, self.buyer_args, num_buyers)
            previous = seller
        if self.isCircle:
            Graph.joinSellers([previous, first], G, self.buyer_args, num_buyers)
        
        return G
    
    def get_layout(self):
        return nx.spectral_layout(self.graph_obj)
    

class Tree(Graph):
    """
    Class to define and create a tree graph with given properties. Uses networkx library to represent the graph.
    Graph properties can be specified through optional argument 'graph_args'. 
    Inherits from Graph.
    """

    def __init__(self, num_sellers = 20, graph_args = {}, buyer_args = {}, seller_args = {}) -> None:
        self.layout = None
        self.num_sellers = num_sellers
        self.buyer_args = buyer_args
        self.seller_args = seller_args
        self.graph_args = graph_args
        self.graph_obj = self.makeGraph()

    def makeGraph(self) -> nx.Graph:
        num_buyers = 1 #default
        if "buyers_per_seller_pair" in self.graph_args:
            num_buyers = self.graph_args["buyers_per_seller_pair"]
        G = nx.Graph()
        root = Seller(self.seller_args)
        G.add_node(str(root), obj = root)
        prev_layer = [root]
        num_layers = math.ceil(math.log2(self.num_sellers))
        remaining_sellers = self.num_sellers - 1
        for i in range(num_layers - 1):
            current_layer = []
            #print(i,2**(i+1),remaining_sellers)
            for x in range(min(2**(i+1),remaining_sellers)):
                seller = Seller(self.seller_args)
                G.add_node(str(seller), obj = seller)
                current_layer.append(seller)
            current = current_layer.copy()
            for prev_seller in prev_layer:
                if len(current) > 0:
                    Graph.joinSellers([prev_seller, current[0]], G, self.buyer_args, num_buyers)
                if len(current) > 1:
                    Graph.joinSellers([prev_seller, current[1]], G, self.buyer_args, num_buyers)
                del current[:2]
            prev_layer = current_layer
            remaining_sellers -= len(current_layer)

        return G