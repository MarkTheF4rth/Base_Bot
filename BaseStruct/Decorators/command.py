from Initialise.initialise import add_command

def command(aliases=[], description=None, category='Default', usage=[('', '...')]):
    class command_struct(object):
        """Stores information about a specific command"""
        def __init__(self, function):
            add_command({function.__name__:self}, category)
            self.name = function.__name__
            self.aliases = [function.__name__] + aliases
            self.description = description
            self.category = category
            self.roles = []
            self.arglen, self.usage_string = self.usage_interpreter(usage)
    
            self.run = function

        def usage_interpreter(self, usage):
            """Intereprets given usage parameter into readable text"""

            required_flag = 0
            usage_list = []
            arglen = -1

            for item in usage: # build usage string through every command
                if item[1] == '?':
                    usage_list.append('<{} (optional)>'.format(item[0]))

                elif item[1] == '...':
                    if item[0]: # do not add empty strings to the end of usage messages
                        usage_list.append('<{} (multiple)>'.format(item[0]))
                    break # mult argument should always be the last one

                else:
                    required_flag += 1
                    usage_list.append('<{}>'.format(item[0]))

            usage_string = ','.join(usage_list)

            if usage[-1][1] == '...':
                if required_flag:
                    arglen = required_flag

            else:
                arglen = (required_flag, len(usage))

            return arglen, usage_string


        def __call__(self, *args, **kwargs):
            self.run(*args, **kwargs)

    return command_struct
