from program.code.agents import Seller, Buyer, Agent

class BuyerCollection:
    """A collection of buyers that all buy from exactly the same Sellers."""

    def __init__(self, buyers : list[Buyer]) -> None:
        assert(len(buyers) > 0)
        self.buyers = buyers
        self.buys_from = self.buyers[0].buys_from

    def makeGraph(self, show_output : bool = False) -> tuple:
        pass