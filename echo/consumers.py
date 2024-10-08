
#uvicorn core.asgi:application --reload
# from channels.generic.websocket import WebsocketConsumer , AsyncWebsocketConsumer
# import json

# from asgiref.sync import async_to_sync


from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer, JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
import urllib.parse as urlparse



class EchoConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None , bytes_data=None):
        if text_data:
            self.send(text_data=text_data + " - send by server ") 
        elif bytes_data:
            self.send(bytes_data=bytes_data) 

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.username = self.scope['url_route']['kwargs']['username']
#         self.group_name = f"chat_{self.username}"

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.accept()
#         # print(self.channel_name)
        

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data=None, bytes_data=None):
#         if text_data:
#             text_data_json = json.loads(text_data)
#             username = text_data_json['receiver']
#             user_group_name = f"chat_{username}"

#             await self.channel_layer.group_send(
#                 user_group_name,
#                 {
#                     'type' : 'chat_message',
#                     'message' : text_data
#                 })

#     async def chat_message(self,event):
#         message = event['message']

#         await self.send(text_data=message)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.group_name = f"chat_{self.username}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            username = text_data_json['receiver']
            user_group_name = f"chat_{username}"

            if 'audio' in text_data_json:
                # Handling audio messages
                await self.channel_layer.group_send(
                    user_group_name,
                    {
                        'type': 'audio_message',
                        'audio': text_data_json['audio'],
                        'sender': text_data_json['sender']
                    }
                )
            elif 'text' in text_data_json:
                # Handling text messages
                await self.channel_layer.group_send(
                    user_group_name,
                    {
                        'type': 'chat_message',
                        'message': text_data_json['text'],
                        'sender': text_data_json['sender']
                    }
                )
            else:
                # Handling unsupported message types
                print("Unsupported message type received.")

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Sending the text message back to the client
        await self.send(text_data=json.dumps({
            'type': 'text',
            'text': message,
            'sender': sender
        }))

    async def audio_message(self, event):
        audio = event['audio']
        sender = event['sender']

        # Sending the audio data back to the client
        await self.send(text_data=json.dumps({
            'type': 'audio',
            'audio': audio,
            'sender': sender
        }))



class ChatConsumer2(AsyncConsumer):
    async def websocket_connect(self, event):
        self.user_id = self.scope['url_route']['kwargs']['username']
        self.group_name = f"chat_{self.user_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer()


    async def websocket_receive(self, event):
        text_data = event.get('text', None)
        bytes_data = event.get('bytes', None)

        if text_data:
            text_data_json = json.loads(text_data)
            username = text_data_json['receiver']
            user_group_name = f"chat_{username}"
            
            await self.channel_layer.group_send(
                user_group_name,
                {
                    'type': 'chat_message',
                    'message': text_data
                }
            )
            await self.channel_layer.group_send(
                'echo_1',
                {
                    'type': 'echo_message',
                    'message': text_data
                }
            )

    async def chat_message(self, event):
        message = event['message']

        await self.send({
            'type': 'websocket.send',
            'text': message
        })



class TestConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
    
        await self.accept()
    
    async def disconnect(self, close_code):
        pass

    async def receive_json(self, content):
        await self.send_json(content)

