import os, re, configparser, asyncio, sys, random, copy

class Command:
    def __init__(self, alias_of=False):
        self.alias_of = alias_of
        self.help_message = None
        self.roles = []

    def add_role(self, role, help_message):
        setattr(self, role, help_message)
        self.roles.append(role)
    
    def __iter__(self):
        return self.roles

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
        self.config = configparser.ConfigParser()
        self.channels = {}
        self.config.read('Configs/MASTER-Config.ini')
        self.hub_channel = [server.get_channel(self.config['Main']['hub_channel']) for server in client.servers if server.id == self.config['Main']['hub_server']][0]
        self.init_flag = False
        for config in os.listdir('Configs'):
            if config.endswith('.ini') and 'MASTER' not in config:
                server_config = configparser.ConfigParser()
                server_config.read(('Configs/'+config))
                new_server_config = self.ini_format(server_config, client)
                self.channels.update(new_server_config)

    def ini_format(self, ini, client):
        return_dict = {}
        if ini['Main']['enabled channels'] == 'all':
            perm_format = self.permition_format(ini['Permitions'], ini['Tiers'], ini['Aliases'])
            for channel in client.get_server(ini['Main']['server id']).channels:
                return_dict.update({channel.id:perm_format})
        else:
            for channel in ini['Main']['enabled channels'].split(','):
                return_dict.update({channel.strip():self.permition_format(ini[channel.strip()], ini['Tiers'], ini['Aliases'])})
        return return_dict


    def permition_format(self, channel, tiers, aliases):
        return_dict = {}
        for command, command_config in channel.items():
            return_dict[command] = Command()

            command_config = command_config.split('\n')
            help_message = command_config[0].strip()
            if help_message:
                return_dict[command].help_message = help_message
                return_dict[command].roles.append('@everyone')

            if len(command_config) > 1:
                for string in command_config[1:]:
                    option, value = string.split(':')
                    option = option.strip()
                    if option != 'alias':
                        if option in tiers: 
                            for role in tiers[option].split(','):
                                return_dict[command].add_role(role.strip(), value)
                        else:
                            return_dict[command].add_role(option, value)
                    else:
                        alias = Command(command)
                        alias.roles = return_dict[command].roles
                        return_dict[value.strip()] = alias

        return return_dict


    async def config_initialise(self):
        await asyncio.sleep(5)
        config = configparser.ConfigParser()
        config['Main'] = {}
        while True:
            char = input('What character will you be using as a command character/phrase?: ')
            ans = input('Are you sure you want to use "'+char+'" as your command character/phrase? (yes/y): ')
            if ans.lower() == 'yes' or ans.lower() == 'y':
                config['Main'].update({'command_char':char})
                break
    
        num = random.randint(1,1000000000)
        print('Please type',num,'into the channel that will be your hub channel (note that you must authorise your bot in the server first)')
        found = False
        while not found:
            await asyncio.sleep(1)
            for message in self.in_messages:
                if message.content == str(num):
                    config['Main'].update({'hub_server':str(message.server.id)})
                    config['Main'].update({'hub_channel':str(message.channel.id)})
                    ans = input('hub channel set to '+message.channel.name+', please confirm your choice (yes/y): ')
                    if ans.lower() == 'yes' or ans.lower() == 'y':
                        found = True
                self.in_messages.pop(0)
    
        print('init process completed')
        self.init_flag = False
        with open('Config.ini', 'w') as configfile:
            config.write(configfile)

if __name__ == "__main__":
    init = ConfigInitialiser()
    init.reader()
