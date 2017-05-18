from initialiser import extend_bot

def command(arglen=-1, aliases=[], description=None):
    class command_struct(object):
        '''Stores information about a specific command'''
        def __init__(self, function):
            extend_bot({function.__name__:self}, 'command')
            self.name = function.__name__
            self.aliases = [function.__name__] + aliases
            self.context = None
            self.command_structure = {}
            self.description_ref = {'description':description}
            self.flags = []
            self.arglen = arglen
    
            self.run = function

        def add_role(self, role, channel):
            '''Adds a role exception to the command 
                structure in the given channel'''
            if channel not in self.command_structure:
                self.command_structure[channel] = [role]
            else:
                self.command_structure[channel].append(role)

        def set_flags(self, string):
            '''Sets flags for commands'''
            self.flags = string.split()

        def validate_length(self, size):
            if size == self.arglen or self.arglen == -1:
                return True
            if type(self.arglen) == list and size in self.arglen:
                return True
            return False

        def validate_role(self, channel, roles):
            valid = []
            if channel in self.command_structure:
                for role in roles:
                    if role.name in self.command_structure[channel]:
                        valid.append(role)

            return valid


        def get_description(self, channel, roles):
            if channel in self.description_ref:
                for role in self.description_ref[channel]:
                    if role in roles:
                        return self.description_ref[channel][role]
                return self.description_ref[channel]['description']
            return self.description_ref['description']            

        def __call__(self, *args, **kwargs):
            self.run(*args, **kwargs)

    return command_struct
