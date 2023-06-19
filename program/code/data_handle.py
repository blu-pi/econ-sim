from program.code.agents import *

class DataHandler:
    """
    Dedicated class for processing collected data in preparation for use in UI output.
    """

    def __init__(self, args: dict, dir = None) -> None:
        #TODO type limit for directory
        self.args = args
        self.dir = dir
        if self.dir != None:
            self.loadDataFile()
        self.seller_class_data = Seller.getClassStats()
        self.seller_data = Seller.getIndividualStats(get_complex=False)
        self.buyer_class_data = Buyer.getClassStats()
        self.buyer_data = Buyer.getCollectionStats()
        #self.sim_data =      

    def loadDataFile(self) -> object:
        #TODO try to unpickle from location given
        try:
            return True #return unpickled obj here
        except:
            return None

    def makeGeneralOutput(self) -> None:
        pass

    def makeSpecificOutput(self) -> None:
        pass
