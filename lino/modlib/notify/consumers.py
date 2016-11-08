from channels import Group


def ws_echo(message):
    Group(str(message.content['text'])).add(message.reply_channel)
    message.reply_channel.send({
        "text": message.content['text'],
    })
