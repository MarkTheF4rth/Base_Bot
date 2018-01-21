import discord, asyncio, sys, os
import importlib.util

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.getcwd()+'/BaseStruct')

from Scripts.message_sender import send_message
from Initialise.initialise import Master_Initialise

async def main_loop(bot, thread_loop):
    while bot.connected:
        while bot.running:
            bot.command_handler()
            for message in bot.out_messages:
                await send_message(*message)
                bot.out_messages.pop(0)

            while bot.pending_tasks:
                task = bot.pending_tasks.pop(0)
                await task[0](bot, *task[1], **task[2])
            await asyncio.sleep(1)

        bot.set_configs()
        bot.running = True


if __name__ == '__main__':
    CLIENT = discord.Client() # Creating client
    LOOP = asyncio.get_event_loop() # Create event loop for asyncio threads
    INPUT = sys.argv[1:] # Save command line input that does not include the filename

    token = open('token.txt').readlines()[0].strip() # Grab token from file

    LOOP.create_task(Master_Initialise(CLIENT, main_loop, LOOP)) # Run the initialiser

    CLIENT.run(token) # Run the bot with given token
    CLIENT.connect() # Connect to discord
