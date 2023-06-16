
class DataHandler:
    """
    Dedicated class for processing collected data in preparation for use in UI output.
    """

    def __init__(self, args: dict, seller_data: dict = None, buyer_data: dict = None, sim_data: dict = None) -> None:
        self.args = args
        self.seller_data = seller_data
        self.buyer_data = buyer_data
        self.sim_data = sim_data
        
    def makeGeneralOutput(self) -> None:
        pass

    def makeSpecificOutput(self) -> None:
        pass
