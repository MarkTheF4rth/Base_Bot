import asyncio
import initialiser
class Main(initialiser.ConfigInitialiser):
    def __init__(self, shelve):
        self.in_messages = []
        self.out_messages = []
        self.init_flag = False

    def message_handler(self, message, edit=False):
        if self.init_flag:
            self.in_messages.append(message)
        elif message.content.lstrip().startswith(self.config['Main']['command_char']): #removes leading spaces and checks that the message begins with the command character
            self.message_parser(message, edit)

    def message_parser(self, message, edit):
        content = [a.split() for a in message.content.split(self.config['Main']['command_char'])[1:]]
        for item in content:
            self.in_messages.append([item, message])

    def command_handler(self):
        for content, message in self.in_messages:
            self.in_messages.pop(0)
            if content[0] in self.channels[message.channel.id]:
                command = self.channels[message.channel.id][content[0]]
                print('Processed message: ', message.content, message.channel)
                for role in message.author.roles:
                    print(role.name, command.roles)
                    if role.name in command.roles:
                        if command.alias_of:
                            getattr(self, 'handle_'+command.alias_of)(content, message)
                        else:
                            getattr(self, 'handle_'+content[0].lower())(content, message)
                        break

    def message_printer(self, message, channel):
        if channel == 'hub':
            channel = self.hub_channel
        self.out_messages.append([channel, message])

    def handle_help(self, content, message):
        command_list = {}
        for command, help_dict in self.channels[message.channel.id].items():
            help_dict = help_dict['help']
            if type(help_dict) == str:
                command_list[command] = help_dict
            else:
                for pair in help_dict:
                    print(pair)
                    role, help_message = [(x, y) for x, y in pair.items()][0]
                    if role in [x.name for x in message.author.roles]:
                        command_list[command] = help_message

        output = []
        for command, help_message in command_list.items():
            formatted_command = command+', '+', '.join(self.channels[message.channel.id][command]['aliases'])
            output.append('**'+formatted_command+'** : '+help_message)

        self.message_printer('\n'.join(output), message.channel)

    def handle_confirm(self, content, message):
        self.message_printer('**I live**', message.channel)

    def runtime_commands(self): #commands which will run through every second
        pass
