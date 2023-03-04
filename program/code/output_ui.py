from typing import Union

from program.code.opt_args import OptArg
from tkinter import *
from tkinter.ttk import *

import pickle

class App:

    def __init__(self, parent : Tk, filepath : str = None, arg_dict : dict = {}) -> None:
        self.parent = parent
        self.arg_dict = arg_dict

        #defaults
        #There are none right now

        for key in arg_dict:
            setattr(self, key, arg_dict[key])

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

        self.genOutput()

    def genOutput(self) -> None:
        sections = {
            "Simulation_data" : self.sim_data,
            "Seller data" : self.seller_data,
            "Buyer data" : self.buyer_data
        }
        for section_name in sections:
            section = Section(section_name, sections[section_name])

class Section(App):

    def __init__(self, data : dict, arg_dict : dict = {}) -> None:
        frame = Frame(self.parent)
        frame.pack(side=TOP)

        for data_key in data:
            val = data[data_key]
            #TODO make output class depending on data contents


class graph_display:

    def __init__(self) -> None:
        pass

        
class Controller: 

    @staticmethod
    def startUI(filepath : str, params : dict = {}) -> None:
        root = Tk()
        app = App(root, filepath, params)
        root.mainloop()