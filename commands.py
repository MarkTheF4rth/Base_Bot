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
            if message.channel.id in self.channels and content[0] in self.channels[message.channel.id]:
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

    def auth_verify(self, user, command):
        pass

    def message_printer(self, message, channel, header='', msg_break=''):
        if channel == 'hub':
            channel = self.hub_channel
        self.out_messages.append([channel, message, header, msg_break])

    def handle_help(self, content, message):
        command_list = {}
        output = []
        header = ['__**A list and brief description of each command you can use:**__']
        msg_break = '**Continued...**'
        lengths = []

        for command_name, command in self.channels[message.channel.id].command_pairs:
            aliases = []
            for role in command.roles:
                if role in [x.name for x in message.author.roles]:
                    if not command.alias_of and getattr(command, role):
                        if command.aliases:
                            command_name = command_name + '/' + '/'.join(command.aliases)
                        output.append((command_name, getattr(command, role)))
                        lengths.append(len(command_name))

        command_length = max(lengths)
        final_message = header+['**`{:<{length}} :`** {}'.format(x, y, length=command_length) for x, y in output]
        self.message_printer('\n'.join(final_message), message.channel, msg_break=msg_break)

    def handle_confirm(self, content, message):
        self.message_printer('**I live**', message.channel)

    def runtime_commands(self): #commands which will run through every second
        pass
