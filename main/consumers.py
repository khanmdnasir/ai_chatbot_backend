# chat/consumers.py

import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from openai import OpenAI
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get('OPENAI_API_KEY'),
)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
 
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user","content":"hi"},
                {"role": "assistant", "content":"what's up"},
                {"role": "user", "content": "Hello, how are you?"},
                {"role": "assistant",
                    "content": "I'm doing well, thank you. How can I assist you today?"},
                {"role": "user", "content": text_data_json['message']}
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stream=True
        )

        stream = 'start'
        for r in response:
            await asyncio.sleep(0.5)
            messageToSend = r.choices[0].delta.content
            print('message to send', {
                "stream": stream,
                "message": messageToSend,
            })
            
            await self.send(text_data=json.dumps({
                "stream": stream,
                "message": messageToSend,
            }))
            stream = True
            
        await self.send(text_data=json.dumps({
            "stream": False,
        }))
