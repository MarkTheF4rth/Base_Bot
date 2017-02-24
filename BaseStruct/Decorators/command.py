from initialiser import add_command

def command(aliases=[], description=None):
    class command_struct(object):
        '''Stores information about a specific command'''
        def __init__(self, function):
            add_command({function.__name__:self})
            self.aliases = [function.__name__] + aliases
            self.context = None
            self.description = description
            self.roles = []
            self.flags = []
    
            self.run = function

        def add_role(self, role):
            setattr(self, role, self.description)
            self.roles.append(role)

        def set_flags(self, string):
            self.flags = string.split()
            if 'ignore_alias' in self.flags:
                self.alias_of = False

        def __call__(self, *args, **kwargs):
            self.run(*args, **kwargs)

    return command_struct
