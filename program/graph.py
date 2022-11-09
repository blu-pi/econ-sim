import networkx as nx
from enum import Enum
from random import Random
from agent import Agent 


#interface
class Graph:
    pass

class Line(Graph):

    def __init__(self, num_sellers, buyer_args = {}, seller_args = {}):
        self.num_sellers = num_sellers

    def makeGraph(num_sellers):
        G = nx.Graph()
        for i in range(num_sellers):
            pass

class Tree(Graph):

    def __init__(self, num_sellers, arg_dict, buyer_args = {}, seller_args = {}):
        self.num_sellers = num_sellers
        self.arg_dict = arg_dict
        super().__init__(num_sellers)