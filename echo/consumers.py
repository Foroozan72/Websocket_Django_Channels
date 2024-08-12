# from channels.generic.websocket import WebsocketConsumer


# class EchoConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self , close_code):
#         pass

#     def receive(self, text_data):
#         self.send(text_data=text_data)


from channels.generic.websocket import WebsocketConsumer
import json

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

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print(self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)


