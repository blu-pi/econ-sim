from program.code.agents import *
from program.code.actions import *
from typing import Union, Any

class ActionInterface:

    def __init__(self, agent : Agent) -> None:
        self.agent = agent
        self.action = None

    def getValue(self) -> float:
        if hasattr(self.action, 'eval'):
            return self.action.eval()
        else:
            print("'{action}' doesn't have any eval method! Critical error, must fix".format(action = self.action))  
            exit(0)  
            
    def setAction(self, action : Union[BuyerAction, SellerAction]) -> bool:
        if isinstance(self.agent, Buyer) and not isinstance(action, SellerAction):
            self.action = action
            return True
        if isinstance(self.agent, Seller) and not isinstance(action, BuyerAction):
            self.action = action
            return True
        else:
            return False

    def hasAction(self) -> bool:
        return self.action != None


    #method graveyard, following methods may or may not be resurrected from the dead. (Not used right now but could be useful later)
    #TODO remove before release. Definitely won't be forgotten 
    @staticmethod
    def stringToClassReference(val : str) -> Any:
        try:
            return eval(val) #different eval to the methods in Actions class
        except:
            print("Warning: Class name {val} could not be referenced! Either it can't be accessed or it doesn't exist.".format(val=val))
            return None