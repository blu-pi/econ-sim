import numpy as np

class Distribution:

    def __init__(self, start : float, end : float, steps : int, isContinuous : bool = True) -> None:
        assert(self.start < self.end)
        self.start = start
        self.end = end
        self.steps = steps
        self.isContinuous = isContinuous
    
    def generate(self, steps : list) -> list[float]:
        pass

class Linear(Distribution):

    def __init__(self, start: float, end: float, steps : int, isContinuous: bool = True) -> None:
        super().__init__(start, end, steps, isContinuous)

    def generate(self, steps : list) -> list[float]:
        np.logspace(np.log(1.08), np.log(1.48), 10, base=np.exp(1))

class Exponential(Distribution):

    def __init__(self, start: float, end: float, steps : int, isContinuous: bool = True) -> None:
        super().__init__(start, end, steps, isContinuous)
    
    def generate(self, steps : list) -> list[float]:
        np.logspace(np.log(1.08), np.log(1.48), 10, base=np.exp(1))