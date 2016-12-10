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
            if 'handle_'+content[0].lower() in dir(self):
                print('Processed message: ', message.content, message.channel)
                if message.channel == self.config['Main']['hub']:
                    getattr(self, 'handle_'+content[0].lower())(content, message)


    def message_printer(self, message, channel):
        if channel == 'hub':
            channel = self.config['Main']['hub']
        self.out_messages.append([channel, message])

    def handle_confirm(self, content, message):
        self.message_printer('**I live**', message.channel)

    def runtime_commands(self): #commands which will run through every second
        pass
