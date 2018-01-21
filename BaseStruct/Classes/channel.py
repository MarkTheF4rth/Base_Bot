
class Channel:
    """An object created to hold data on the given channel, 
        verifying how commands should behave on that channel"""
    def __init__(self, ID, commands):
        self.ID = ID
        self.commands = commands
        self.resolve_commands()

    def resolve_commands(self):
        """Moves commands from the categories dict into an 
            easily readable dict for later use"""
        self.command_ref = {}
        for command_name, command in self.commands.items():
            for alias in command.get_aliases():
                self.command_ref[alias] = (command,  command.roles)

    def get_command(self, command_name, roles):
        """Returns the command object given a command name"""
        if command_name in self.command_ref:
            command = self.command_ref[command_name][0]
            accepted_roles = self.validate_role(command_name, roles)
            return command, accepted_roles
        return None, None

    def validate_role(self, command_name, roles):
        """Returns the intersection of a given list of role objects 
            and a command name, assumes the command exists in the channel"""
        return [role for role in roles if role.name in self.command_ref[command_name][1]]
