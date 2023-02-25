import numpy as np
import math

class Distribution:

    def __init__(self, start : float, end : float, steps : int, isContinuous : bool = True) -> None:
        assert(self.start < self.end)
        self.values = None
        self.start = start
        self.end = end
        self.steps = steps
        self.isContinuous = isContinuous

class Linear(Distribution):

    def __init__(self, start: float, end: float, steps : int, isContinuous: bool = True) -> None:
        super().__init__(start, end, steps, isContinuous)
        self.values = self.generate()

    def generate(self) -> list[float]:
        current = self.start
        range = self.end - self.start
        step_amount = range / self.steps
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
    Exponentially increasing growth between given 2 values. 
    Formula used is e^xb where x is current step number and b = (ln(max) - ln(min)) / num_steps. Ln = Log base e NOT log base 2.
    This 'transforms' function e^x so that it passes through min and max points. 
    """
    

    def __init__(self, start: float, end: float, steps : int, isContinuous: bool = True) -> None:
        super().__init__(start, end, steps, isContinuous)
        self.values = self.generate()
    
    def generate(self, steps : list) -> list[float]:
        current = math.log(self.start)
        range = math.log(self.end) - current
        step_amount = range / self.steps
        out = [self.start]
        for i in range(self.steps - 1):
            current += step_amount
            #actual value of current must be maintained and not rounded else solution won't be strictly linear!
            if self.isContinuous:
                out.append(math.e ** current)             
            else:
                out.append(round(math.e ** current))
        return out

class Logarithmic(Distribution): #INCOMPLETE TODO

    def __init__(self, start: float, end: float, steps : int, isContinuous: bool = True) -> None:
        super().__init__(start, end, steps, isContinuous)
        self.values = self.generate()
    
    def generate(self, steps : list) -> list[float]:
        return np.logspace(np.log(1.08), np.log(1.48), 10, base=np.exp(1))   