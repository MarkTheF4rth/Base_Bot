import json, os, importlib, copy, sys

class Filesystem:
    """Deals with reading, writing, and editting files not part of Base_Bot"""
    def __init__(self, default_config_path, home_dir):
        """intialises by importing all external configs and libraries"""
        self.home_dir = home_dir # location of run.py
        self.default_config_path = default_config_path # path to templates for default config values
        self.load_default_configs()
        self.load_external_configs()


    def import_libs(self, module_path, home):
        """Recursively and iteratively import visible python scripts in the command modules
        if intialise.py is found as a file, it will assume that file is contained within a module"""
        path_list = [] # paths of all imported scripts
        cutoff = None # determines path
        added = '' # last path added to syspath

        for root, dirs, files in os.walk(module_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('_')]
            if not cutoff or cutoff == root: # insert syspath if no cutoff is available
                if added: # remove anything added to the sys path
                    sys.path.remove(added)

                sys.path.insert(0, root)
                added = root

            os.chdir(root)
            for script in files:
                if not script.startswith('.') and not script.startswith('_') and script.endswith('.py'):

                    spec = importlib.util.spec_from_file_location(script.rstrip('.py'), os.path.join(root, script))
                    foo = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(foo)

                    path_list.append(script)

            os.chdir(home)


            if 'initialise.py' in files:
                cutoff = root

        sys.path.remove(added) # remove final path
        return path_list

    def load_default_configs(self):
        """loads the default configs that are used for
            verification and defaulting optional keys"""
        with open(self.default_config_path+'Default_Server.json') as server_file:
            self.default_server_config = json.load(server_file)

        with open(self.default_config_path+'/Default_Category.json') as category_file:
            self.default_category_config = json.load(category_file)


    def load_external_configs(self):
        """loads json configs from the configs folder and sorts
            their keys for easy reference"""

        self.config_ref = {}

        for file_name in os.listdir(self.home_dir+'/Configs'):
            if file_name.endswith('.json'):
                with open(self.home_dir+'/Configs/'+file_name) as config_file:
                    file_config = json.load(config_file)

                    for key in file_config:
                        if key in self.config_ref:
                            self.config_ref[key][file_name] = file_config[key]
                        else:
                            self.config_ref[key] = {file_name:file_config[key]}
                            self.config_ref[key]['CONFIG_TYPE'] = type(file_config[key])()




    def resolve_external_configs(self):
        """merge configs and return a single dictionary"""
        merged_config = {}
        for key, server in self.config_ref.items():
            key_type = type(self.config_ref[key]['CONFIG_TYPE'])
            merged_config[key] = type(self.config_ref[key]['CONFIG_TYPE'])()
            for server_name, presets in server.items():
                if key_type is list:
                    merged_config[key].extend(presets)
                elif key_type is dict:
                    merged_config[key].update(presets)


        return merged_config

    def get_defaults(self, key=None):
        """return default configs optionally only a certain section of them"""
        if key:
            return self.default_server_config[key], self.default_category_config[key]
        return self.default_server_config, self.default_category_config


    def get_key_origin(self, prim_key, sec_key):
        """given 2 keys, returns the file name of where the secondary key is held"""
        for file_name, items in self.config_ref[prim_key].items():
            if sec_key in items:
                return file_name
        return None


    def edit_channel(self, channel, action, key, value):
        """given a channel, edits the necessary config file
            using a given action and a given value"""
        server_id = str(channel.guild.id)
        channel_id = str(channel.id) # json has to work with the channel ID as a string
        file_name = self.get_key_origin('Servers', server_id)

        with open(self.home_dir+'/Configs/'+file_name) as config_file:
            temp_dict = json.load(config_file)
            server = temp_dict['Servers'][server_id]
            print(server)
            if 'channels' not in server:
                print('channels don\'t exist')
                server['channels'] = {}

            if channel_id not in server['channels']: # make sure there is a channel to edit
                val = copy.copy(temp_dict['Servers'][server_id][key])
                temp_dict['Servers'][server_id]['channels'][channel_id] = {key : val}

            print('before', server['channels'])

            if action == 'append':
                server['channels'][channel_id][key].append(value)

            elif action == 'remove' and value in server['channels'][channel_id][key]:
                server['channels'][channel_id][key].remove(value)

            print('after', server['channels'])

        with open(self.home_dir+'/Configs/'+file_name, 'w') as config_file:
            json.dump(temp_dict, config_file, sort_keys=True, indent=4, separators=(',', ': '))

        self.load_external_configs()
