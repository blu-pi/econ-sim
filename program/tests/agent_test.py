
import sys
  
# append the path of the parent directory
sys.path.append("./")

from program.agent import Agent


def test_agent():
    test_seller1 = Agent()
    test_seller2 = Agent()
    test_buyer1 = Agent(Agent.Type.Buyer, [test_seller1, test_seller2])
    print(type(test_seller1), type(Agent.Type.Seller))
    assert test_seller1.type == Agent.Type.Seller
    assert test_buyer1.type == Agent.Type.Buyer
    assert len(Agent.sellers) == 2
    assert len(Agent.buyers) == 1

test_agent()