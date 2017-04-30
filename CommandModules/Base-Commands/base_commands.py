import discord, asyncio
from command import command
from task import task
from func import func

@command(description='Displays this message')
def help(self, message, ctx): 
    command_list = {} 
    output = [] 
    pm_output = [] 
    header = ['__**A list and brief description of each command you can use:**__'] 
    msg_break = '**Continued...**' 
    lengths = [] 
 
    for command_name, command in self.commands.items():
        description = command.get_description(message.channel, message.author.roles)
        if not description:
            continue
        command_name = '/'.join(command.aliases)
        if 'pm_help' in command.flags: 
            pm_output.append((command_name, description))
        else: 
            output.append((command_name, description))
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

@command(aliases=['c'], arglen=0, description='Confirms the bot is still alive')
def confirm(self, message, ctx): 
    livemessage = self.addattr()
    self.message_printer(livemessage, message.channel)

@func()
def addattr(self):
    return '**I live**'

