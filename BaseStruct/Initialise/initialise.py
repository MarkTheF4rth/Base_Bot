import os, asyncio
from collections import OrderedDict
from Initialise.verify import Verify
from Initialise.add_event_listeners import add_event_listeners
from filesystem import Filesystem
from Bot.bot import Bot
import importlib.util

EXTENSION_DICT = {'task':{}, 'command':OrderedDict({'ALL_COMMANDS':{}}), 'func':{}}
TRUE_CASE = ['TRUE', 'True', 'true', '1', 'yes']
FALSE_CASE = ['FALSE', 'False', 'false', '0', 'no']

def extend_bot(func, f_type):
    """Adds a given function to a local dictionary"""
    EXTENSION_DICT[f_type].update(func)

def add_command(function, category):
    """Adds a command to a local dictionary"""
    if category in EXTENSION_DICT['command']:
        EXTENSION_DICT['command'][category].update(function)
    else:
        EXTENSION_DICT['command'][category] = function
    EXTENSION_DICT['command']['ALL_COMMANDS'].update(function)
    

async def Master_Initialise(client, main_loop, thread_loop):
    """Runs all initialisation scripts in the correct order, 
         running the main thread loop when it finishes"""
    print('='*10+'BEGINNING INIT'+'='*10)

    verify = Verify()
    filesystem = Filesystem()
#    if not verify.stage_one(): # first verification stage
#        print('One or more critical failures arose, exiting...')
#        return

    print('Stage one verification passed')

    print('\n')

    filesystem.import_libs() # imports libraries from the commandmodules directory

    bot = Bot(client, EXTENSION_DICT, filesystem)


    print('Adding ready listener:')
    add_event_listeners(client, bot, whitelist=['onready'])
    print('\n')

    while not bot.connected:
        print('Connecting....')
        await asyncio.sleep(1)
    print('\n')

    bot.resolve_external(EXTENSION_DICT, thread_loop)

    print('\n')

    print('Adding remaining listeners:')
    add_event_listeners(client, bot, blacklist=['onready'])
    print('='*10+'INIT COMPLETED'+'='*10+'\n')
    print('\n')

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----\n')

    await thread_loop.create_task(main_loop(bot, thread_loop))


