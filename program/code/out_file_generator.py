import os
import pickle

class Output:

    @staticmethod
    def createOutputDir(sim_args : dict, name : str) -> str:
        """
        Create a new directory containing sim parameters. 
        Later actual output data can be stored here. returns directory name to be used later
        """

        current_directory = os.getcwd()
        
        out_dir = os.path.join(current_directory, 'output', name)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        else:
            print("args file inside {} overwritten!".format(out_dir))

        args_f = open(out_dir + '/args.obj', 'wb')
        pickle.dump(sim_args,args_f)
        args_f.close()


        

        

