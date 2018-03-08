
class FormattedCommand:
    """An object that contains the command script,
        and can do validation for that command"""
    def __init__(self, command, config, category_name):
        self.command = command
        self.set_config(config)
        self.category_name = category_name

        # create length comparisons
        self.lengths = {
                '<'  : (lambda x,y : x < y),
                '<=' : (lambda x,y : x <=y),
                '>'  : (lambda x,y : x > y),
                '>=' : (lambda x,y : x >=y),
                '='  : (lambda x,y : x ==y)
                }

        # create operand identities
        self.identities = {
                'i'  : (lambda x : x.isdigit()),
                '?'  : (lambda x : True),
                ''   : (lambda x : True)
                }

    def set_config(self, config):
        """Sets keys from a config as attributes of the class"""
        for key in config:
            setattr(self, key, config[key])

    def validate_input(self, input_string):
        """Checks an input string against the commands usage format,
            if correct, returns a parsed version of the input string
            otherwise returns None"""

        usage = self.command.usage
        parameter_track = {} # tracks what arguments each parameter is assigned

        if not usage: # command has no required usage
            return input_string, None

        argument_counter = 0 # track amount of arguments passed for this parameter
        parameter_counter = 0
        parameter = usage[parameter_counter]
        parameter_track[parameter['name']] = []

        length_check = False # arguments ending prematurely will cause a fail
        for argument in input_string:
            parameter_track[parameter['name']].append(argument)
            argument_counter += 1

            length_check = self.lengths[parameter['length'][0]](argument_counter, parameter['length'][1])

            for operand in parameter['operands']:
                if not self.identities[operand](argument):
                    msg = '`{}` hasn\'t been met, please make sure to re-check usage'.format(parameter['name'])
                    return None, '\n'.join([self.command.usage_string, msg])

            if length_check and parameter_counter < len(usage)-1: # move onto next parameter if possible

                # if arg length is only 1, don't use a list
                if len(parameter_track[parameter['name']]) == 1:
                    parameter_track[parameter['name']] = parameter_track[parameter['name']][0]

                argument_counter = 0
                parameter_counter += 1
                parameter = usage[parameter_counter]
                parameter_track[parameter['name']] = []

        length_check = self.lengths[parameter['length'][0]](argument_counter, parameter['length'][1]) # final check

        if not length_check:
            msg = 'Please use the correct amount of arguments for this command'
            return None, '\n'.join([self.command.usage_string, msg])

        parameter_track = {x:(y[0] if len(y) == 1 else y) for x, y in parameter_track.items()}
        return parameter_track, None


    def validate_length(self, size):
        """Check that the amount of parameters are either more than the
            minimum or between the minimum and maximum"""
        if self.command.arglen == -1:
            return True

        if type(self.command.arglen) is tuple:
            return self.command.arglen[0] <= size <= self.command.arglen[1]

        return size >= self.command.arglen

    def get_description(self):
        """returns a description of the command"""
        return self.command.description

    def get_usage(self):
        """returns the raw string for the usage of the command"""
        return self.command.usage_string

    def get_aliases(self):
        """returns the aliases of the command"""
        return self.command.aliases

    def __call__(self, *args, **kwargs):
        """calling the FormattedCommand object will instead
            call the command associated with it"""
        self.command(*args, **kwargs)
