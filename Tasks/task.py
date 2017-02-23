import asyncio
import time
from commands import task

@task
async def task(self):
    print('running')
    while True:
        print(self.all_in_messages)
        await asyncio.sleep(1)
