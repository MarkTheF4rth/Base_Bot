def listen (client, main):

    @client.event
    async def on_message(message):
        main.message_handler(message)
