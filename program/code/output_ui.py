from typing import Union

from program.code.data_plot import NamedDataPlot
from program.code.opt_args import OptArg

from tkinter import *
from tkinter.ttk import *

import pickle

class App:

    def __init__(self, parent : Tk, data_dict : dict = {}, filepath : str = None, params : dict = {}) -> None:
        parent.winfo_toplevel().title("Simulation Findings")
        self.parent = parent
        self.params = params
        self.section_objs = []

        #defaults
        #There are none right now

        for key in params:
            setattr(self, key, self.params[key])

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
            print(data_dict)
            for key,data in data_dict.items():
                if isinstance(data,dict):
                    setattr(self, key, data_dict[key]) #self.*key_name* = *dict_name*[*key_name*]
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

    def __init__(self, parent, title : str, data : dict, arg_dict : dict = {}) -> None:
        self.frame = Frame(parent)
        self.frame.pack(side=TOP)
        self.displays = []
        title_label = Label(self.frame,text=title,font=('Arial', 18))
        title_label.pack(side=TOP)
        for key,vals in data.items():
            if isinstance(vals,list):          
                self.displays.append(graph_display(self.frame))

class graph_display:

    def __init__(self, parent) -> None:
        self.parent = parent
        self.frame = Frame(parent)
        self.frame.pack(side=TOP)

        
class Controller: 

    @staticmethod
    def startUI(data_dict : dict = {}, filepath : str = None, params : dict = {}) -> None:
        root = Tk()
        app = App(root, data_dict, filepath, params)
        root.mainloop()