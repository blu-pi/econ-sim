import networkx as nx
import matplotlib.pyplot as plt
from random import Random
from program.code.agent import *


#interface, not to be confuced with nx.Graph!
class Graph:
    
    total_graphs = []

class Line(Graph):

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

    def __init__(self, num_sellers, graph_args = {}, buyer_args = {}, seller_args = {}) -> None:
        self.num_sellers = num_sellers
        self.buyer_args = buyer_args
        self.seller_args = seller_args
        self.graph_args = graph_args
    #TODO makeGraph implementation
