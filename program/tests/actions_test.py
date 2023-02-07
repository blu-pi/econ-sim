import sys
  
# append the path of the parent directory
sys.path.append("./")

from program.code.graphs import *
from program.code.agents import *
from program.code.actions import *

def test_constructors():
    #test setup
    seller1 = Seller()
    seller2 = Seller()
    seller3 = Seller()
    buyer1 = Buyer([seller1, seller2])
    buyer2 = Buyer([seller2, seller3])

    buy_obj1 = Buy(buyer1)
    print(buy_obj1)
    buy_obj2 = Buy(buyer2)
    print(buy_obj2)
    buy_obj1.apply()
    buy_obj2.apply()
    assert buy_obj1 != buy_obj2
    assert len(buyer1.action_history) == 1

def test_seqEval():
    s_args = {
        "PERFECT_INFORMATION" : []
    }
    b_args = {
        "percieved_util" : 10
    }
    graph = Line(20, seller_args=s_args, buyer_args=b_args)
    Seller.setSequential() #only thing implemented
    s1 = Agent.sellers_arr[6]
    s2 = Agent.sellers_arr[7]
    buyer = Agent.buyers_arr[6]
    assert(isinstance(s1, Seller))
    assert(isinstance(s2, Seller))
    assert(isinstance(buyer, Buyer))
    assert(buyer.buys_from == [s1,s2])
    print("Buyer utility: {}".format(buyer.percieved_utility))
    a1 = s1.findBestAction()
    a2 = s2.findBestAction()
    print("{}\n{}".format(a1,a2))
    a1.apply()
    a2.apply()
    print(buyer.findBestAction())
    #Read console output and see if it makes sense, at time of writing it does!

#IMPORTANT only run 1 tester method at a time or they'll clash!

#test_constructors()
test_seqEval()