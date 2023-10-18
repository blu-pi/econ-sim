from typing import Union
from tkinter import *
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from program.code.data_handle import *

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

        self.lookup_frame = Frame(self.root)
        self.lookup_frame.pack(side=BOTTOM)

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

        self.newWindow = Toplevel(self.root)
        self.newWindow.title(text + " selection") 

        frame = Frame(self.newWindow)
        frame.pack()

        title_label = Label(frame, font=App.heading_font)  
        title_label.configure(text="Select which type of {} information you want to see:".format(text))
        title_label.pack(side=TOP)

        individual_button = Button(frame, text="Individual")
        individual_button.configure(command= lambda section_name = text: self.requestData(section_name, is_individual=True))
        individual_button.pack(side=LEFT)

        summary_button = Button(frame, text="Summary")
        summary_button.configure(command= lambda section_name = text: self.requestData(section_name, is_individual=False))
        summary_button.pack(side=LEFT)

    def requestData(self, section_name : str, is_individual : bool) -> None:
        pos = None
        if is_individual:
            #get user input
            pos = 2

        data_handler = DataHandler(parameters={})
        data : dict = data_handler.process(section_name, is_individual, pos)
        self.displayData(data, section_name, is_individual)
            
    def displayData(self, data : dict, section_name : str, is_individual : bool) -> None:
        self.newWindow.destroy()

        if is_individual:
            detail = "Individual"
        else:
            detail = "Average"
        title = "{} {}".format(detail, section_name)
        self.displays[title] = LookupContainer(self.lookup_frame, title, data)

class LookupContainer:

    def __init__(self, container : Tk, title : str, data : dict):

        self.displayed_figures = {}
        self.displayed_vals = {}

        self.container = container
        self.title = title
        self.data = data

        self.frame = Frame(self.container)
        self.frame.pack(side=BOTTOM, pady=10)

        self.title_label = Label(self.frame, text=self.title, font=App.heading_font)
        self.title_label.pack(side=TOP,padx=10)

        self.remove_button = Button(self.frame, text="remove")
        self.remove_button.configure(command= lambda a="": self.frame.destroy())
        self.remove_button.pack(side=TOP)

        self.show_conts()

    def show_conts(self):
        for title, contents in self.data.items():
            if isinstance(contents, Figure):
                self.displayed_figures[title] = FigureDisplay(title, figure=contents, container=self.container)
            if isinstance(contents, SingleOutput):
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