from initialiser import add_init

def init():
    class initialiser(object):
        def __init__(self, function):
            add_init({function.__name__:self})
            self.run = function

        def __call__(self, *args, **kwargs):
            self.run(*args, **kwargs)

    return initialiser
