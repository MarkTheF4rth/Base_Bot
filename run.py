import discord, asyncio, sys, os, shelve, random, types, importlib

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.getcwd()+'/BaseStruct')
sys.path.insert(0, os.getcwd()+'/BaseStruct/Decorators')

from message_sender import send_message
from initialiser import Master_Initialise

async def main_loop(main, thread_loop):
    for task_name, task in main.tasks.items():
        if task.instant_run:
            thread_loop.create_task(task.run(main))

    while not CLIENT.is_closed:
        main.command_handler()
        for message in main.out_messages:
            await send_message(CLIENT, *message)
            main.out_messages.pop(0)
        await asyncio.sleep(1)

def verify_bot():
    verified = True
    if not os.path.isfile('token.txt'):
        print('There is no token file present, make sure your token file is named "token.txt"')
        verified = False

    if not os.path.isfile('Configs/MASTER-Config.ini'):
        print('Master config file not present')
        verified = False

    return verified

if __name__ == '__main__':
    if not verify_bot(): # Verify that bot requirements are met, forcefully exit if not
        print('One or more requirements not met, exiting')
        sys.exit()

    CLIENT = discord.Client() # Creating client
    LOOP = asyncio.get_event_loop() # Create event loop for asyncio threads
    INPUT = sys.argv[1:] # Save command line input that does not include the filename

    from CommandModules import * # Import modules

    token = open('token.txt').readlines()[0].strip() # Grab token from file


    LOOP.create_task(Master_Initialise(CLIENT, main_loop, LOOP)) # Run the initialiser

    CLIENT.run(token) # Run the bot with given token
    CLIENT.connect() # Connect to discord
