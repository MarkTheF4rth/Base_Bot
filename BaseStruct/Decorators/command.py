from initialiser import add_command

def command(arglen=-1, aliases=[], description=None):
    class command_struct(object):
        '''Stores information about a specific command'''
        def __init__(self, function):
            add_command({function.__name__:self})
            self.aliases = [function.__name__] + aliases
            self.context = None
            self.description = description
            self.roles = {}
            self.flags = []
            self.arglen = arglen
    
            self.run = function

        def add_role(self, role, channel):
            if channel not in self.roles:
                self.roles[channel] = [role]
            else:
                self.roles[channel].append(role)

        def set_flags(self, string):
            self.flags = string.split()
            if 'ignore_alias' in self.flags:
                self.alias_of = False

        def valid_len(self, size):
            size = size-1
            if size == self.arglen or self.arglen == -1:
                return True
            if type(self.arglen) == list and size in self.arglen:
                return True
            return False

        def __call__(self, *args, **kwargs):
            self.run(*args, **kwargs)

    return command_struct
