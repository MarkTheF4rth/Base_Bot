def listen(client, main):

    @client.event
    async def on_message_edit(old, message):
        main.message_handler(message)

