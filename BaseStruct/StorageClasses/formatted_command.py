
class FormattedCommand:
    """An object that contains the command script, 
        and can do validation for that command"""
    def __init__(self, command, config, category_name):
        self.command = command
        self.set_config(config)
        self.category_name = category_name

    def set_config(self, config):
        """Sets keys from a config as attributes of the class"""
        for key in config:
            setattr(self, key, config[key])

    def validate_length(self, size):
        """Check that the amount of parameters are either more than the 
            minimum or between the minimum and maximum"""
        if self.command.arglen < 0:
            return True

        if type(self.command.arglen) is tuple:
            return self.command.arglen[0] <= size <= self.arglen[1]

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
