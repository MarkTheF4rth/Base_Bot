# Discord-Bot-Base-Structure V 3.0.0
Serves as a bridge between the Discord API and various scripts to handle bot functions in Discord

Dependancies:
The only dependancy for this project is discord. This project uses discord rewrite which can be obtained via the command:
sudo pip3 install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]

Discord Dependancies include:
python3.5+ (remember to install pip3 to be able to install discord)
libffi-dev (pre-installed on newer operating systems)

Usage:
git clone a project into CommandModules
create a token.txt in base dir
create configs (Template coming soon)
run run.py with python3.5+
to stop the bot you will need to ctrl+c or ctrl+z exit


Manual:
Here I will explain syntax when creating your own bot that uses base bot...

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
