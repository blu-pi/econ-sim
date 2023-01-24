from typing import Union

#static
class OptArgDict:
    """
    Class for handling optional argument dictionaries. Currently only includes a validity check.
    """

    @staticmethod
    def verifyDict(to_check : dict, allowed : Union[list, dict]) -> Union[None, dict]:
        rejected = {}
        for key in to_check:
            if key not in allowed:
                rejected.update({key : to_check[key]}) #add removed content to new dict
                del to_check[key] #This change happens to the dict globally
        if len(rejected) == 0:
            return None
        else:
            return rejected
