from initialiser import add_task

def task(instant_run=False):
    class task:
        def __init__(self, function):
            add_task({function.__name__:self})
            self.instant_run = instant_run
            self.run = function

        def __call__(self, main):
            self.run(main)

    return task
