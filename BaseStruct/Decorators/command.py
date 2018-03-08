from Initialise.initialise import add_command
import re

def command(aliases=[], description=None, category='Default', usage=[['']]):
    class command_struct(object):
        """Stores information about a specific command"""
        def __init__(self, function):
            add_command({function.__name__:self}, category)
            self.name = function.__name__
            self.aliases = [function.__name__] + aliases
            self.description = description
            self.category = category
            self.roles = []
            self.raw_usage = usage
            self.usage_string, self.usage = self.usage_interpreter(usage)

            self.run = function

        def usage_interpreter(self, usage):
            """Intereprets given usage parameter into readable text"""

            # match symbols to descriptions
            symref = {
                    ''  : "{} args",
                    '-' : "",
                    '_' : "",
                    '?' : "optional",
                    '<' : "less than {} args",
                    '>' : "more than {} args",
                    '<=': "less or equal to {} args",
                    '>=': "more or equal to {} args",
                    'i' : "integer"}

            usage_list = [] # list of descriptions
            compact_operands = [] # better compiled usage list for future calculations

            for item in usage:
                if type(item) == str: # allow parameters without operands
                    item = (item, '')
                if item[0]: # don't process empty strings
                    operand_description_list = []
                    operands = {'name':item[0], 'length':('=', 1), 'operands':[]}


                    for operand in item[1:]:
                        numeric = re.match(r'([<>=]{,2})([0-9]*)', operand)
                        if any(numeric.groups()):
                            operand_description_list.append(symref[numeric.group(1)].format(numeric.group(2)))
                            sign = numeric.group(1)
                            if not sign:
                                sign = '='

                            operands['length'] = (sign, int(numeric.group(2)))

                        else:
                            operand_description_list.append(symref[operand])
                            operands['operands'].append(operand)

                            if operand == '?': # optional arguments have a required length of 0
                                operands['length'] = ('=', 0)

                    if operand_description_list:
                        usage_list.append('<{} ({})>'.format(item[0], '|'.join(operand_description_list)))

                    else:
                        usage_list.append('<{}>'.format(item[0]))

                    compact_operands.append(operands)

            return ','.join(usage_list), compact_operands


        def __call__(self, *args, **kwargs):
            self.run(*args, **kwargs)

    return command_struct
