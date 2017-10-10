from Initialise.initialise import extend_bot

def func():
    """creates a callable function as part of the bot"""
    class func:
        def __init__(self, function):
            setattr(self, function.__name__, function)
            self.name = function.__name__
            self.run = function
            extend_bot({self.name:self}, 'func')

        def __call__(self, *args, **kwargs):
            return self.run(self.main, *args, **kwargs)


    return func
