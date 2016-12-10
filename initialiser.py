import os, re, configparser, asyncio, sys, random, copy

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
        self.text_config = configparser.ConfigParser()
        self.text_config.read('Config.ini')
        self.config = {}
        self.config['Main'] = {'command_char':self.text_config['Main']['command_char']}
        self.config['Main']['hub'] = [server.get_channel(self.text_config['Main']['hub_channel']) for server in client.servers if server.id == self.text_config['Main']['hub_server']][0]
        self.init_flag = False

    async def config_initialise(self):
        await asyncio.sleep(5)
        config = configparser.ConfigParser()
        config['Main'] = {}
        while True:
            char = input('What character will you be using as a command character?: ')
            ans = input('Are you sure you want to use "'+char+'" as your command character? (yes/y): ')
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
