import os, re

class ConfigInitialiser:
    def config_finder(self, exceptions):
        accepted_files = []
        if os.path.isdir("Configs"):
            print('config directory found')
            for ini in os.listdir("./Configs"):
                if ini.endswith('.ini') and ini.strip('.ini') not in exceptions:
                    accepted_files.append(("Configs/"+ini))
        return accepted_files

    def equal_splicer(self, text):
        return_dict = {}
        current_key = None
        cumilative_list = []
        for line in text:
            split = line.split('=')
            if len(split)>1:
                if current_key:
                    return_dict[current_key] = (' '.join(cumilative_list)).strip()
                current_key = split[0]
                cumilative_list = [split[1]]
            else:
                cumilative_list.append(line)
        return_dict[current_key] = (' '.join(cumilative_list)).strip()
        return return_dict
        

    def server_config_reader(self, ini):
        #try:
           # server = int(ini.readline().split('=')[1])
        ini_list = []
        line = (open(ini).read().split('\n'))
        print(self.equal_splicer(line))
        for line in zip(ini_list, ini_list[1:]):
           print('value_set',x, y, '\n')
        #except:
        #    print('Incorrectly formatted ini, omitting... please check template')

    def main_reader(self, ini):
        config = {x:y for x, y in [z.split(':') for z in open(ini).read().strip().split('\n') if z.contains(':')]}
        return config

    def reader(self, *exceptions):
        self.configs = {}
        for ini in self.config_finder(exceptions):
            print('Reading ini file: '+ini)
            if ini.startswith('MAIN'):
                self.main_config = self.main_reader(ini)
            else:
                self.server_config_reader(ini)

if __name__ == "__main__":
    init = ConfigInitialiser()
    init.reader()
