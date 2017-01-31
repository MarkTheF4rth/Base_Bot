def listen(client, message_handler):

    @client.event
    async def on_message_edit(old, message):
        message_handler(message)

