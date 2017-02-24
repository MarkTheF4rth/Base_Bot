import os, re, configparser, asyncio, sys, random, copy
from addeventlisteners import addListeners
from collections import OrderedDict
from bot import Main
from StorageClasses import commandConfig

COMMAND_DICT = {}
TASK_DICT = {}

class Config_Creator:
    def __init__(self, client):
        self.raw_config = configparser.ConfigParser(dict_type=OrderedDict) #Raw Master Config
        self.raw_config.read('Configs/MASTER-Config.ini')
        self.command_config = commandConfig.Command_Config() #Config for all commands

        for config_file in os.listdir('Configs'):
            if config_file.endswith('.ini') and 'MASTER' not in config_file:
                server_config = configparser.ConfigParser(dict_type=OrderedDict)
                server_config.read(('Configs/'+config_file))
                self.ini_format(server_config, client)


    def ini_format(self, ini, client):
        if ini['Main']['enabled channels'] == 'all':
            for channel in client.get_server(ini['Main']['server id']).channels:
                channel.id, self.permition_format(channel.id, ini['Default Commands'], ini)
        else:
            for channel in ini['Main']['enabled channels'].split(','):
                channel.strip(), self.permition_format(channel.strip(), ini[channel.strip()], ini)


    def permition_format(self, channel, channel_config, ini):
        command_dict = {}
        unique_command_list = {}
        tiers = []

        if 'Tiers' in ini:
            tiers = ini['Tiers']

        for command_name, command_config in channel_config.items():
            if command_name == 'clear defaults':
                continue

            if command_name not in COMMAND_DICT:
                print('Command: '+command+' not defined... omitting')
                continue

            current_command = COMMAND_DICT[command_name]
            command_config = command_config.split('\n')

            for string in command_config:
                split_text = re.match(r'(\w+): ([^:]+)', string)
                if split_text:

                    key, value = split_text.groups()
                    
                    if key == 'ROLE':
                        for option in value.split(','):
                            option = option.strip()
                            if option in tiers: 
                                for role in tiers[option].split(','):
                                    current_command.add_role(role.strip())
                            else:
                                current_command.add_role(option)


                    elif key == 'FLAGS':
                        current_command.set_flags(value)

                            
            for alias in current_command.aliases: 
                command_dict.update({alias:current_command})
            unique_command_list.update({command_name:current_command})

        self.command_config.command_tree.update({channel:command_dict})
        self.command_config.unique_command_tree.update({channel:unique_command_list})


async def Master_Initialise(client, main_loop, thread_loop):
    main = Main(client)
    addListeners(client, main) # Add listeners

    main.commands = COMMAND_DICT
    main.tasks = TASK_DICT

    while not main.connected:
        await asyncio.sleep(1)

    main.set_config(Config_Creator(client))
    thread_loop.create_task(main_loop(main, thread_loop))

def add_command(command):
    COMMAND_DICT.update(command)

def add_task(task):
    TASK_DICT.update(task)
