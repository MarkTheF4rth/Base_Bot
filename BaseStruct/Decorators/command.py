from Initialise.initialise import extend_bot

def command(aliases=[], description=None, category='General', arglen=-1):
    class command_struct(object):
        '''Stores information about a specific command'''
        def __init__(self, function):
            extend_bot({function.__name__:self}, 'command')
            self.name = function.__name__
            self.aliases = [function.__name__] + aliases
            self.context = None
            self.command_structure = {}
            self.description_ref = {'description':description, 'category':category}
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
            '''Check that the amount of parameters are either more than the minimum, 
            or between the minimum and maximum'''
            if self.arglen < 0:
                return True

            if type(self.arglen) is tuple:
                return self.arglen[0] <= size <= self.arglen[1]

            return size >= self.arglen

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

        def get_category(self, channel):
            if channel in self.description_ref:
                return self.description_ref[channel]['category']
            return self.description_ref['category']


        def __call__(self, *args, **kwargs):
            self.run(*args, **kwargs)

    return command_struct
