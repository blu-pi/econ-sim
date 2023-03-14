import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple

class NamedDataPlot:
    """
    Data structure representing related data to be displayed in a pyplot. This class doesn't itself make plots.
    Mainly used to streamline data output.
    """

    time_axis_name = "time"
    placeholder_name = "Placeholder"

    def __init__(self, x_vals : Tuple[str,list[float]], y_vals : Tuple[str,list[float]], plot_name : str = None) -> None:
        #!IMPORTANT! in x_vals if the 'str' aspect of the tuple is EXACTLY equal to NamedDataPlot.time_axis_name then the remaining data is ignored.
        #This is since it assumes the data is graphed over time with each interval being 1 step of t. 
        #y_vals data will then be graphed by their position in the list as the point in time. 
        self.y_title = y_vals[0]
        self.y_vals = y_vals[1]
        self.x_title = x_vals[0]
        if self.x_title == NamedDataPlot.time_axis_name:
            #ugly but simplest solution in practise
            self.x_vals = list(np.arange(len(self.y_vals)))
        else:
            self.x_vals = x_vals[1]

        self.plot_name = plot_name
    
    def setName(self, name : str) -> None:
        self.plot_name = name

    def setTitles(self, x_title : str = None, y_title : str = None):
        """Change one or both of the axis titles of a NamedDataPlot"""
        if x_title != None:
            self.x_title = x_title
        if y_title != None:
            self.y_title = y_title

    def combine_y(self, other : 'NamedDataPlot', new_title : str = None) -> 'NamedDataPlot':
        """Add data element-wise while keeping x axis the same. Used when combining plots of BuyerCollections that share a single Seller."""
        if not(self.x_vals == other.x_vals):
            print("Warning x-axis don't match. Might mean invalid data (also might not idk)")
            print(self.x_vals)
            print("Compared to")
            print(other.x_vals)
        new_x_title = self.x_title
        new_y_title = other.y_title
        if self.x_title != other.x_title:
            new_x_title = NamedDataPlot.placeholder_name
        if self.y_title != other.y_title:
            new_y_title = NamedDataPlot.placeholder_name        
        new_y = [sum(x) for x in zip(self.y_vals, other.y_vals)]
        return NamedDataPlot((new_x_title,self.x_vals),(new_y_title,new_y),new_title)

    def mean(self, other : 'NamedDataPlot') -> 'NamedDataPlot':
        """Produce new NamedDataPlot with element-wise mean of passed data."""
        #Could enforce checks here to ensure NDPs storing different data aren't averaged.
        avg_x = [np.mean(x) for x in zip(self.x_vals, other.x_vals)]
        avg_y = [np.mean(x) for x in zip(self.y_vals, other.y_vals)]
        x_title = self.x_title if self.x_title == other.x_title else NamedDataPlot.placeholder_name
        y_title = self.y_title if self.y_title == other.y_title else NamedDataPlot.placeholder_name
        new_name = self.plot_name if self.plot_name == other.plot_name else None
        return NamedDataPlot((x_title,avg_x),(y_title,avg_y), new_name)

    @staticmethod
    def meanOfList(plots : list['NamedDataPlot']) -> 'NamedDataPlot':
        """Produce new NamedDataPlot with element-wise mean of passed data."""
        assert(len(plots) > 0)

        if len(plots) == 1:
            return plots[0]
        
        running_average_plot = plots.pop(0)
        for current_plot in plots.copy():
            assert(isinstance(current_plot, NamedDataPlot))
            running_average_plot._mean(current_plot)
            
        return running_average_plot
    
    def show_output(self) -> None:
        """Create pyplot for given data."""
        if self.plot_name != None:
            plt.title(self.plot_name)
        
        plt.xlim(0, max(self.x_vals))
        plt.ylim(0, max(self.y_vals))

        plt.grid()

        plt.xlabel(self.x_title)
        plt.ylabel(self.y_title)

        plt.plot(self.x_vals, self.y_vals)
        plt.show() 
