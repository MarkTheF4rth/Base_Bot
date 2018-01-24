def listen(client, main):
    """Listens for when messages are editted in discord,
        sends them to the message handler"""

    @client.event
    async def on_message_edit(old, message):
        main.message_handler(message, True)

