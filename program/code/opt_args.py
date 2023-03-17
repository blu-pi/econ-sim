from typing import Union

#static
class OptArg:
    """
    Single class for storing all allowed parameters that can be passed to the simulation either directly by the user or implicitly by the program.
    Includes methods for checking passed parameter list/dictionaries to see if they are valid.
    ALL OTHER CLASSES import their respective 'possible argument' list or dictionary from here when they are initialised!
    """
    _all_parameters = []

    #FORMAT EXPLANATION for parameter dictionaries:
    #'..' is inspired by haskell. Logically serves the same function but simpler. Implies a range between l[n-1] and l[n+1]. Also implies numerical data
    #List containing values without a '..' is a whitelist of accepted values.
    #also possible is an explicit list of values as long as those don't countain the literal ".." mentioned earlier.

    #sim parameters are generic top-level parameters. Other are more specific but there is some overlap. 
    sim_parameters = {
        "num_sellers" : [2,"..",1000],
        "graph_type" : ["Line", "Circle","Tree"],
        "SEQ_DECISIONS" : [True,False],
        "max_iterations" : [1,"..",1000],
        "buyers_per_seller_pair" : [1,"..",10]
    }
    _all_parameters.append(sim_parameters)
    
    #logically, min and max util have tighter restrictions but they are checked later. e.g. min can't be bigger than max and its implications.
    buyer_parameters = {
        "percieved_util" : [0,"..",100],
        "util_distribution" : ["Random","Linear","Exponential"],
        "min_util" : [0,"..",100],
        "max_util" : [0,"..",100]
    }
    _all_parameters.append(buyer_parameters)

    #TODO implement imperfect information and simultaneous (non-sequential) and all their new combinations in seller decision making.
    seller_parameters = {
        "PERFECT_INFORMATION" : [True,False],
        "price_change_amount" : [0,"..",5],
        "price_steps" : [0,"..",10],
        "product_price" : [0,"..",100]
    } 
    _all_parameters.append(seller_parameters)

    output_parameters = {
        "create_output_file" : [True,False]
    }
    _all_parameters.append(output_parameters)

    @staticmethod
    def getAllParams() -> list: #ugly solution but it will do
        """Returns a list containing all 'possible-parameter' dicts."""
        return OptArg._all_parameters

    @staticmethod
    def verifyDictKeys(to_check : dict, allowed : Union[list, dict]) -> Union[None, dict]:
        """Verifies keys. Returns keys that are not permitted"""
        rejected = {}
        for key in list(to_check):
            if key not in allowed:
                rejected.update({key : to_check[key]}) #add removed content to new dict
                del to_check[key] #This change happens to the dict globally
        if len(rejected) == 0:
            return None
        return rejected

    @staticmethod
    def verifyDictParams(to_check : dict, allowed : dict) -> Union[None,dict]:
        """Verifies keys and the values they store. Returns keys and their contents that are not permitted"""
        rejected = {}
        bad_args = OptArg.verifyDictKeys(to_check, allowed)
        if bad_args != None:
            rejected.update(bad_args)

        #The following could be cleaner but this part of the code simply isn't important enough for me to care that much.
        for key in list(to_check):
            if to_check[key] in [[] , "", None]: #Extra safety, may not be needed. 
                del to_check[key] #This change happens to the dict globally
                continue #when a value for a parameter isn't passed then it probably has a default calue hardcoded somewhere.

            #allowed parameters are either lists or single values
            if isinstance(allowed[key],list):
                if ".." in allowed[key]: #hasskell style range of values
                    if not allowed[key][0] <= to_check[key] <= allowed[key][2]: #if not in range then it's bad
                        rejected.update({key : to_check[key]}) #add removed content to new dict
                        del to_check[key] #This change happens to the dict globally 

                elif to_check[key] not in allowed[key]: #if param not in list of explicitly allowed params then it's bad
                    rejected.update({key : to_check[key]}) #add removed content to new dict
                    del to_check[key] #This change happens to the dict globally
            else:
                if to_check[key] != allowed[key]: #if param doesn't match possible param then it's bad
                    rejected.update({key : to_check[key]}) #add removed content to new dict
                    del to_check[key] #This change happens to the dict globally

        if len(rejected) == 0:
            return None
        return rejected

    