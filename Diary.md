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

Revamped eval system for price change action to better reflect return types. Still working on decision making. Needs thorough testing after completion. Moved some methods to more appropriate classes. This type of refactoring will continue throughout.
Want to implement behaviour class for sellers to use in case of imperfect information but I'm worried about it's potential complexity and time. Testing current implementation for eval, fixing problems encountered.

Testing of seqEval for perfect information is now complete. Lessons were learnt. Now going to try and implement a full simulation run by starting the simulation after creating the graph and ending it at a fixed number of loops or looking for an equilibrium/cycle. Progress! 
Extra features initially intended to be in final product that aren't yet implemented will be implemented later. For now I need the simulation to run successfully with existing parameters.

Started on basic template for setup of the simulation. Needs to be tested! Methodology may change. 

Completed sim setup but need to test it. Working on UI for data input. Still need to do data output and implementation of extra features which I planned to include. Generally most goals are marked with #TODO comments throughout the code. 
Decided to use tkinter for UI since it comes in the default python package and I have previous experience using it.

Working on setup UI. Going to use existing valid arg lists/dicts to generate entry fields. Decided to make one class for storing and checking all possible parameters that can be passed to the simulation. 
This makes it easier to maintain and makes the implementation of the dynamic UI creating easier. Essentially the UI will automatically look which parameters the simulation can take and will generate entry fields accordingly.
This makes it much simpler to add extra features in future. This maintainability has also been a focus for the code base since the beginning.

Completed basic workin UI. Now need to connect UI with sim setup class so the simulation can be started through UI input. Also still need to update exisitng code to use reworked opt_arg dictionary format.
Started debugging existing implementation. Adding robust type security for inputs. No user input should be able to crash the simulation. 
Might need to remove old .pyc files from version tracking as they could potentially interfere and aren't functionally useful in any way. 
They were simply added to the gitignore too late. 

Debug stage 1 complete, the code runs to the end without crashing for default values. Now other values need to be tested including edge cases. "The End." console output is reached meaning the simulation is successfully running
and terminating itself through proper means. After completing more debugging I will work on most important additional features I wanted to add. 

Added circle graph type. Restructured Graph generation as original code wasn't flexible enough. Debugged infinite loop caused by __eq__ comparisons with buyers and sellers. Comparing buyer equality required comparing who they buy from. This starts comparing sellers which requires comparing who they sell to. I have no idea how this didn't casue an infinite loop earlier. Fixed removing overriden __eq__ methods as they are just not needed. They were written very early in development when I thought they were needed. 
Might use tkinter .ttk for better looking UI, seems simple enough. 

Ended up using ttk, it reeally was simple and looks much, much better. Refactored parts of Graph class making Circle implementation much cleaner (Was previously pretty bad). Added descriptions for existing parameters.
Planning on rewriting Graph class to better utilise oop but I'm not sure if I will. Feels like it might be a waste of time.
Abandoned Graph reqrite for now. Added Tree Graph to available graph types. Completed testing for it. Planning to add more variations of trees in future.

Wrote initial code for exploring "local minima" problem that sellers face when they have large amounts of Buyers. Added Descriptions for newly added parameters. 
Began Adding distribution classes to distribute numerical arguments in varying ways. Will give users the power to select how values should be distributed. This is based on the examples.py implementation.

Began adding BuyerCollection class to implement utility distribution. Additionally, it will be used in decision making logic to clean up code. Every collection is an Edge. Added implementations for some distributions but still need to test.
Need to be able to draw graph of any BuyerCollection as this is used in Simultaneous + perfect info seller decision-making. Will also be useful when generating output from simulation. 
Current main objectives outlined above other than that just complete sim output and minor polishing changes then initial release is ready.

