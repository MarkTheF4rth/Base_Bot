#!/home/mc/python3.5.1/bin/python3.5
'''
This is a short test script which is build to check whether the bot can
receive and send messages in a given server, note that a token file must
be present for this script to work
'''

import discord, asyncio, sys, os
client = discord.Client()

@client.event
async def on_message(message):
    print('received message')
    if message.server.name == SERVER and message.author.name != 'Tournament-Bot':
        print('sending message')
        await client.send_message(message.channel, 'I live!')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

if __name__ == '__main__':
    INPUT = sys.argv[1:]
    if INPUT:
        SERVER = ' '.join(INPUT)
        if os.path.isfile('token.txt'):
            token = open('token.txt').readlines()[0].strip()
            client.run(token)
            client.connect()
        else:
            print('There is no token file present, make sure your file is named "token.txt"')
            sys.exit()
    else:
        print('You must input a server to be used')
        sys.exit()
