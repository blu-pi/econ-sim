from pandas import Series
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class BoxPlot:
    """
    A way to display a pandas Series as a BoxPlot in a standardised way.
    """

    def __init__(self, data : Series, title : str = None, axis_name : str = None) -> None:
        self.data = data
        self.title = title
        self.axis_name = axis_name

    def setTitle(self, title : str) -> None:
        self.title = title

    def setAxisName(self, axis_name : str) -> None:
        self.axis_name = axis_name

    def showOutput(self) -> None:
        ax = self.data.plot.box(column=self.axis_name)
        ax.show()

    def getFigure(self) -> Figure:
        """Get a reference to an image (of the box plot) which can later be used in a Tkinter display."""
        pass