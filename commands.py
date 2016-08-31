class Main:
    def __init__(self, shelve):
        self.config = shelve.open('Configs/config-MASTER')
        self.in_messages = []
        self.out_messages = []

    def message_parser(self, message, edit=False):
        content = [a.split() for a in message.content.split(self.config['command_char'])[1:]]
        for item in content:
            self.in_messages.append([item, message])

    def message_handler(self):
        for content, message in self.in_messages:
            if 'handle_'+content[0].lower() in dir(self):
                print('Processed message: ', message.content, message.channel)
                if message.channel == self.config['hub']:
                    getattr(self, 'handle_'+content[0].lower())(content, message)

                self.in_messages.pop(0)

    def message_printer(self, message, channel):
        self.out_messages.append([channel, message])

    def handle_confirm(self, content, message):
        self.message_printer('**I live**', message.channel)

