import os, json, discord
from collections import OrderedDict
from StorageClasses.channel import Channel
from StorageClasses.formatted_command import FormattedCommand

class ConfigCreator:
    def __init__(self, client):
        self.client = client
        self.default_server_config, self.default_category_config = self.filesystem.get_defaults(key='optional')
        self.set_configs()
        self.command_char = self.config['Main']['command character']

    def set_configs(self):
        self.config = self.filesystem.resolve_external_configs()
        self.categories = self.format_categories(self.extension_dict['command'])
        self.channels = self.format_servers(self.config['Servers'])


    def format_commands(self, category_name, category_config, command_dict, explored):
        '''return a dict of name:command pairs that are involved in the given category'''
        formatted_commands = {}
        explored.append(category_name) # prevent infinite loops
        commands = {command_name:command_dict['ALL_COMMANDS'][command_name] for command_name in category_config['commands']}

        if category_name in command_dict:
            commands.update(command_dict[category_name])

        for command_name, command in commands.items():
            formatted_commands.update({command_name:FormattedCommand(command, category_config, category_name)})

        for subcategory_name in category_config['subcategories']:
            if subcategory_name not in explored:
                new_config = self.merge_configs(self.config['Categories'][subcategory_name], category_config)
                formatted_commands.update(self.format_commands(subcategory_name, new_config, command_dict, explored))

        return formatted_commands


    def format_categories(self, command_dict):
        '''formats categories and the  commands 
            inside them to a more easily readable format'''
        categories = {category:[] for category in self.config['Categories']}
        for category_name, category_config in self.config['Categories'].items():
            full_config = self.merge_configs(category_config, self.default_category_config)
            formatted_commands = self.format_commands(category_name, full_config, command_dict, [])
            categories[category_name] = formatted_commands

        return categories

    def format_servers(self, server_configs):
        '''adds the correct command with the desired presets to each channel'''
        channels = {}
        for server_id, server_config in server_configs.items():
            print('Formatting server {}'.format(server_id))
            server_config = self.merge_configs(server_config, self.default_server_config)
            server = self.client.get_server(server_id)
            for channel in server.channels:
                if channel.id in server_config['channels']:
                    merged_config = self.merge_configs(server_config['channels'][channel.id], server_config)
                    new_channel = self.format_channel(channel, merged_config)

                else:
                    new_channel = self.format_channel(channel, server_config)

                channels.update(new_channel)

        return channels


    def format_channel(self,  channel, channel_config):
        '''formats and returns single channel'''
        channel_commands = {}
        for category in channel_config['categories']:
            channel_commands.update(self.categories[category])

        return({channel.id:Channel(channel.id, channel_commands)})
                

    def merge_configs(self, primary_config, fallback_config):
        '''merges a fallback config into a given config, 
            filling any gaps in keys the primary config may have'''
        for key in fallback_config:
            if key not in primary_config:
                primary_config[key] = fallback_config[key]

        return primary_config

