from typing import Tuple, Union

from program.code.data_plot import NamedDataPlot
from program.code.opt_args import OptArg

import pandas as pd
from tkinter import *
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import pickle

SingleOutput = float | int | str | bool

class App:

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

    prefer_asLabels = True #Just to inform that this value exists in runtime. Value not determined here though.

    heading_font = ('Arial', 18)
    sub_heading_font = ('Arial', 12)


    def __init__(self, parent : Tk, data_dict : dict = {}, filepath : str = None, params : dict = {}) -> None:
        parent.winfo_toplevel().title("Simulation Findings")
        self.parent = parent
        self.params = params
        self.section_objs = []

        #defaults
        self.prefer_desc_as_labls = True 

        #overrides defaults
        for key in params:
            setattr(self, key, self.params[key])

        App.prefer_asLabels = self.prefer_desc_as_labls

        if filepath != None:
            try:
                sim_file = open(filepath+"/sim_data.pkl", "r")
                seller_file = open(filepath+"/seller_data.pkl", "r")
                buyer_file = open(filepath+"/buyer_data.pkl", "r")
            except FileNotFoundError:
                print("Chosen file not found, can't output data.")
                print("Path given = {}".format(filepath))
                exit(0)
            finally:
                self.sim_data = pickle.load(sim_file)
                self.seller_data = pickle.load(seller_file)
                self.buyer_data = pickle.load(buyer_file)
                sim_file.close()
                seller_file.close()
                buyer_file.close()
        elif len(data_dict) > 0:
            #instantiate to avoid referenced before assignment
            self.sim_data = {}
            self.seller_data = {}
            self.buyer_data = {}
            for key,data in data_dict.items():
                if isinstance(data,dict|list):
                    setattr(self, key, data_dict[key]) #self.*key_name* = *dict_name*[*key_name*]
                    #the list is assumed to be a list of dicts since this will always be hardcoded.
                else:
                    print("DEGUG, passed data was ignored as it's not a section dictionary")
                    print(data)
        else:
            print("Error, no filepath or data dictionaries passed to output generator!")
            exit(0)

        self.genOutput()

    def genOutput(self) -> None:
        sections = {
            "Simulation data" : self.sim_data,
            "Seller data" : self.seller_data,
            "Buyer data" : self.buyer_data
        }
        for section_name in sections:
            self.section_objs.append(Section(self.parent, section_name, sections[section_name]))

class Section():
    """A subheading container for output UI. Also stores data within other tk objects stored in its Frame instance"""

    def __init__(self, parent, title : str, data : dict|list, arg_dict : dict = {}) -> None:
        self.frame = Frame(parent)
        self.frame.pack(side=TOP)
        self.displays = []
        title_label = Label(self.frame,text=title,font=App.heading_font)
        title_label.pack(side=TOP)
        if isinstance(data,list):
            if all(isinstance(d, dict) for d in data):
                self.data = data[0] | data[1]
            else:
                #cba to handle this. It could be handled but it just shouldn't need to be
                print("Error, data list passed to section didn't only contain dictionaries.")
                print("This section now has no valid data")
        elif isinstance(data, dict):
            self.data = data.copy()
        else:
            print("Error, bad data input for section data. Yeah... it's real bad")
            exit(0)

        for key,val in self.data.items():
            if isinstance(val,NamedDataPlot):          
                self.displays.append(graph_display(self.frame, key, val, withDescription="y"))
            elif isinstance(val,SingleOutput):          
                self.displays.append(single_stat_display(self.frame, key, val))
            elif isinstance(val,dict):    
                print("dict ignored")  
                #self.displays.append(labeled_multi_stat_display(self.frame, key, val))
            elif isinstance(val,list):
                temp = pd.Series(val)
                desc = temp.describe()
                self.displays.append(description_display(self.frame, key, desc, asLabels=App.prefer_asLabels))
            else:
                print("Error, unsupported Unknown outout data")
                print("{} section generation will be skipped".format(key))
                print(type(val))


#---------------------    UI-DISPLAYS    ---------------------

class graph_display:

    def __init__(self, parent : Tk, data_name : str, plot : NamedDataPlot, withDescription : str = None) -> None:
        self.parent = parent
        self.plot = plot
        self.plot.trim()
        self.data_name = data_name
        self.withDescription = withDescription
        self.description_display = None
        self.fig = self.plot.getFigure()
        self.frame = Frame(parent)
        self.frame.pack(side=TOP)

        self.title_label = Label(self.frame, text = data_name, font = App.sub_heading_font)
        self.title_label.pack()

        canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        new_data = []
        new_title = []
        if self.withDescription != None:
            if "x" in withDescription:
                new_data.append(self.plot.describe_x())
                new_title.append("_x")
            if "y" in withDescription:
                new_data.append(self.plot.describe_y())
                new_title.append("_y")
            for val,title in zip(new_data,new_title):
                new_data_name = data_name + "_described" + title
                self.description_display = description_display(parent,new_data_name,val,asLabels=App.prefer_asLabels)

class description_display:

    def __init__(self, parent : Tk, data_name : str, data : dict, asLabels : bool = True) -> None:
        self.parent = parent
        self.data = data
        self.data_name = data_name
        self.frame = Frame(parent)
        self.frame.pack(side=TOP)

        self.title_label = Label(self.frame, text = data_name, font = App.sub_heading_font)
        self.title_label.pack()

        self.data_labels = []
        if asLabels:
            for key,val in data.items():
                if isinstance(val, float):
                    val = round(val,4)
                sub_data_name = key
                if key in App.description_keys:
                    sub_data_name = App.description_keys[key]
                key_label = Label(self.frame,text=sub_data_name+": "+str(val))
                key_label.pack(side=LEFT)
                #data_label = Label(self.frame,text=val)
                #data_label.pack(side=LEFT)
                #self.data_labels.append(data_label)
        else:
            print("Error distribution display not done.")
            print(data_name + " was skipped.")

class single_stat_display:

    def __init__(self, parent : Tk, data_name : str, data : SingleOutput) -> None:
        self.parent = parent
        self.data = data
        self.data_name = data_name
        self.frame = Frame(parent)
        self.frame.pack(side=TOP)

        self.title_label = Label(self.frame, text = data_name, font = App.sub_heading_font)
        self.title_label.pack(side=TOP)

        self.data_label = Label(self.frame,text=data)
        self.data_label.pack(side=TOP)

class labeled_multi_stat_display:

    def __init__(self, parent : Tk) -> None:
        pass
        
class Controller: 

    @staticmethod
    def startUI(data_dict : dict = {}, filepath : str = None, params : dict = {}) -> None:
        root = Tk()
        app = App(root, data_dict, filepath, params)
        root.mainloop()