import networkx as nx
import matplotlib.pyplot as plt
from random import Random
from agent import Agent, Buyer, Seller


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
        nx.draw(G)
        return G

class Tree(Graph):

    def __init__(self, num_sellers, graph_args = {}, buyer_args = {}, seller_args = {}) -> None:
        self.num_sellers = num_sellers
        self.buyer_args = buyer_args
        self.seller_args = seller_args
        self.graph_args = graph_args
        #TODO makeGraph implementation

if __name__ == "__main__":
    G = nx.petersen_graph()
    subax1 = plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
    subax2 = plt.subplot(122)
    nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')