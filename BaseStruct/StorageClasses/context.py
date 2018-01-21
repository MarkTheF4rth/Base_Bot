class Context:
    def __init__(self, roles, content, sorted_content):
        '''create a context object, given content and roles'''
        self.accepted_roles = roles
        self.message_content = sorted_content # dictionary of arguments and the parameters they apply to
        self.raw_message_content = content # list of command parameters

#    def set_message_content(self, split_content, split_content):
#        '''Sets the message content, based on what content there is,
#            and how the command should be used for easy referencing'''
#
#        self.raw_message_content = content
#        self.message_content = split_content
