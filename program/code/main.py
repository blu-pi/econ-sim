import sys

sys.path.append("./")

from program.code.simulation import Simulation
from program.code.opt_args import *
from tkinter import *

# column_names, eventually this could be parsed from 'COLUMNS'. Currently it is
# used to insert the data. 

SIM_PARAMS = [('type', 'TEXT'), ('manufacturer', 'TEXT'), 
        ('focal_length', 'TEXT'), ('wavelength', 'TEXT'),
        ('diameter', 'TEXT'), ('comment', 'TEXT')]

B_PARAMS = [('type', 'TEXT'), ('Manufacturer', 'TEXT'), 
        ('focal_length', 'TEXT'), ('wavelength', 'TEXT'),
        ('diameter', 'TEXT'), ('comment', 'TEXT')]

S_PARAMS = [('type', 'TEXT'), ('manufacturer', 'TEXT'), 
        ('focal_length', 'TEXT'), ('wavelength', 'TEXT'),
        ('diameter', 'TEXT'), ('comment', 'TEXT')]

PARAMS = [SIM_PARAMS,B_PARAMS,S_PARAMS]

class entry_field:
    def __init__(self, parent, colName):

        self.frame = Frame(parent)
        self.frame.pack(side = TOP)
        
        self.label = Label(self.frame, text = colName)
        self.label.configure(width = 15)
        self.label.pack(side = LEFT)

        self.entry = Entry(self.frame)
        self.entry.pack(side = LEFT)
        self.value = lambda : self.entry.get()

        self.holdButton = Button(self.frame, command = self.hold)
        self.holdButton.configure(text = 'Hold')
        self.holdButton.pack(side = RIGHT)

    def hold(self):
        print('derp')

class drop_down:
    def __init__(self, parent, colName) -> None:
        pass


class App:
    def __init__(self, parent, columns, title):
        self.myParent = parent
        self.columns = columns
        self.title = title + " arguments:"
        #self.colNames = get_colNames(COLUMNS)

        self.Container = Frame(parent)
        self.Container.pack()
        
        self.entrycont = Frame(self.Container)
        self.entrycont.pack(side = TOP)

        self.title_label = Label(self.entrycont,text=self.title)
        self.title_label.pack()

        self.make_buttons(self.myParent, self.columns)

        # Next/esc container
        self.next_esc = Frame(self.Container)
        self.next_esc.pack(side = BOTTOM)

        # Next button.
        self.nextButton = Button(self.next_esc, command = self.nextItem)
        self.nextButton.configure(text = 'Next')
        self.nextButton.pack(side = LEFT)

        # Escape the window.
        self.Container.bind('<Escape>', self.quit)

    def quit(self, event):
        self.myParent.destroy()
        print('herp')

    # Make data entry buttons.
    def make_buttons(self, parent, column_names):
        #self.colName for colName in column_names
        self.factory = {}
        for i in column_names:
            colName = i[0]
            self.factory[colName] = entry_field(self.entrycont, colName)

        
    # Next button handeler.
    def nextItem(self):
        # get data from buttons
        data = []
        for i in self.columns:
            colName = i[0]
            data.append(self.factory[colName].value())
        print(data)

print(sys.path)
root = Tk()
app = App(root, B_PARAMS, "test")
#sim = App(root,Simulation.valid_parameters,"Simulation")
root.mainloop()
#TODO work on this to make subsections!