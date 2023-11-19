# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from openai import OpenAI
import os
from datetime import datetime

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=settings.OPENAI_API_KEY,
)




class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, how are you?"},
                {"role": "assistant",
                    "content": "I'm doing well, thank you. How can I assist you today?"},
                text_data_json
            ],
        )
        
        messageToSend = response.choices[0].message.content.strip()
        print('message to send',messageToSend)
        await self.send(text_data=json.dumps({
            "role": "assistant",
            "content": messageToSend,       
        }))
