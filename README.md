# Discord-Bot-Base-Structure V 3.0.1
Serves as a bridge between the Discord API and various scripts to handle bot functions in Discord

Dependancies:
The only dependancy for this project is discord. This project uses discord rewrite which can be obtained via the command:
sudo pip3 install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]

Discord Dependancies include:
python3.5+ (remember to install pip3 to be able to install discord)
libffi-dev (pre-installed on newer operating systems)

# Usage:
git clone a project into CommandModules
create a token.txt in base dir
create configs for your project
run run.py with python3.5+
to stop the bot you will need to ctrl+c or ctrl+z exit


# Configs:
## Main:
Find the template in BaseStruct/ConfigTemplates.
All fields in this section are required, they will dictate the general behaviour of the bot
"command character" - the character used to run a command for the bot 
"chain commands" - allows multiple commands to be passed in a single message, if the command character comes up more than once, recommended for simple bots with less complex commnads

## Servers:
This section controls what servers/channels the bot can respond in, all fields in this section are a server id followed by a dictionary, see template for details.
Every server has the following fields:
"categories" - the command categories which are enabled in the server
"channels" - a subset of server, used to set configs specifically for channels within the server, it behaves identical to server, without a "channels" field

## Categories:
All commands are sorted into categories, generally by the module they belong to. In this section you can set the behaviour of each category, and what commands they hold.
If a category is defined within a function definition, and that category is added to the config, it will automatically populate with all commands that specified that category in their function definition. Also categories do not need to be defined here to be included in server configurations.
All fields in this section are optional, they are as follows:
"display" - (defaults to true) a flag to communicate that this function should not be displayed in help calls
"roles" - (defaults to ["@everyone"]) a list of roles that are allowed to access this command
"pm\_help" (defaults to false) communicates that help functions should be PM'd to the user when querying this command
"commands" (defaults to []) a list of commands that are in this category
"subcategories" (defaults to []) a list of categories that should inherit the configs in this category


Usage syntax:
The usage parameter defines what arguments should be passed to the bot, it is written as
usage=[('operator', 'operand1', 'operand2'), ('operator2', 'operand')]
Where the operator is the name of the parameter to be passed. If two conflicting operands are passed, only the first will be read.

Operand meanings
(empty) - this argument is required
'?' - this argument is optional
'n' (integer) - n number of arguments are required for this parameter
'<\n' (integer) - up to n number of arguments are required for this parameter (this must be the last parameter)
'>\n' (integer) - the number of arguments given for this parameter must be higher than n
'i' - argument must be an integer
