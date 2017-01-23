import asyncio
import initialiser

class Context:
    def __init__(self):
        self.accepted_roles = []
        self.message_content = []

class Main(initialiser.ConfigInitialiser):
    def __init__(self, shelve):
        self.in_messages = []
        self.out_messages = []
        self.init_flag = False

    def message_handler(self, message, edit=False):
        if self.init_flag:
            self.in_messages.append(message)
        elif message.content.lstrip().startswith(self.config['Main']['command char']): #removes leading spaces and checks that the message begins with the command character
            self.message_parser(message, edit)

    def message_parser(self, message, edit):
        content = [a.split() for a in message.content.split(self.config['Main']['command char'])[1:]]
        for item in content:
            self.in_messages.append([item, message])

    def command_handler(self):
        for content, message in self.in_messages:
            self.in_messages.pop(0)
            if message.channel.id in self.channels and content[0] in self.channels[message.channel.id]:
                command = self.channels[message.channel.id][content[0]]
                print('Processed message: ', message.content, message.channel)
                accepted_roles = set([role.name for role in message.author.roles]) & set(command.roles)
                if accepted_roles:
                    ctx = Context()
                    ctx.accepted_roles = accepted_roles
                    ctx.message_content = content
                    if command.alias_of:
                        getattr(self, 'handle_'+command.alias_of)(message, ctx)
                    else:
                        getattr(self, 'handle_'+content[0].lower())(message, ctx)
                    break

    def message_printer(self, message, channel, header='', msg_break=''):
        if channel == 'hub':
            channel = self.hub_channel
        self.out_messages.append([channel, message, header, msg_break])

    def handle_help(self, message, ctx):
        command_list = {}
        output = []
        pm_output = []
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
                        print(command.flags)
                        if 'pm_help' in command.flags:
                            pm_output.append((command_name, getattr(command, role)))
                        else:
                            output.append((command_name, getattr(command, role)))
                        lengths.append(len(command_name))

        command_length = max(lengths)
        if output:
            final_message_pb = header+['**`{:<{length}} :`** {}'.format(x, y, length=command_length) for x, y in output]
            self.message_printer('\n'.join(final_message_pb), message.channel, msg_break=msg_break)
        else:
            self.message_printer('No help message can be displayed at this time', message.channel)   
        if pm_output:
            final_message_pm = header+['**`{:<{length}} :`** {}'.format(x, y, length=command_length) for x, y in pm_output]
            self.message_printer('\n'.join(final_message_pm), message.author, msg_break=msg_break)

    def handle_confirm(self, message, ctx):
        self.message_printer('**I live**', message.channel)

    def runtime_commands(self): #commands which will run through every second
        pass
