def listen(client, message_handler):

    @client.event
    async def on_ready(): 
        print('Logged in as') 
        print(client.user.name) 
        print(client.user.id) 
        print('-----')
