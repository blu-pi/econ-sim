import sys
  
# append the path of the parent directory
sys.path.append("./")

from program.code.collection import *
from program.code.agents import *
from program.code.distribution import *

import numpy as np
import matplotlib.pyplot as plt

#DISTRIBUTION TEST

lin_dist = Linear(5,100,11)
exp_dist = Exponential(5,100,11)

plt.xlim(0, 11)
plt.ylim(0, 110)

plt.grid()

plt.xlabel("Step num")
plt.ylabel("Value")

plt.plot(range(11), lin_dist.values)
plt.plot(range(11), exp_dist.values)
plt.show()

#COLLECTION TEST (MIGHT USES DISTRIBUTIONS)

buyer_args = {
    "util_distribution" : "Random",
    "min_util" : 5,
    "max_util" : 30
}

seller_args = {
    "price_change_amount" : 1,
    "price_steps" : 2
}

sellers = []
for x in range(2):
    sellers.append(Seller(arg_dict = seller_args))

buyers = []
for x in range(10):
    buyers.append(Buyer(sellers,arg_dict = buyer_args))

collection = BuyerCollection(buyers)
#collection.makeGraph(show_output=True)
collection.makeGraph((0,35), 0.1, show_output=True)
