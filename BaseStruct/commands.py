import asyncio
import initialiser
import importlib
import os
import sys
sys.path.insert(0, '/home/ec2-user/BOTS/Base_Bot/CommandModules')

class Context:
    def __init__(self):
        self.accepted_roles = []
        self.message_content = []

class Main(initialiser.ConfigInitialiser):
    def __init__(self):
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

def command(func):
    setattr(Main, "handle_"+func.__name__, func)

