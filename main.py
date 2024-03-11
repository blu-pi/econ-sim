
from interface.in_ui import App

from structs.opt_args import OptArg
from tkinter import *
from tkinter.ttk import *


if __name__ == "__main__":

    dict_names = ["Simulation", "Buyer", "Seller", "Output"]
    root = Tk()
    app = App(root, dict_names, OptArg.getAllParams())
    root.mainloop()