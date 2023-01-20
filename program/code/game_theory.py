import math
from typing import Union


#concept class, may be superceded by library made for game theory - should have thought about this earlier
class DecisionMatrix: #only supported for Seller vs Seller
    """
    Data structure mimicking a matrix storing a Decision matrix for 2 Sellers 'competing' for the same buyer. 
    Values are accessed by passing 1 decision name for each Seller. Rows and collumns can also be accessed by name using getRow / get collumn.
    Every getter also ahs a setter with the same naming convention.
    """

    def __init__(self, size : int, axis_labels : list[str]) -> None:
        self.size = size
        self.axis_labels = axis_labels
        self.__matrix = []
        self.__createEmpty()

    def __str__(self) -> str:
        return str(self.__matrix) #Can be fully expanded if needed

    def __createEmpty(self) -> None:
        for y in range(self.size):
            self.__matrix.append([])
            for x in range(self.size):
                self.__matrix[y].append(0)

    def __nameToIndex(self, name : str) -> int:
        if name not in self.axis_labels:
            raise ValueError("Seller Choice {val} doesn't exist in this decision matrix".format(val = name))
        return self.axis_labels.index(name)
    
    def __indexToName(self, index : int) -> str:
        if index < len(self.axis_labels):
            return self.axis_labels[index]
        else:
            raise IndexError("Invalid index {val} for Decision Matrix of size {size}".format(val = index, size = self.size))

    def get(self, x : str, y : str) -> Union[int, float]:
        return self.__matrix[self.__nameToIndex(x)][self.__nameToIndex(y)]

    def getRow(self, row_name : str) -> list[int]:
        out = []
        for y in self.axis_labels:
            out.append(self.get(row_name, y))
        return out

    def getCollumn(self, collumn_name : str) -> list[int]:
        out = []
        for x in self.axis_labels:
            out.append(self.get(x, collumn_name))
        return out

    def set(self, x : str, y : str, val : Union[int, float]) -> None:
        self.__matrix[self.__nameToIndex(x)][self.__nameToIndex(y)] = val
    
    def setRow(self, row_name : str, val : list[int]) -> None:
        if len(val) != self.size:
            raise ValueError("Given row isn't the correct size for Decision Matrix, expected size: {0} but got {1}".format(self.size, len(val)))
        i = 0
        for y in self.axis_labels:
            self.set(row_name, y, val[i])
            i += 1

    def setCollumn(self, collumn_name : str, val : list[int]) -> None:
        if len(val) != self.size:
            raise ValueError("Given row isn't the correct size for Decision Matrix, expected size: {0} but got {1}".format(self.size, len(val)))
        i = 0
        for x in self.axis_labels:
            self.set(x, collumn_name, val[i])
            i += 1
