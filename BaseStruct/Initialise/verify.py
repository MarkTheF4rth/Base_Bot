import os, sys, shutil

class Verify:
    '''Verifies that the bot is in working order'''
    def __init__(self):
        self.base_path = os.getcwd()

    def stage_one(self):
        print('Beginning stage one verification:')
        system = self.filesystem_verify()
        if all([system]):
            print('Stage one verification passed')
        else:
            print('One or more critical failures arose, exiting...')
            sys.exit()
        

    def filesystem_verify(self):
        '''Checks if file structure is correct, make corrections if needed'''
        print('----Verifying that file structure is correct')
        create_dir = lambda x: os.makedirs(x) if not os.path.isdir(x) else True
        commands = create_dir(self.base_path+'CommandModules')
        configs  = create_dir(self.base_path+'Configs')
        data     = create_dir(self.base_path+'Data')
    
        if not os.path.exists(self.base_path+'/Configs/MASTER-Config.ini'):
            print('--------CRITICAL FAILURE : Master config file not found, creating template...')
            shutil.copy(self.base_path+'/BaseStruct/ConfigTemplates/MASTER-Config.ini', self.base_path+'/Configs/MASTER-Config.ini')
            return False

        return True
        
