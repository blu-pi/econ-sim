import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *

from program.code.data_handle import *
from program.code.graphs import Graph


class GraphUI:

    def __init__(self, graph : Graph, output_dest : Tk, data_handler : DataHandler):
        self.graph = graph
        self.fig, self.ax = plt.subplots()
        self.output_dest = output_dest
        self.data_handler = data_handler

    def on_click(self, event):

        if event.button == 1 and event.inaxes is not None:
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
        from program.code.output_ui_v2 import LookupContainer
        #incoming war crime, I'm not sorry (it never happened) but if it did (it did) they deserved it (they did not)
        #Explanation below 
        #GraphUI.Line/Tree.networkx_Graph.nodes[node][seller_obj_arg_reference] -> Chosen Seller object reference
        seller_obj : Seller = self.graph.graph_obj.nodes[node]["obj"]
        data = {
            "Absolute performance" : self.data_handler.absoluteSellerPerformance(seller_obj),
            "Relative performance" : self.data_handler.relativeSellerPerformance(seller_obj),
            "Price to profit graph" : self.data_handler.priceProfit(seller_obj)
        }
        title = "{} data".format(seller_obj)
        cont = LookupContainer(self.output_dest, title, data)
        
        
