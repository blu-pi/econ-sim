import sys
  
# append the path of the parent directory
sys.path.append("./")

from program.environment import Graph
from program.agent import Agent

def test_line_graph():
    env = Graph() #line graph is the default
    current = Agent.sellers[0]
    for i in range(len(Agent.buyers) + len(Agent.sellers)):
        next_type = Agent.Type.Buyer
        neighbours = current.customers
        if i % 2 == 0:
            next_type = Agent.Type.Seller
            neighbours = current.buys_from
#carry on later, changing env structure concept.
        
