import discord, asyncio, sys, os, shelve, random, types

sys.path.insert(0, '/home/ec2-user/BOTS/Base_Bot/BaseStruct')
from addeventlisteners import addListeners
from commands import Main
from message_sender import send_message

client = discord.Client()
MAIN = Main(shelve)
addListeners(client, MAIN)

LOOP = asyncio.get_event_loop()
INPUT = sys.argv[1:]


async def main_loop(main, loop):
    while main.init_flag or not client.is_logged_in:
        await asyncio.sleep(1)
    main.initialise(client)
#    if main.hub_channel:
#        await client.send_message(main.hub_channel, 'I have restarted')
    #[loop.create_task(getattr(tasks, a)(main)) for a in dir(tasks) if isinstance(getattr(tasks, a), types.FunctionType)]
    while not client.is_closed:
        main.command_handler()
        for message in main.out_messages:
            await send_message(client, *message)
            main.out_messages.pop(0)
        await asyncio.sleep(1)


if __name__ == '__main__':
    if not os.path.isfile('token.txt'):
        print('There is no token file present, make sure your file is named "token.txt"')
        sys.exit()

    token = open('token.txt').readlines()[0].strip()

    MAIN.init_flag = True
    if not os.path.isdir('Configs'):
        os.makedirs('Configs')
    if not os.path.isfile('Configs/MASTER-Config.ini'):
        print('Master config file not present, running initialiser')
        LOOP.create_task(MAIN.config_initialise())
    elif len(INPUT) == 1 and (INPUT[0] == 'init' or INPUT[0] == 'initialise'):
        print('Running initialiser upon request')
        LOOP.create_task(MAIN.config_initialise())
    else:
        MAIN.init_flag = False

    LOOP.create_task(main_loop(MAIN, LOOP))

    LOOP.run_until_complete(client.run(token))
    LOOP.run_until_complete(client.connect())
