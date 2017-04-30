import os, re, configparser, asyncio, sys, random, copy, discord
from addeventlisteners import addListeners
from collections import OrderedDict
from bot import Main
from StorageClasses import commandConfig

EXTENSION_DICT = {'task':{}, 'command':{}, 'func':{}}
TRUE_CASE = ['True', 'true', '1', 'yes']
FALSE_CASE = ['False', 'false', '0', 'no']

class Config_Creator:
    def __init__(self, client, extension_dict):
        self.commands, self.command_ref = self.set_commands(extension_dict['command'])
        self.raw_config = configparser.ConfigParser(dict_type=OrderedDict) #Raw Master Config
        self.raw_config.read('Configs/MASTER-Config.ini')
        self.command_config = commandConfig.Command_Config() #Config for all commands

        for config_file in os.listdir('Configs'):
            if config_file.endswith('.ini') and 'MASTER' not in config_file:
                server_config = configparser.ConfigParser(dict_type=OrderedDict)
                server_config.read(('Configs/'+config_file))
                self.ini_format(server_config, client)

        self.default_permition_format(client)

    def set_commands(self, command_dict):
        new_command_dict = OrderedDict()
        command_ref = {}
        for command, function in command_dict.items():
            new_command_dict.update({command:command})
            for alias in function.aliases:
                command_ref.update({alias:command})

        return command_dict, command_ref 

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
                self.permition_format(channel, ini[channel], roles=ini['Roles'])

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
        for command_name, command_config in ini.items():
            if command_name not in self.command_ref:
                print('Command: '+command_name+' not defined... omitting')
                continue

            current_command = self.commands[self.command_ref[command_name]]
            command_config = command_config.split('\n')

            for string in command_config:
                split_text = string.split(':', 1)

                if split_text:
                    identifier, values = split_text
                    identifier = identifier.strip()
                    
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

            self.commands[self.command_ref[command_name]] = current_command

    def get_attributes(self):
        return (self.raw_config, self.commands, self.command_ref,
                self.raw_config['Main']['command char'])

async def Master_Initialise(client, main_loop, thread_loop):
    '''Runs all initialisation scripts in the correct order, 
         running the main thread loop when it finishes'''
    print('='*10+'BEGINNING INIT'+'='*10)
    main = Main(client)

    print('Adding Listeners')
    addListeners(client, main)
    print('\n')

    while not main.connected:
        print('Connecting....')
        await asyncio.sleep(1)
    print('\n')

    main.resolve_external(EXTENSION_DICT, thread_loop)

    config = Config_Creator(client, EXTENSION_DICT)
    main.set_config(config.get_attributes())
    print('\n')

    print('='*10+'INIT COMPLETED'+'='*10+'\n')
    print('\n')

    print('Logged in as')  
    print(client.user.name)  
    print(client.user.id)  
    print('-----\n')

    await thread_loop.create_task(main_loop(main, thread_loop))

def extend_bot(func, f_type):
    EXTENSION_DICT[f_type].update(func)
