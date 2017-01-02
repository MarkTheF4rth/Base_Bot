import discord, asyncio, sys, os, shelve, time, random, tasks, types
from commands import Main
client = discord.Client()

LOOP = asyncio.get_event_loop()
INPUT = sys.argv[1:]
max_msg_size = 1500

@client.event
async def on_message(message):
    MAIN.message_handler(message)
   
@client.event
async def on_message_edit(old, message):
    MAIN.message_handler(message)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

async def send_message(channel_str, message_str, header='', msg_break=''):
    if not message_str:
        return

    if len(message_str) > max_msg_size:
        stripped = message_str.strip()
        boxed = stripped.startswith('```') and stripped.endswith('```')
        split_pos = message_str.rfind('\n',0,max_msg_size)

        if split_pos < 0:
            split_pos = max_msg_size

        message_head = header+'\n'+message_str[:split_pos]
        message_tail = message_str[split_pos:]

        if boxed:
            message_head += '```'
            message_tail = '```' + message_tail

        await really_send_message(channel_str, message_head)
        await send_message(channel_str, msg_break+message_tail, header, msg_break)

    else:
        await really_send_message(channel_str, header+message_str)

async def really_send_message(channel_str, message_str):
    return await client.send_message(channel_str, message_str)

async def main_loop(main, loop):
    while main.init_flag or not client.is_logged_in:
        await asyncio.sleep(1)
    main.initialise(client)
    if main.hub_channel:
        await client.send_message(main.hub_channel, 'I have restarted')
    [loop.create_task(getattr(tasks, a)(main)) for a in dir(tasks) if isinstance(getattr(tasks, a), types.FunctionType)]
    while not client.is_closed:
        main.command_handler()
        for message in main.out_messages:
            await send_message(*message)
            main.out_messages.pop(0)
        await asyncio.sleep(1)

MAIN = Main(shelve)
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
