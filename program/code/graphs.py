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

    #Args that apply no matter which graph type is being used
    valid_g_args = []
    valid_b_args = ["percieved_util", "min_util", "max_util"]
    valid_s_args = ["PERFECT_INFORMATION"]
    
    total_graphs = []

class Line(Graph):
    """
    Class to define and create a line graph with given properties. Uses networkx library to represent the graph.
    Graph properties can be given through optional argument 'graph_args'. 
    GENERAL (NOT individual) Buyer and Seller args can be passed using optional arguments 'buyer_args' and 'seller_args' respectively.
    All optional arguments are dictionaries with valid keys stored in class attributes 'valid_g_args', 'valid_b_args', and 'valid_s_args' respectively.
    Inherits from Graph.
    """

    #Args that apply only for a line graph
    valid_g_args = []
    valid_b_args = []
    valid_s_args = []

    def __init__(self, num_sellers, graph_args = {}, buyer_args = {}, seller_args = {}) -> None:
        self.num_sellers = num_sellers
        self.buyer_args = buyer_args
        self.seller_args = seller_args
        self.graph_args = graph_args
        self.graph_obj = self.makeGraph(num_sellers, buyer_args, seller_args)

    def makeGraph(self, num_sellers, buyer_args = {}, seller_args = {}) -> nx.Graph:
        G = nx.Graph()
        Graph.total_graphs.append(G)
        previous = None
        for i in range(num_sellers):
            seller = Seller(seller_args)
            G.add_node(str(seller), obj = seller)
            if i > 0:
                buyer = Buyer([previous, seller], buyer_args)
                G.add_edge(str(previous), str(seller), obj = buyer) #add edge between previous and seller. Give buyer object as reference.
            previous = seller
        nx.draw_networkx(G) #just to test correct shape
        # Set margins for the axes so that nodes aren't clipped
        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        plt.show()
        return G

class Tree(Graph):
    """
    Class to define and create a tree graph with given properties. Uses networkx library to represent the graph.
    Graph properties can be given through optional argument 'graph_args'. 
    GENERAL (NOT individual) Buyer and Seller args can be passed using optional arguments 'buyer_args' and 'seller_args' respectively.
    All optional arguments are dictionaries with valid keys stored in class attributes 'valid_g_args', 'valid_b_args', and 'valid_s_args' respectively.
    Inherits from Graph.
    """

    #Args that only apply for a tree graph
    valid_g_args = []
    valid_b_args = []
    valid_s_args = []

    def __init__(self, num_sellers, graph_args = {}, buyer_args = {}, seller_args = {}) -> None:
        self.num_sellers = num_sellers
        self.buyer_args = buyer_args
        self.seller_args = seller_args
        self.graph_args = graph_args
    #TODO makeGraph implementation
