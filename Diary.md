First Diary entry. 
Testing git is working properly and adding basic file structure. Starting on base code.

Set up pytest, added line graph functionality. Testing Line graph functionality as well as constructors.
Can't get pytest to work so just use basic assert statements. Took ages for test module to be able to access program module so import errors were thrown. Fixed by moving test module into program module and messing with sys.path. This took soo long to fix
and I now hate anything to do with modules in python... Tests currently failing but I'm too exhausted to fix them right now. Will fix errors next.

Tests now pass. Added equality implementation to Agent class. Decided to change graph structures to make them individual classes and not just enum within environment class. This allows easier implementation of complex features and graph traversal. Also more readable!
PSA: Pytest isn't being used. Using vanilla implementation of assert in python.

Looked into using networkx library for graphing. Investigating best solution for graph generating, specifically which metrics should decide the graph shape. Certain properties can influence others so which should be specified and which should be a result of given paremeters. Maybe only presets should be allowed with minor variations possible through optional parameters. Decision will drastically effect constructor for Graph class so needs to be made before I start coding. 

Decided on how to rewrite environment/graph class. Now uses interface Graph which implemented graph types inherit. Finished rewriting Agents class. Agent is now an interface which Buyers and Sellers inherit from. Game theory code will go in Agents class. Working on finishing rewrite of Graph class. Changes are completly untested and old tests will not work. Began adding support for variable parameters for creating any Agent. This will allow the user to change Agent properties between simulations through a UI.