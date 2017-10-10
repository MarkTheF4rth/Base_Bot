import inspect
from Initialise.initialise import extend_bot

def task(run_time='call'):
    class task:
        """A task instance can be added to a queue and 
            be called asynchronously in any lib"""
        def __init__(self, function):
            extend_bot({function.__name__:self}, 'task')
            self.run_time = run_time
            self.run = function
            self.valid = inspect.iscoroutinefunction(function)

        async def __call__(self, main, *args, **kwargs):
            await self.run(main, *args, **kwargs)

    return task
