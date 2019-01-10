import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class LinoConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        if self.scope.get('user', False):
            username = self.scope["user"].username
            async_to_sync(self.channel_layer.group_add)(username, self.channel_name)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

    def send_notification(self, text):
        self.send(text_data=text['text'])
