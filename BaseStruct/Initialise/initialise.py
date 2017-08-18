import os, asyncio
from collections import OrderedDict
from Initialise.verify import Verify
from Initialise.add_event_listeners import add_event_listeners
from Bot.bot import Bot
import importlib.util

EXTENSION_DICT = {'task':{}, 'command':OrderedDict(), 'func':{}}
TRUE_CASE = ['TRUE', 'True', 'true', '1', 'yes']
FALSE_CASE = ['FALSE', 'False', 'false', '0', 'no']

def extend_bot(func, f_type):
    '''Adds a given function to a local dictionary'''
    EXTENSION_DICT[f_type].update(func)


def import_libs():
    '''Procedurally import visible python scripts in the command modules'''
    homedir = os.getcwd()
    startdir = homedir+'/CommandModules'
    for root, dirs, files in os.walk(startdir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('_')]
        for script in files:
            if not script.startswith('.') and not script.startswith('_'):
                os.chdir(root)

                spec = importlib.util.spec_from_file_location(script.rstrip('.py'), os.path.join(root, script))
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)

                os.chdir(homedir)


async def Master_Initialise(client, main_loop, thread_loop):
    '''Runs all initialisation scripts in the correct order, 
         running the main thread loop when it finishes'''
    print('='*10+'BEGINNING INIT'+'='*10)

    verify = Verify()
    verify.stage_one() # first verification stage

    print('\n')

    import_libs() # imports libraries from the commandmodules directory

    bot = Bot(client, EXTENSION_DICT)


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


