def listen(client, main):

    @client.event
    async def on_ready(): 
        main.connected = True
