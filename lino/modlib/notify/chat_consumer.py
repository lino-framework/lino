import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from pprint import pprint

class ReactChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        if self.scope.get('user', False):
            username = self.scope["user"].username # ideally should be user.PK..
            self.add_group(username)
            self.add_group("CHAT")


    def add_group(self, group_uid):
        """Connects this channel to a group
        Can add several groups"""
        async_to_sync(self.channel_layer.group_add)(group_uid, self.channel_name)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        pprint(text_data_json)
        # message = text_data_json['message']
        #
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))

    def send_notification(self, text):
        ## just passes data through. real work is done in .api
        self.send(text_data=text['text'])
