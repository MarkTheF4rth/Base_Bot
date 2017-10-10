def listen (client, main):
    """Sends a recieved message to the message handler"""

    @client.event
    async def on_message(message):
        main.message_handler(message, False)
