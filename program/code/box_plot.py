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
        plt.figure(figsize=(8, 6))
        plt.boxplot(self.data)
        if self.title is not None:
            plt.title(self.title)
        plt.xlabel(self.axis_name)
        plt.ylabel('Y-axis label')
        plt.show()

    def getFigure(self) -> Figure:
        """Get a reference to an image (of the box plot) which can later be used in a Tkinter display."""
        fig, ax = plt.subplots()  # Create a new figure and axes
        self.data.plot(kind='box', ax=ax)  # Create a boxplot on the axes
        return fig