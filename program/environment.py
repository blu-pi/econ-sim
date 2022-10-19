from enum import Enum
from random import Random
from agent import Agent 

class Graph:

    class Type(Enum):
        Line = "Line graph",
        Tree = "Tree graph",
        Mesh = "Mesh graph",
        Rand = "Random graph"

    def __init__(self, graph_type = Type.Line, num_sellers = 10, layers = 1):
        self.graph_type = graph_type
        self.num_sellers = num_sellers
        self.layers = layers #only relevant for tree and mesh. Line is always 1.

    def makeGraph(self):
        for i in range(self.num_sellers):
            seller = Agent() #default args used for making sellers
        if self.graph_type == self.Type.Rand:
            x = Random.randint(0, len(Graph.Type) -1)
        self.graph_type = self.Type[x]
        match self.graph_type:
            case self.Type.Tree:
                self.makeTreeGraph()
            case self.Type.Mesh:
                self.makeMeshGraph()
            case _:
                self.makeLineGraph()
    
    def makeTreeGraph(self):
        pass

    def makeMeshGraph(self):
        pass

    def makeLineGraph(self):
        pass