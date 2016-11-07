def ws_echo(message):
    message.reply_channel.send({
        "text": message.content['text'],
    })
