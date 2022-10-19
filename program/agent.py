from enum import Enum
from random import Random

class Agent:

    class Type(Enum):
        Seller = "Seller",
        Buyer = "Buyer",
        Both = "Buyer and Seller"

    sellers = []
    buyers = []

    def __init__(self, type = Type.Seller, vendors = []):
        if type == Agent.Type.Seller or type == Agent.Type.Both:
            self.product_price = 0
            self.customers = [] #list of all agents looking to buy from this agent. Not used for decision making. Populated later
            Agent.sellers.append(self)
        if type == Agent.Type.Buyer or type == Agent.Type.Both:
            self.percieved_utility = Random.randint(1,10)
            self.vendors = vendors #list of all agents this buyer is looking to purchase from. Is used in decision making
            Agent.buyers.append(self)