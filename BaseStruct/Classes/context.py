class Context:
    def __init__(self, roles, content, sorted_content):
        '''create a context object, given content and roles'''
        self.accepted_roles = roles
        self.message_content = sorted_content # dictionary of arguments and the parameters they apply to
        self.raw_message_content = content # list of command parameters
