def listen (client, message_handler):

    @client.event
    async def on_message(message):
        message_handler(message)
