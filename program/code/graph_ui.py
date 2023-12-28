import networkx as nx
import matplotlib.pyplot as plt

from program.code.data_handle import *
from program.code.graphs import Graph


class GraphUI:

    def __init__(self, graph : Graph):
        self.graph = graph
        self.fig, self.ax = plt.subplots()

    def on_click(self, event):
        print(event) #TODO only for debug

        if event.button == 1 and event.inaxes is not None:
            print("click")
            x, y = event.xdata, event.ydata
            pos = self.graph.get_layout()
            
            tolerance = 0.1  # Adjust this value for your specific case to determine the proximity to a node

            # Check if the click is near a node
            for node, coord in pos.items():
                distance = ((coord[0] - x) ** 2 + (coord[1] - y) ** 2) ** 0.5
                if distance < tolerance:
                    self.clicked_node = node
                    break 
            
            self.display_data(self.clicked_node)

    def connect_events(self):
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def display_interactive_graph(self):
        pos = self.graph.get_layout()
        nx.draw(self.graph.graph_obj, pos, with_labels=True)

        self.connect_events()
        plt.show()
    
    def display_data(self, node) -> None:
        #incoming war crime, I'm not sorry (it never happened) but if it did (it did) they deserved it (they did not)
        #Explanation below 
        #GraphUI.Line/Tree.networkx_Graph.nodes[node][seller_obj_arg_reference] -> Chosen Seller object reference
        seller_obj : Seller = self.graph.graph_obj.nodes[node]["obj"]
        
