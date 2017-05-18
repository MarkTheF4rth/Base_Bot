import asyncio
import importlib
import os
import sys
import threading
import time
from StorageClasses import context

class Main(object):
    def __init__(self, client):
        self.in_messages = []
        self.out_messages = []
        self.pending_tasks = []
        self.connected = False
        self.running = True
        self.client = client
        self.commands = []
        self.home_dir = os.getcwd()+'/'
        self.data_dir = os.getcwd()+'/Data/'
        self.config_dir = os.getcwd()+'/Configs/'
        self.command_dir = os.getcwd()+'/CommandModules/'
        self.tasks = {'call':{}, 'init':{}, 'onmessage':{}, 'oncommand':{}}

    def set_config(self, config):
        self.raw_config =   config[0]
        self.commands =     config[1]
        self.command_ref =  config[2]
        self.command_char = config[3]

    def resolve_external(self, external_dict, thread_loop):
        self.commands = external_dict['command']
        print('---Integrating external commands:')
        for command_name in self.commands:
            print('------{} added'.format(command_name))
        print('\n')
        print('---Integrating external functions:')
        for func, func_name in external_dict['func'].items():
            setattr(self, func_name, func)
            func.main = self
            print('------{} added'.format(func_name))

        print('\n')

        self.resolve_tasks(external_dict['task'], thread_loop)
        print('\n')

    def resolve_tasks(self, task_dict, thread_loop):
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
        if not message.content.startswith(self.command_char):
            return

        if self.raw_config['Main']['chain commands'] == 'True':
            content = [a.split() for a in message.content.split(self.raw_config['Main']['command char'])[1:]]
        else:
            content = [message.content[1:].split()]

        for item in content:
            for task in self.tasks['onmessage']:
                task(self)
            self.in_messages.append((item, message))

    def command_handler(self):
        for content, message in self.in_messages:
            self.in_messages.pop(0)
            if content[0] in self.command_ref:
                command = self.commands[self.command_ref[content[0]]]

                if not command.validate_length(len(content)-1):
                    self.message_printer('Please use a valid amount of arguments for this comand', message.channel)
                    break

                accepted_roles = command.validate_role(message.channel.id, message.author.roles) 
                print('Processed message from: {} with roles:{} in channel:{} ... message:{}'.format(message.author, [role.name for role in accepted_roles], message.channel,  message.content))
                if accepted_roles:
                    ctx = context.Context()
                    ctx.accepted_roles = accepted_roles
                    ctx.message_content = content[1:]
                    command(self, message, ctx)
                    break


    def message_printer(self, message, channel, header='', msg_break=''):
        if channel == 'hub':
            channel = self.hub_channel
        self.out_messages.append([channel, message, header, msg_break])

    def call_task(self, task, *args, **kwargs):
        self.pending_tasks.append([self.tasks['call'][task], [*args], {**kwargs}])
