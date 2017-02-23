def listen(client, main):

    @client.event
    async def on_ready(): 
        print('Logged in as') 
        print(client.user.name) 
        print(client.user.id) 
        print('-----')
        main.connected = True
