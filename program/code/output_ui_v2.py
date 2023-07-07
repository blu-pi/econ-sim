from typing import Union
from tkinter import *
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from program.code.data_handle import *

SingleOutput = float | int | str | bool
sections = ["Buyers", "Sellers", "Simulation"] #possible sections of data

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

    heading_font = ('Arial', 18)
    sub_heading_font = ('Arial', 12)


    def __init__(self, parameters : dict = {}) -> None:
        self.root = Tk()
        self.root.winfo_toplevel().title("Data Visualiser")
        self.parameters = parameters

        self.data_handler = DataHandler(parameters)

        #------FRAMES------
        top_frame = Frame(self.root)
        top_frame.pack(side=TOP)

        button_frame = Frame(self.root)
        button_frame.pack()

        #------LABELS------
        title_label = Label(top_frame, text= "Select which stats to view", font=App.heading_font)
        title_label.pack(side=TOP)

        #------BUTTONS------
        self.section_buttons = []
        for section_name in sections:
            btn = Button(button_frame, text=section_name)
            btn.configure(command= lambda name=section_name: self.makeWindow(name))
            btn.pack(side=RIGHT)
            self.section_buttons.append(btn)


        self.root.mainloop()

    def makeWindow(self, text : str) -> None:

        newWindow = Toplevel(self.root)
        newWindow.title(text + " selection") 

        frame = Frame(newWindow)
        frame.pack()

        title_label = Label(frame, font=App.heading_font)  
        title_label.configure(text="Select which type of {} information you want to see:".format(text))
        title_label.pack(side=TOP)

        individual_button = Button(frame, text="Individual")
        individual_button.configure(command= lambda section_name = text: self.displayData(section_name, is_individual=True))
        individual_button.pack(side=LEFT)

    def displayData(self, section_name : str, is_individual : bool) -> None:
        pass

    def requestData(self, section_name : str) -> dict:
        pass
