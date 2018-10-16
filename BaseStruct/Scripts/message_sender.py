import asyncio

max_msg_size = 1500

async def send_message(channel, message_str, header='', footer='', msg_break='', recur_depth=1):
    """Parses and sends messages via recursion, if the message is larger
        than allowed, will parse it into send-able chunks, with the given
        "msg_break" at the top of the next sent message"""
    if not message_str:
        return

    if len(message_str) > max_msg_size:
        message_str = header+message_str
        stripped = message_str.strip()
        split_pos = message_str.rfind('\n',0,max_msg_size)

        if split_pos < 0:
            split_pos = max_msg_size

        message_head = '\n'+message_str[:split_pos]+footer
        message_tail = message_str[split_pos:]

        await really_send_message(channel, message_head)
        await send_message(channel, message_tail, header=msg_break, footer=footer, 
                             msg_break=msg_break, recur_depth=recur_depth+1)

    else:
        return await really_send_message(channel, header+message_str)

async def really_send_message(channel, message_str):
    """Awaits the parsed message, sending it to discord"""
    return await channel.send(message_str)
