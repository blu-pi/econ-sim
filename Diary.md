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

Added optional argument dictionary checker which removes invalid optional arguments passed to constructors. Added custom data structure for decision matrices which will inform agent decisions. Nether has yet been tested and isn't yet being used by the code. Next steps are testing them and using them in the code. Have been focusing on the "perfect information for sellers" implementation. Will get an extension for dec 2 deadline.

Began fixing circular import issue by adding additional interface between Agents and the actions classes. Planning on also using library for game theory stuff rather than writing it myself. Might keep existing game theory code as custom made solution to non-standard game theory application. (this may just be an incredibly stupid idea but let's see)
Need to fix tests (their imports are also broken). Short-term goals are now getting a basic simulation to run and then increasing complexity. Solutions are made with possible implementation od extra features in mind to allow for easy increase in simulation complexity. E.g. Theoretically support for Agents that are both Buyers AND Sellers exists right now but may not be utilised until later in development.

Current progress for fixing import issues and adding decision making functionality to agents. Now decided I will try to restructure code so that actions are inner classes of specific agents. The use case of inner/outer classes is as follows:
Every outer class obj needs an inner class obj and an inner class obj won't be used without an outer class obj. E.g. Every Agent has decisions they can make and no decision will be used without an agent object. This will however make that module much bigger and may also cause it to need a renaming. Making new bramch for that after this.

Found solution for the imports which is importing actions only when locally in methods where they are needed. I also removed agent_actions_interface class (it was a very dumb idea). Implemented method for agents to pick the action they calculate as having the most value to them. Next few steps are mostly testing and then implementing the game theory library. Added arguments for Buyers, Sellers and Graphs to valid argument lists. Added valid argument lists for specific graph shapes. Added more docstrings to newly written methods.

Began working on game theory usage for decision making. Decided to use my own Decision matrix implementation as nashpy library functionality isn't really needed as much. Might use it infuture. 
Investigated the differences between different ways of applying agent decision making. Agents could make decisions vertually simultaneously each turn where the effect of one agent's decision won't directly inform another agent's decision.
Alternatively agents could make decisions sequentially once being put in a random order. The chosen method will effect use cases of the simulation and abstract different detail out of the simulation. Might offer an option for both but it's complicated to implement and may have limited benefits. If I only implement one then it would be Sequential decision making as it works for all current and planned simulation parameters. (e.g. level of information posessed by Sellers)
Other unforseen problems could arise here. Feels like there's no good solution. More detail in report. 
Ended up splitting decision making process between simultanious with perfect information, sequential with perfect information and the rest (any imperfect information). Working on solution now.
Added simulation.py which will be the top-level class handling all aspects of the simulation.

After advice from supervisor, I added option for having Sellers make decisions in random sequential order as well as simultaniously. Solution for Simultanious + perfect information on seller decision-making is in the conceptual stage. All other combinations are ready and just have to be written which is what I'm doing now. 