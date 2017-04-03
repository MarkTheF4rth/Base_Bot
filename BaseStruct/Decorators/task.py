from initialiser import add_task

def task(run_time='call'):
    class task:
        def __init__(self, function):
            add_task({function.__name__:self})
            self.run_time = run_time
            self.run = function

        async def __call__(self, main):
            self.run(main)

    return task
