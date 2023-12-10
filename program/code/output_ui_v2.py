from typing import Union
from tkinter import *
from tkinter.ttk import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from program.code.data_handle import *
from program.code.graphs import Graph

SingleOutput = float | int | str | bool
sections = ["Buyer", "Seller", "Simulation"] #possible sections of data

class App:

    displays = {}

    #dict of all statistical data provided by pandas.describe method and their meaning for UI display
    #remove keys that don't need to be displayed.
    description_keys = {
        "count" : "Size of data set",
        "mean" : "Mean",
        "std" : "Standard deviation",
        "min" : "Minimum value",
        "25%" : "25th percentile",
        "50%" : "Median value",
        "75%" : "75th percentile",
        "max" : "Maximum value"
    }

    heading_font = ('Arial', 18)
    sub_heading_font = ('Arial', 12)


    def __init__(self, graph: Graph, in_parameters : dict, out_parameters : dict = {}) -> None:
        self.root = Tk()
        self.root.winfo_toplevel().title("Data Visualiser")
        self.graph = graph
        self.in_parameters = in_parameters
        self.out_parameters = out_parameters

        self.data_handler = DataHandler(out_parameters)

        #------FRAMES------
        top_frame = Frame(self.root)
        top_frame.pack(side=TOP)

        button_frame = Frame(self.root)
        button_frame.pack()

        self.buyer_frame = Frame(self.root)
        self.buyer_frame.pack(side=BOTTOM)

        self.seller_frame = Frame(self.root)
        self.seller_frame.pack(side=BOTTOM)

        #------LABELS------
        title_label = Label(top_frame, text= "General Data Output", font=App.heading_font)
        title_label.pack(side=TOP)

        seller_label = Label(self.seller_frame, text= "General Seller performance", font= App.sub_heading_font)
        seller_label.pack(side=TOP)

        buyer_label = Label(self.buyer_frame, text= "General Buyer performance", font= App.sub_heading_font)
        buyer_label.pack(side=TOP)

        #------BUTTONS------
        show_graph = Button(button_frame, text="Graph")
        show_graph.configure(command=self.show_graph)
        show_graph.pack(side=LEFT, padx=5, pady=5)

        show_params = Button(button_frame, text="Simulation parameters")
        show_params.configure(command=self.show_parameters)
        show_params.pack(side=LEFT, padx=5, pady=5)

        self.getSellerPerf()

        self.getBuyerPerf()

        self.root.mainloop()
    
    def show_graph(self) -> None:
        self.graph.display(self.graph.graph_obj)

    def show_parameters(self) -> None:
        popup = Toplevel()
        popup.title("Simulation parameters")

        for section_name, dict in self.in_parameters.items():
            sec_frame = Frame(popup)
            sec_frame.pack(side=TOP,pady=5)
            sec_title_label = Label(sec_frame, text=section_name, font= App.sub_heading_font)
            sec_title_label.pack(side=TOP)
            for param_name, value in dict.items():
                temp = ParamDisplay(sec_frame, param_name, value)

    #TODO carry on here
    def getSellerPerf(self) -> dict:
        pass
        #self.data_handler.

class ParamDisplay:

    def __init__(self, container: Tk, param_name : str, value : any):
        self.container = container
        self.param_name = param_name
        self.value = value
        
        combined_text = "{}: {}".format(param_name, value)

        val_label = Label(container, text= combined_text)
        val_label.pack()


class LookupContainer:

    def __init__(self, container : Tk, title : str, data : dict):

        self.displayed_figures = {}
        self.displayed_vals = {}

        self.container = container
        self.title = title
        self.data = data

        self.frame = Frame(self.container)
        self.frame.pack(side=BOTTOM, pady=5)

        self.title_label = Label(self.frame, text=self.title, font=App.sub_heading_font)
        self.title_label.pack(side=TOP,padx=5)

        self.remove_button = Button(self.frame, text="remove")
        self.remove_button.configure(command= lambda a="": self.frame.destroy())
        self.remove_button.pack(side=TOP)

        self.show_conts()

    def show_conts(self):
        for title, contents in self.data.items():
            if isinstance(contents, Figure):
                self.displayed_figures[title] = FigureDisplay(title, figure=contents, container=self.container)
            elif isinstance(contents, SingleOutput):
                self.displayed_vals[title] = ValueDisplay(title, value=contents, container=self.container)
            else:
                print("Error, incompatible display data for {}. {} is not yet supported!".format(title,type(contents)))


class FigureDisplay:

    def __init__(self, title : str, figure : Figure, container : Frame):
        self.frame = Frame(container)
        self.frame.pack(side=BOTTOM)

        self.title_label = Label(self.frame, text=title, font=App.sub_heading_font)
        self.title_label.pack(side=TOP)

        canvas = FigureCanvasTkAgg(figure, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)



class ValueDisplay:

    def __init__(self, title : str, value : SingleOutput, container : Frame):
        self.frame = Frame(container)
        self.frame.pack(side=BOTTOM)

        self.title_label = Label(self.frame, text=title, font=App.sub_heading_font)
        self.title_label.pack(side=TOP)