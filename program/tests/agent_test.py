
import sys
  
# append the path of the parent directory
sys.path.append("./")

from program.code.agent import *


def test_agent():
    # these pass
    test_seller1 = Seller()
    test_seller2 = Seller()
    test_buyer1 = Buyer([test_seller1, test_seller2])
    assert isinstance(test_seller1, Seller) and isinstance(test_seller1, Agent)
    assert isinstance(test_buyer1, Buyer) and isinstance(test_buyer1, Agent)
    assert len(Agent.sellers_arr) == 2
    assert len(Agent.buyers_arr) == 1
    assert test_seller1 in test_buyer1.buys_from

test_agent()