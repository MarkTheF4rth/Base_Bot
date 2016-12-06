import asyncio

async def spam(main):
    while True:
        main.message_printer('I *still* live', 'hub')
        await asyncio.sleep(60)

