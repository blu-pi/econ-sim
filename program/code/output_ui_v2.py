from typing import Union
from tkinter import *
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

SingleOutput = float | int | str | bool
Sections = ["Buyers", "Sellers", "Simulation"] #possible sections of data

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


    def __init__(self, parent : Tk, parameters : dict = {}) -> None:
        parent.winfo_toplevel().title("Data Visualiser")
        self.parent = parent
        self.parameters = parameters

        select_frame = Frame(parent)
        select_frame.pack(side=TOP)

        sellers_button = Button(select_frame, text="Sellers", command=self.makeWindow)
        sellers_button.pack(side=RIGHT)

    def makeWindow(self) -> None:
        print("test")


root = Tk()

app = App(root)

root.mainloop()