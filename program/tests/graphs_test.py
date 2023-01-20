import sys
  
# append the path of the parent directory
sys.path.append("./")

from program.code.graphs import *
#from program.code.agents import *

def test_line_graph():
    #passes (makes correct graph checked visually)
    graph = Line(20) #20 seller line graph
    
test_line_graph()
        
