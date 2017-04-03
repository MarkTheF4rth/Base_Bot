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
        self.connected = False
        self.client = client
        self.commands = []
        self.tasks = {'call':{}, 'init':{}, 'onmessage':{}, 'oncommand':{}}

    def set_config(self, config):
        self.raw_config = config.raw_config
        self.commands = config.command_config

    def resolve_tasks(self, task_dict, thread_loop):
        self.thread_loop = thread_loop
        print('Resolving tasks:')
        print('---Reading tasks:')
        for name, task in task_dict.items():
            if task.run_time in self.tasks:
                self.tasks[task.run_time].update({name:task})
                print('------{} resolved (run time = {})'.format(name, task.run_time))
            else:
                print('------WARNING {} could not be resolved, (run time {} not recognised) omitting...'.format(name, task.run_time))

        print('---Initialising tasks:')
        for name, task in self.tasks['init'].items():
            thread_loop.create_task(task(self))
            print('------{} initialised'.format(name))

    def message_handler(self, message, edit=False):
        if message.channel.id in self.commands.command_tree and message.content.lstrip().startswith(self.raw_config['Main']['command char']):
            self.message_parser(message, edit)

    def message_parser(self, message, edit):
        content = [a.split() for a in message.content.split(self.raw_config['Main']['command char'])[1:]]
        for item in content:
            for task in self.tasks['onmessage']:
                task(self)
            self.in_messages.append([item, message])

    def command_handler(self):
        for content, message in self.in_messages:
            self.in_messages.pop(0)
            if content[0] in self.commands[message.channel.id]:
                command = self.commands[message.channel.id][content[0]]

                if not command.valid_len(len(content)):
                    self.message_printer('Please use a valid amount of arguments for this comand', message.channel)
                    break

                print('Processed message: ', message.content, message.channel)
                accepted_roles = set([role.name for role in message.author.roles]+[message.author.id]) & set(command.roles[message.channel.id])
                if accepted_roles:
                    ctx = context.Context()
                    ctx.accepted_roles = accepted_roles
                    ctx.message_content = content
                    command(self, message, ctx)
                    break

    def message_printer(self, message, channel, header='', msg_break=''):
        if channel == 'hub':
            channel = self.hub_channel
        self.out_messages.append([channel, message, header, msg_break])
