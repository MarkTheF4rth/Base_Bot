import asyncio

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
                    if 'pm_help' in command.flags: 
                        pm_output.append((command_name, getattr(command, role))) 
                    else: 
                        output.append((command_name, getattr(command, role))) 
                    lengths.append(len(command_name)) 
                    break 
 
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
