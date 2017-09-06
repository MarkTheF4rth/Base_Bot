from Initialise.initialise import add_command

def command(aliases=[], description=None, category='Default', arglen=-1):
    class command_struct(object):
        '''Stores information about a specific command'''
        def __init__(self, function):
            add_command({function.__name__:self}, category)
            self.name = function.__name__
            self.aliases = [function.__name__] + aliases
            self.description_ref = {'description':description}
            self.category = category
            self.arglen = arglen
            self.roles = []
    
            self.run = function

        def __call__(self, *args, **kwargs):
            self.run(*args, **kwargs)

    return command_struct
