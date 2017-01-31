import os, re, configparser, asyncio, sys, random, copy
from collections import OrderedDict

class Command_List:
    def __init__(self):
        self.command_names = []
        self.commands = []
        self.command_pairs = []

    def add_command(self, command_name, command):
        setattr(self, command_name, command)
        command = getattr(self, command_name)
        self.command_names.append(command_name)
        self.commands.append(command)
        self.command_pairs.append((command_name, command))
        
    def __iter__(self):
        return (x for x in self.command_names)

    def next(self):
        try:
            yield
        except:
            raise StopIteration

    def __getitem__(self, key):
        return getattr(self, key)


class Command:
    def __init__(self, alias_of=False, context=None):
        self.alias_of = alias_of
        self.context = context
        self.aliases = []
        self.roles = []
        self.flags = []

    def add_role(self, role, help_message):
        setattr(self, role, help_message)
        self.roles.append(role)
    
    def set_flags(self, string):
        self.flags = string.split()
        if 'ignore_alias' in self.flags:
            self.alias_of = False

class ConfigInitialiser:
    def config_finder(self, exceptions):
        accepted_files = []
        if os.path.isdir("Configs"):
            print('config directory found')
            for ini in os.listdir("./Configs"):
                if ini.endswith('.ini') and ini.strip('.ini') not in exceptions:
                    accepted_files.append(("Configs/"+ini))
        return accepted_files

    def initialise(self, client):
        self.config = configparser.ConfigParser(dict_type=OrderedDict)
        self.channels = {}
        self.config.read('Configs/MASTER-Config.ini')
        self.hub_channel = client.get_server(self.config['Main']['hub channel'])
        self.init_flag = False
        for config in os.listdir('Configs'):
            if config.endswith('.ini') and 'MASTER' not in config:
                server_config = configparser.ConfigParser(dict_type=OrderedDict)
                server_config.read(('Configs/'+config))
                new_server_config = self.ini_format(server_config, client)
                self.channels.update(new_server_config)

    def ini_format(self, ini, client):
        return_dict = {}
        if ini['Main']['enabled channels'] == 'all':
            perm_format = self.permition_format(ini['Default Commands'], ini)
            for channel in client.get_server(ini['Main']['server id']).channels:
                return_dict.update({channel.id:perm_format})
        else:
            for channel in ini['Main']['enabled channels'].split(','):
                return_dict.update({channel.strip():self.permition_format(ini[channel.strip()], ini)})
        return return_dict

    def permition_format(self, channel, ini):
        tiers = []
        if 'Tiers' in ini:
            tiers = ini['Tiers']

        command_list = Command_List()
        for command, command_config in channel.items():
            if command == 'clear defaults':
                continue
            current_command = Command()
            command_config = command_config.split('\n')

            for string in command_config:
                if string.strip():

                    split_text = re.split(r'[^\\]\|',string)
                    current_command.set_flags(split_text[2])
                    descriptor = split_text[0].strip()

                    if descriptor.strip() == 'ALIAS':
                        alias = Command(command)
                        alias.roles = current_command.roles
                        alias.set_flags(split_string[3])
                        command_list.add_command(split_text[1].strip(), alias)
                        current_command.aliases.append(split_text[1].strip())

                    else:
                        for option in split_text[1].split(','):
                            option = option.strip()
                            if option in tiers: 
                                for role in tiers[option].split(','):
                                    current_command.add_role(role.strip(), split_text[3])
                            else:
                                current_command.add_role(option, split_text[3])
                            
            command_list.add_command(command, current_command)

        return command_list

    async def config_initialise(self):
        await asyncio.sleep(5)
        config = configparser.ConfigParser()
        config['Main'] = {}
        while True:
            char = input('What character will you be using as a command character/phrase?: ')
            ans = input('Are you sure you want to use "'+char+'" as your command character/phrase? (yes/y): ')
            if ans.lower() == 'yes' or ans.lower() == 'y':
                config['Main'].update({'command char':char})
                break
    
        num = random.randint(1,1000000000)
        print('Please type',num,'into the channel that will be your hub channel (note that you must authorise your bot in the server first)')
        found = False
        while not found:
            await asyncio.sleep(1)
            for message in self.in_messages:
                if message.content == str(num):
                    config['Main'].update({'hub server':str(message.server.id)})
                    config['Main'].update({'hub channel':str(message.channel.id)})
                    ans = input('hub channel set to '+message.channel.name+', please confirm your choice (yes/y): ')
                    if ans.lower() == 'yes' or ans.lower() == 'y':
                        found = True
                self.in_messages.pop(0)
    
        print('init process completed')
        self.init_flag = False
        with open('Configs/MASTER-Config.ini', 'w') as configfile:
            config.write(configfile)

if __name__ == "__main__":
    init = ConfigInitialiser()
    init.reader()