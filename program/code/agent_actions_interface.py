from program.code.agents import *
from program.code.actions import *

class ActionInterface:

    def __init__(self, action) -> None:
        self.action = action

    @staticmethod
    def getPossibleActions(agent : Union[Buyer,Seller]) -> list[str]:
        actions = []
        if isinstance(agent, Buyer):
            actions.append(BuyerAction.possible_actions)
        if isinstance(agent, Seller):
            actions.append(SellerAction.possible_actions)
        #the actions all agents can do
        actions.append(AgentAction.possible_actions)

        return actions

    def getActionValues(actions):
        pass #TODO call eval functions 