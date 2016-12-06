import discord, asyncio, sys, os, shelve, time, random, tasks, types
from commands import Main
client = discord.Client()

LOOP = asyncio.get_event_loop()
INPUT = sys.argv[1:]
max_msg_size = 1500

class Store:
    def __init__(self):
        self.init_flag = False
        self.messages = []

@client.event
async def on_message(message):
    if STORE.init_flag:
        STORE.messages.append(message)
    elif message.content.lstrip().startswith(MAIN.config['command_char']): #removes leading spaces and checks that the message begins with the command character
        MAIN.message_parser(message)
    
@client.event
async def on_message_edit(old, message):
    if STORE.init_flag:
        STORE.messages.append(message)
    elif message.content.lstrip().startswith(MAIN.config['command_char']):
        MAIN.message_parser(message, True)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

async def send_message(channel_str, message_str):
    if not message_str:
        return
    if len(message_str) > max_msg_size:
        stripped = message_str.strip()
        boxed = stripped.startswith('```') and stripped.endswith('```')
        split_pos = message_str.rfind('\n',0,max_msg_size)
        if split_pos < 0:
            split_pos = max_msg_size
        message_head = message_str[:split_pos]
        message_tail = message_str[split_pos:]
        if boxed:
            message_head += '```'
            message_tail = '```' + message_tail
        await really_send_message(channel_str, message_head)
        await send_message(channel_str, message_tail)
    else:
        await really_send_message(channel_str, message_str)

async def really_send_message(channel_str, message_str):
    return await client.send_message(channel_str, message_str)

async def main_loop(main, loop):
    await asyncio.sleep(1)
    await client.send_message(main.config['hub'], 'I have restarted')
    [loop.create_task(getattr(tasks, a)(main)) for a in dir(tasks) if isinstance(getattr(tasks, a), types.FunctionType)]
    while not client.is_closed:
        main.message_handler()
        for message in main.out_messages:
            await send_message(message[0], message[1])
            main.out_messages.pop(0)
        await asyncio.sleep(1)

async def initialise():
    await asyncio.sleep(5)
    config = open('Configs/config-MASTER', 'w')
    while True:
        char = input('What character will you be using as a command character?: ')
        ans = input('Are you sure you want to use "'+char+'" as your command character? (yes/y): ')
        if ans.lower() == 'yes' or ans.lower() == 'y':
            config.write('command_char = '+char)
            break

    num = random.randint(1,1000000000)
    print('Please type',num,'into the channel that will be your hub channel (note that you must authorise your bot in the server first)')
    found = False
    while not found:
        await asyncio.sleep(1)
        for message in STORE.messages:
            if message.content == str(num):
                config['hub'] = message.channel
                ans = input('hub channel set to '+message.channel.name+', please confirm your choice (yes/y): ')
                if ans.lower() == 'yes' or ans.lower() == 'y':
                    found = True
            STORE.messages.pop(0)

    print('init process completed, please go about your day')
    config.close()
    MAIN.__init__(shelve)
    LOOP.create_task(main_loop(MAIN))

STORE = Store()
MAIN = Main(shelve)
if __name__ == '__main__':
    if not os.path.isfile('token.txt'):
        print('There is no token file present, make sure your file is named "token.txt"')
        sys.exit()

    token = open('token.txt').readlines()[0].strip()

    if not os.path.isfile('Configs/config-MASTER.bak'):
        print('Master config file not present, running initialiser')
        STORE.init_flag = True
        LOOP.create_task(initialise())
    elif len(INPUT) == 1 and (INPUT[0] == 'init' or INPUT[0] == 'initialise'):
        print('Running initialiser upon request')
        STORE.init_flag = True
        LOOP.create_task(initialise())
    else:
        LOOP.create_task(main_loop(MAIN, LOOP))

    LOOP.run_until_complete(client.run(token))
    LOOP.run_until_complete(client.connect())
