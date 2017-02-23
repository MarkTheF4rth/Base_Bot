class Command_Config:
    '''Stores 3 lists regarding commands, when iterated over, uses the command_names list'''
    def __init__(self):
        self.commands = {} # Dict of command/alias name to command
        self.command_tree = {} # Relational database of commands
        self.unique_command_tree = {} # Relational database of commands excluding aliases

    def __getattr__(self, index):
        return self.command_tree[index]

    def __iter__(self):
        return (x for x in self.command_tree.keys())

    def __next__(self):
        try:
            yield
        except:
            raise StopIteration

    def __getitem__(self, key):
        return getattr(self, key)