Working on adding more distributions. Numpy.logspace had me stuck for a while... Need to figure out how to prevent or deal with buyer_util being set to 0 by user. Value or even min_value of 0 breaks most of the distributions.
Testing of new content partially complete. Will rewrite existing code to always use Collections and Distributions. Once that is done and tested, I'll work on producing output. 
Some of the old test files are outdated and no longer run. This is because the tested code has evolved too far for them to still apply. Generally testing is mostly done by running main.

Distributions and BuyerCollection now complete. Could use buyercollection in other parts of the code. Next is sim output (finally). After that I might work on other decision-making related things.

Working on collecting and then outputting relevant data during simulation. Decided to store data using pickle which allows python objects to be serialised and deserialised. Basically a python version of json.
At some point relevant data will be used to calculate all sorts of averages etc which will be displayed and plotted in the output screen. Also planning on reworking some code using the new buyercollection class.

Might pass all data directly from simulation to output without saving a copy and reloading it. Generally progressed with data collection and more of the output UI. Cleaned up some code with the power of hindsight.

Working on output UI, should be completed soon. As part of that work I need to process the output data a little to generate more interesting output.

Added more data collection to different aspects of the simulation. Mainly focused on Sellers. Also began processing data to be able to provide more interesting and meaningful output. Limited on time here so ambitions for output detail will be scaled back slightly. I'm still planning to add imperfect decision-making and a method for detecting nash equilibria. Last but not least, I still want to change the file structure to something more professional. 
Not only am I running out of time but from now on I also have to spend more time on the report which takes away from development time.

Restructured part of the BuyerCollection class to split some functionality into a new class "NamedDataPlot". This is a data structure for handling sets of related data to be graphed against each other. 
Now close to having initial data output ready.

Started implementing data analysis to accompany data plots. This way raw data can be graphed and data such as variance etc. can also be given with the graph. Did a lot of research ojn pandas library. 
Solution isn't yet tested and quite complicated. Might also be resource intensive. Whole approach could be abandoned if it's too much of a headache. Need to pass all data to output UI where I need to 
finish the logic to automatically create plots for output. Once again I add complexity when I really shouldn't... However, I do feel data-output is important for a simulation.

Doing a bunch of debugging. Learning a lot about more complex data handling. My implementation isn't perfect but actually not so bad. Code is working well! 
Also added opt args for output. Currently only with a test value but new ones can noew be added easily.

More work on displaying graphical data in output UI. Coming towards completions. Still needs some testing and polish.

Messing around with implementation for output UI and data generation for that UI. Many bug fixes. 

Fixed all known bugs. Now going through full testing. Output seems accurate to some extent. Might work on adding more graphs to give more detail on sim outcomes. This is the very minimum of a completed product.

Finally, it's all over now.

Or was it? Carrying on for fun... ah such fun. Let's see where I can take this.
Set initital goals in form of TODOs. 

Allowed saving of args used to start a simulation in a file.

Added loading new simulation from parameter file.

Began adding support for box plots. Working on data output.

More prep work for data output. Decided to rework the control flow and methodology for data processing. This will be done by the DataHandler class in data_handle.py file.
Ideally, data output will look better and be far more useful and dynamic depending on what the user is interested in seeing. It's quite a big change. ETA: not so soon.

Made a roadmap for future plans on paper in regards to data output.
Essentially:
- Modify data collection to ensure data is collected cleanly and efficiently
- Work on data processing in the DataHandler class.
- Work on brand new output UI system in output_ui_v2.py - this will be dynamic
- Add saving and loading of output data, eliminating the need to rerun a simulation with the same parameters twice (unless it's non-deterministic)
ETA: vaguely, 2 weeks depending on work ethic.

Worked on setting up backbone for new UI. Minor clean-up of other parts of the code.

Working on new implementation for data collection and then later data processing. These are prerequisites for further development of the new UI.

More work done on data collection + processing.

Completed initial rework of data collection and procesing for Sellers. Will test next and then implement for buyers. Finally, all this will be integrated into the new UI.
Also added new opt argument to determine the performance measure of a Seller.

Made progress on outputting data in new UI.