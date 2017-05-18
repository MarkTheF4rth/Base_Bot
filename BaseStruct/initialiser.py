import os, re, configparser, asyncio, sys, random, copy, discord
from addeventlisteners import addListeners
from collections import OrderedDict
from bot import Main
from StorageClasses import commandConfig

EXTENSION_DICT = {'task':{}, 'command':OrderedDict(), 'func':{}}
TRUE_CASE = ['True', 'true', '1', 'yes']
FALSE_CASE = ['False', 'false', '0', 'no']

class Config_Creator:
    def __init__(self, client, extension_dict):
        self.permission_presets = {}
        self.raw_config = configparser.ConfigParser(dict_type=OrderedDict) #Raw Master Config
        self.raw_config.read('Configs/MASTER-Config.ini')

        self.commands, self.command_ref = self.set_commands(extension_dict['command'])
        self.command_config = commandConfig.Command_Config() #Config for all commands
        self.resolve_configs(client)

    def resolve_configs(self, client):
        for config_file in os.listdir('Configs'):
            if config_file.endswith('.ini') and 'MASTER' not in config_file:
                server_config = configparser.ConfigParser(dict_type=OrderedDict)
                server_config.read(('Configs/'+config_file))
                self.server_permition_format(server_config, client)

        self.master_permition_format(client)

    def set_commands(self, command_dict):
        self.permission_presets = self.find_presets(self.raw_config)

        new_command_dict = OrderedDict()
        command_ref = {}
        for command, function in command_dict.items():
            new_command_dict.update({command:command})
            for alias in function.aliases:
                command_ref.update({alias:command})

        return command_dict, command_ref 

    def find_presets(self, server_ini):
        print('Loading command presets:')
        return_ini = {}
        for heading, content in server_ini.items():
            if "command" in heading.lower():
                return_ini.update({heading:content})
                print('---{} loaded'.format(heading))

        return return_ini


    def master_permition_format(self, client):
        for server_id, configs in self.raw_config['Server Config'].items():
            server_id = server_id.strip()
            server = client.get_server(server_id)
            ini = {}

            for config in configs.split(','):
                print(config, [key for key in self.permission_presets.keys()])
                if config in self.permission_presets:
                    ini.update(self.permission_presets[config])

            print('\n')

            if not server:
                print('server: \''+server_id+'\' not found... omitting')
                continue

            print('Applying command permitions to all valid channels in {}, ({})'.format(server_id, server.name))
            for channel in server.channels:
                if channel.type != discord.ChannelType.voice and channel.id not in self.command_config.command_tree and ini:
                    
                    print('---{}'.format(channel.name))
                    self.permition_format(channel.id, ini) 


    def server_permition_format(self, ini, client):
        print('Applying config formats to channels in {}'.format(client.get_server(ini['Main']['server id'])))
        server_presets = self.find_presets(ini)
        for channel, presets in ini['Channel Config'].items():
            if not channel.isdigit():
                print('---WARNING Invalid channel {} (not an integer) omitting...'.format(channel))
                continue

            if not client.get_channel(channel):
                print('---WARNING Invalid channel {} (not found) omitting...'.format(channel))
                continue

            permission_ini = {}
            loaded = []
            omitted = []

            for preset in presets.split(','):
                if preset in server_presets:
                    permission_ini.update(server_presets[preset]) 
                    loaded.append(preset)

                elif preset in self.permission_presets:
                    permission_ini.update(self.permission_presets[preset])
                    loaded.append(preset)  

                else:
                    omitted.append(preset)


            if permission_ini:
                self.permition_format(channel, permission_ini, roles=ini['Roles'])


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

    await thread_loop.create_task(main_loop(main, thread_loop, config))

def extend_bot(func, f_type):
    EXTENSION_DICT[f_type].update(func)
