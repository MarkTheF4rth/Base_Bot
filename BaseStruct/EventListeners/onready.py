def listen(client, main):
    """Verifies that the client is connected to discord
        using the "connected" flag"""

    @client.event
    async def on_ready():
        main.connected = True
