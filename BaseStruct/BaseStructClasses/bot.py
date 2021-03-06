import os
from BaseStructClasses import context
from Initialise.config_creator import ConfigCreator

FOUNDATION_DESCRIPTION = 'The foundation of the Bot, which all modules are built off of.'
FOUNDATION_CREDITS = 'Created by @MII#0255 (<https://github.com/MarkTheF4rth/Base_Bot>)'

class Bot(ConfigCreator):
    def __init__(self, client, extension_dict, filesystem):
        self.filesystem = filesystem
        self.extension_dict = extension_dict
        self.in_messages = []
        self.out_messages = []
        self.pending_tasks = []
        self.connected = False
        self.running = True
        self.client = client
        self.commands = []
        self.home_dir = self.filesystem.home_dir
        self.data_dir = self.home_dir+'/Data/'
        self.config_dir = self.home_dir+'/Configs/'
        self.command_dir = self.home_dir+'/CommandModules/'
        self.module_info = {'Foundation':(FOUNDATION_DESCRIPTION, FOUNDATION_CREDITS)}
        self.tasks = {'call':{}, 'init':{}, 'onmessage':{}, 'oncommand':{}}

    def resolve_external(self, external_dict, thread_loop):
        """Resolves external commands, functions,
            and tasks, to add them to self"""
        ConfigCreator.__init__(self, self.client)
        self.commands = external_dict['command']
        print('---Integrating external commands:')
        for command_name in self.commands:
            print('------{} added'.format(command_name))
        print('\n')
        print('---Integrating external functions:')
        for func_name, func in external_dict['func'].items():
            setattr(self, func_name, func)
            func.main = self
            print('------{} added'.format(func_name))

        print('\n')

        self.resolve_tasks(external_dict['task'], thread_loop)
        print('\n')

    def resolve_tasks(self, task_dict, thread_loop):
        """Resolves adding external tasks, verifying
            that they can be added first"""
        self.thread_loop = thread_loop
        print('Resolving tasks:')
        print('---Reading tasks:')
        for name, task in task_dict.items():
            if not task.valid:
                print('------WARNING {} could not be resolved, (function needs to be a coroutine) omitting...'.format(name))
                continue

            if task.run_time in self.tasks:
                self.tasks[task.run_time].update({name:task})
                print('------{} resolved (run time = {})'.format(name, task.run_time))
            else:
                print('------WARNING {} could not be resolved, (run time {} not recognised) omitting...'.format(name, task.run_time))

        print('---Initialising tasks:')
        for name, task in self.tasks['init'].items():
            thread_loop.create_task(task(self))
            print('------{} initialised'.format(name))

    def message_handler(self, message, edit):
        """Receives messages, parses them,
            and sends them to the command handler"""
        if (not message.content.startswith(self.command_char)) or (message.channel.id not in self.channels):
            return

        if self.config['Main']['chain commands']:
            content = [a.split() for a in message.content.split(self.config['Main']['command character'])[1:]]
        else:
            content = [message.content[1:].split()]

        for item in content:
            for task in self.tasks['onmessage']:
                task(self)
            self.in_messages.append((item, message))

    def command_handler(self):
        """Handles incoming commands, running them if they are valid"""
        for content, message in self.in_messages:
            self.in_messages.pop(0)
            channel = self.channels[message.channel.id]
            command, accepted_roles = channel.get_command(content[0], message.author.roles)

            if accepted_roles:
                par_ref, error = command.validate_input(content[1:])
                if error:
                    self.message_printer(error, message.channel)
                    break

                print('Processed message from: {} with roles:{} in channel:{} ... message:{}'.format(message.author, [role.name for role in accepted_roles], message.channel,  message.content))
                ctx = context.Context(accepted_roles, content[1:], par_ref)
                command(self, message, ctx)
                break


    def message_printer(self, message, channel, header='', footer='', msg_break=''):
        """Adds a given message to the print queue"""
        if channel == 'hub':
            channel = self.hub_channel
        self.out_messages.append([channel, message, header, footer, msg_break])

    def call_task(self, task, *args, **kwargs):
        """Calls a given task with the given arguments"""
        self.pending_tasks.append([self.tasks['call'][task], [*args], {**kwargs}])
