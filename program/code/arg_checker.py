from typing import Union

#static
class OptArgDict:
    """
    Class for handling optional argument dictionaries. Currently only includes validity checks.
    """

    @staticmethod
    def verifyDictKeys(to_check : dict, allowed : Union[list, dict]) -> Union[None, dict]:
        """Verifies keys. Returns keys that are not permitted"""
        rejected = {}
        for key in to_check:
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
        bad_args = OptArgDict.verifyDictKeys(to_check, allowed)
        if bad_args != None:
            rejected.update(bad_args)

        #The following could be cleaner but this part of the code simply isn't important enough for me to care that much.
        for key in to_check:
            #allowed parameters are either lists or single values
            if isinstance(allowed[key],list):
                if allowed[key].contains(".."): #hasskell style range of values
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
