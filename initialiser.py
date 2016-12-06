import os

class ConfigInitialiser:
    def config_finder(self, exceptions):
        accepted_files = []
        if os.path.isdir("Configs"):
            print('config directory found')
            for ini in os.listdir("./Configs"):
                if ini.endswith('.ini') and ini.strip('.ini') not in exceptions:
                    accepted_files.append(("Configs/"+ini))
        return accepted_files

    def reader(self, *exceptions):
        configs = []
        for ini in self.config_finder(exceptions):
            config = {x:y for x, y in [z.split(':') for z in open(ini).read().strip().split('\n')]}
            configs.append(config)
        return configs

if __name__ == "__main__":
    init = ConfigInitialiser()
    print(init.reader())
