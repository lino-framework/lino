import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from lino.api import rt, dd

import logging
logger = logging.getLogger(__name__)


class ReactChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        if self.scope.get('user', False):
            group_uid = str(self.scope["user"].pk) # ideally should be user.PK..
            self.add_group(group_uid)
            self.add_group("CHAT") # not used.


    def add_group(self, group_uid):
        """Connects this channel to a group
        Can add several groups"""
        async_to_sync(self.channel_layer.group_add)(group_uid, self.channel_name)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        try:
            data = json.loads(text_data)
            # logger.info("Recived WS data: " + text_data)

            user =self.scope.get('user', False)

            # Very Basic auth for confirming that this user is the on sending this message.
            if user:
                data["user"] = user
                if dd.is_installed("chat"):
                    ChatMessage = rt.models.resolve("chat.ChatMessage") # TODO HAVE WHITELIST OF FUNCTIONS!
                    if data.get('function') and hasattr(ChatMessage,data.get('function')):
                        getattr(ChatMessage,data.get('function'))(data)
        except Exception as E:
            logger.exception(E)
            raise E


    def send_notification(self, text):
        ## just passes data through. real work is done in .api
        self.send(text_data=text['text'])
