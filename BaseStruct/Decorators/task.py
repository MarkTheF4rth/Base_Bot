import inspect
from initialiser import extend_bot

def task(run_time='call'):
    class task:
        def __init__(self, function):
            extend_bot({function.__name__:self}, 'task')
            self.run_time = run_time
            self.run = function
            self.valid = inspect.iscoroutinefunction(function)

        async def __call__(self, main, *args, **kwargs):
            await self.run(main, *args, **kwargs)

    return task
