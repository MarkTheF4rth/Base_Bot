import os, re, configparser, asyncio, sys, random, copy, discord
from addeventlisteners import addListeners
from collections import OrderedDict
from bot import Main
from StorageClasses import commandConfig

COMMAND_DICT = {}
TASK_DICT = {}
INIT_DICT = {}
TRUE_CASE = ['True', 'true', '1', 'yes']
FALSE_CASE = ['False', 'false', '0', 'no']

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

        self.default_permition_format(client)

    def ini_format(self, ini, client):
        print('Applying config formats to channels in {}'.format(client.get_server(ini['Main']['server id'])))
        channels = {}
        default_scope = ini['Main']['default channel scope'].strip()
        if default_scope != 'none':
            channels = {channel.id:default_scope for channel in client.get_server(ini['Main']['server id']).channels if channel.type != discord.ChannelType.voice}
        channels.update(ini['Channel Config'])

        for channel, scope in channels.items():
            print('---{}'.format(client.get_channel(channel)))
            if scope in ['master', 'global']:
                self.permition_format(channel, self.raw_config['Default Commands'], roles=ini['Roles'])

            if scope in ['global', 'local']:
                self.permition_format(channel, ini['Default Commands'], roles=ini['Roles'])

            if channel in ini:
                self.permition_format(channel, ini[channel.id], roles=ini['Roles'])

    def default_permition_format(self, client):
        for server_id in self.raw_config['Server Specific']['servers'].split(','):
            server_id = server_id.strip()
            server = client.get_server(server_id)

            if not server:
                print('server: \''+server_id+'\' not found... omitting')
                continue

            print('Applying default permitions to all valid channels in {}, ({})'.format(server_id, server.name))
            for channel in server.channels:
                if channel.type != discord.ChannelType.voice and channel.id not in self.command_config.command_tree:
                    print('---{}'.format(channel.name))
                    self.permition_format(channel.id, self.raw_config['Default Commands'])

    def permition_format(self, channel, ini, roles=[]):
        command_dict = {}
        unique_command_list = {}

        for command_name, command_config in ini.items():
            if command_name not in COMMAND_DICT:
                print('Command: '+command+' not defined... omitting')
                continue

            current_command = COMMAND_DICT[command_name]
            command_config = command_config.split('\n')

            for string in command_config:
                split_text = re.match(r'(\w+): ([^:]+)', string)
                if split_text:

                    identifier, values = split_text.groups()
                    
                    if identifier == 'ROLE':
                        for value in values.split(','):
                            value = value.strip()
                            if value in roles: 
                                for role in roles[value].split(','):
                                    current_command.add_role(role.strip(), channel)
                            else:
                                current_command.add_role(value, channel)

                    elif identifier == 'FLAGS':
                        current_command.set_flags(values)

                            
            for alias in current_command.aliases: 
                command_dict.update({alias:current_command})
            unique_command_list.update({command_name:current_command})

        if channel in self.command_config.unique_command_tree:
            self.command_config.command_tree[channel].update(command_dict)
            self.command_config.unique_command_tree[channel].update(unique_command_list)
        else:
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

    for name, func in INIT_DICT.items():
        func(main)
        
    thread_loop.create_task(main_loop(main, thread_loop))

def add_command(command):
    COMMAND_DICT.update(command)

def add_task(task):
    TASK_DICT.update(task)

def add_init(func):
    INIT_DICT.update(func)
