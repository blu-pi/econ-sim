import numpy as np

class Distribution:
    """General system for generating a fixed amount of numbers between 2 values. Only rule is that it must return a list of values containing all steps including the start and end values."""

    def __init__(self, start : float, end : float, steps : int, isContinuous : bool = True) -> None:
        assert(start < end)
        self.values = None
        self.start = start
        self.end = end
        self.steps = steps
        self.isContinuous = isContinuous

class Linear(Distribution):
    """Yeah this is basically just np.arange but worse. No I don't plan on changing it."""

    def __init__(self, start: float, end: float, steps : int, isContinuous: bool = True) -> None:
        super().__init__(start, end, steps, isContinuous)
        self.values = self.generate()

    def generate(self) -> list[float]:
        #wrote it myself bc I was too lazy to use a library 
        current = self.start
        val_range = self.end - self.start
        step_amount = val_range / (self.steps - 1) #always include max val.
        out = [self.start]
        for i in range(self.steps - 1):
            current += step_amount
            #actual value of current must be maintained and not rounded else solution won't be strictly linear!
            if self.isContinuous:
                out.append(current)             
            else:
                out.append(round(current))
        return out

class Exponential(Distribution):
    """
    Exponentially increasing growth between given 2 values. Uses base e.
    """

    def __init__(self, start: float, end: float, steps : int, isContinuous: bool = True) -> None:
        super().__init__(start, end, steps, isContinuous)
        self.values = self.generate()
    
    def generate(self) -> list[float]:
        return np.logspace(np.log(self.start), np.log(self.end), self.steps, base=np.e)
