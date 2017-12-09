class Context:
    def __init__(self):
        self.accepted_roles = []
        self.message_content = {} # dict of parameter:value
        self.raw_message_content = [] # list of command parameters

    def set_message_content(self, content, usage):
        '''Sets the message content, based on what content there is, 
            and how the command should be used for easy referencing'''
        place_counter = 0

        self.raw_message_content = content

        for use_type in usage:
            if use_type[1] == '...':
                if self.message_content:
                    self.message_content[use_type[0]] = content[place_counter:]

                else:
                    self.message_content = self.raw_message_content

                break

            self.message_content[use_type[0]] = content[place_counter]
            place_counter += 1

