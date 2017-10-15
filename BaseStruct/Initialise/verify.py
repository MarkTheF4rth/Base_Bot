import os, sys, shutil

class Verify:
    '''Verifies that the bot is in working order'''
    def __init__(self):
        self.base_path = os.getcwd()

    def stage_one(self):
        print('Beginning stage one verification:')
        system = self.configs_verify()
        return all([system])
        

    def configs_verify(self):
        """Checks if file structure is correct, make corrections if needed"""
        print('----Verifying that file structure is correct')

        files = os.listdir(self.base_path+'/Configs')

        if not [file_name for file_name in files if file_name.endswith('.json')]: # no configs present
            print('--------CRITICAL FAILURE : No config files present')
            return False

        return True
        
