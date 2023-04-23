# consumers are the channel's version of django views
#   which handles incoming client requests
# But they can also initiate requests to the clients while still listening
# on incoming connections
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

# For receiving cilent request and broadcasting them to everyone in Chat
class ChatConsumer(WebsocketConsumer):
    # when the connection is first successful, we will send a message
    def connect(self):
        self.room_group_name = 'test'
        # Add a user's channel to the group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        # upon successful connection send to user browser a success message
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connection successful!',
        }))
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print(message) 
        # send back to the user browser (only who sent the msg) a text_data object
        # self.send(text_data=json.dumps({
        #     'type':'chat',
        #     'message':message
        # }))

        # Broadcast to channel layer group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {   # message & name of function to handle this event
                'type':'chat_message',
                'message':message
            }
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))