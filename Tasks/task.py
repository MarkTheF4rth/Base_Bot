import asyncio

async def task(main):
    while True:
        main.message_printer('I am still here', main.hub_channel)
        asyncio.sleep(1)
