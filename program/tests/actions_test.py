import sys
  
# append the path of the parent directory
sys.path.append("./")

from program.code.graphs import *
from program.code.agents import *
from program.code.actions import *

#test setup
seller1 = Seller()
seller2 = Seller()
seller3 = Seller()
buyer1 = Buyer([seller1, seller2])
buyer2 = Buyer([seller2, seller3])

def test_constructors():
    buy_obj1 = Buy(buyer1)
    print(buy_obj1)
    buy_obj2 = Buy(buyer2)
    print(buy_obj2)
    buy_obj1.apply()
    buy_obj2.apply()
    assert buy_obj1 != buy_obj2
    assert len(buyer1.action_history) == 1


test_constructors()