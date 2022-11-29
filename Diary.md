First Diary entry. 
Testing git is working properly and adding basic file structure. Starting on base code.

Set up pytest, added line graph functionality. Testing Line graph functionality as well as constructors.
Can't get pytest to work so just use basic assert statements. Took ages for test module to be able to access program module so import errors were thrown. Fixed by moving test module into program module and messing with sys.path. This took soo long to fix
and I now hate anything to do with modules in python... Tests currently failing but I'm too exhausted to fix them right now. Will fix errors next.

Tests now pass. Added equality implementation to Agent class. Decided to change graph structures to make them individual classes and not just enum within environment class. This allows easier implementation of complex features and graph traversal. Also more readable!
PSA: Pytest isn't being used. Using vanilla implementation of assert in python.

Looked into using networkx library for graphing. Investigating best solution for graph generating, specifically which metrics should decide the graph shape. Certain properties can influence others so which should be specified and which should be a result of given paremeters. Maybe only presets should be allowed with minor variations possible through optional parameters. Decision will drastically effect constructor for Graph class so needs to be made before I start coding. 

Decided on how to rewrite environment/graph class. Now uses interface Graph which implemented graph types inherit. Finished rewriting Agents class. Agent is now an interface which Buyers and Sellers inherit from. Game theory code will go in Agents class. Working on finishing rewrite of Graph class. Changes are completly untested and old tests will not work. Began adding support for variable parameters for creating any Agent. This will allow the user to change Agent properties between simulations through a UI.
Can't test new graph class visually since networkx visualisation isn't working for some reason... will fix next.

Can now visually display networkx graph. Redid testing on rewritten classes. Fixed imports where needed. Offiacially finished rewrite.

Began preperations for running simulations. Implementation for Agent actions started. Planned how to implement agent decision making. Need to finish Agent actions then move to programming Agent decision making which will be absed on game theory. 
Will do basic research for graph traversal using networkx library. Will struggle to get basic simulations ready for Dec. 2nd. Changed file names to reflect that they define multiple types of the given class. 

Did some more testing for Actions class. Goals remain what they are above. Need to do more testing too.

Planning on initial direction for how to implement interesting and meaningful Agent decision-making. Must follow Game theory principles: rational agents, finite choices. 
Came up with the following idea: Buyers simply follow objective value function (cost - percieved utility) and if that's > 0 they buy. 
Sellers are more complicated. This is because Sellers don't have an objective way
to make decisions without cheating (having too much information). The predicted utility from raising or lowering prices can't be accurately predicted. This is because Buyers aren't predicatable from the perspective of the Seller as the Seller doesn't know the Buyer's percieved utility of the product they're selling. 
Solution for Sellers: Make multiple "Personalities" that have different decision making profiles. (Some may take more risk or be more aggressive etc.) The way these personalities are distributed among sellers will be determined at the start of the simulaton. There will also be a toggle to allow or disallow Sellers to change personality mid simulation.

Added docstrings to all classes. Also added to methods that aren't self-explanatory. Decided to split utility evaluation for Price Changes into objective and imperfect versions. Objective will use perfect information to calculate predicted utility while imperfect uses limited (and maybe more realistic) information to inform an estimate. Decided to first implement basic Game theory ideas and then optionally add imperfect information as an option later.