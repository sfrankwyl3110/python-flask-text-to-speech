from datetime import datetime, UTC
import asyncio
import base64
import json
import os
import uuid
import aiohttp
import pygame


class WYLTTS:
    tts_url = None
    default_tts_url = "http://ec2-3-71-10-192.eu-central-1.compute.amazonaws.com:8000/v1/audio/speech"
    default_post_headers = {
        "Content-Type": "application/json"
    }

    def __init__(self, tts_url=None):
        if tts_url is None:
            self.tts_url = self.default_tts_url
        else:
            self.tts_url = tts_url
        self.responses_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                "responses")
        if not os.path.isdir(self.responses_directory):
            os.makedirs(self.responses_directory, exist_ok=True)

    def make_json(self,
                  text_input,
                  model="tts-1",
                  voice="alloy",
                  response_format="mp3",
                  speed=1.0
                  ):
        json_data = {
            "model": model,
            "input": text_input,
            "voice": voice,
            "response_format": response_format,
            "speed": speed,
            "created_at": datetime.now(UTC).isoformat()
        }

        new_uuid = uuid.uuid4()
        filename_base = f"response-{new_uuid}"
        with open(os.path.join(self.responses_directory, f"{filename_base}.base64"), "w") as base64_f:
            base64_f.write(base64.b64encode(json.dumps(json_data).encode('utf-8')).decode('utf-8'))
        return filename_base, json_data

    @staticmethod
    async def play_sound(file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

    async def fetch(self, url, text_input, play=True):
        filename_base, json_data = self.make_json(text_input=text_input)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json_data, headers=self.default_post_headers) as response:
                if response.status == 200:
                    response_data = await response.read()
                    mp3_filename = f"{filename_base}.mp3"
                    mp3_filepath = os.path.join(self.responses_directory, mp3_filename)
                    with open(mp3_filepath, "wb") as f:
                        f.write(response_data)
                    if play:
                        print("playing sound...")
                        await asyncio.sleep(1)
                        await self.play_async(mp3_filepath)
                    return mp3_filepath

    async def main_get(self, url, text_input, play=True):
        result = await self.fetch(url, text_input, play)
        return result

    async def play_async(self, file_path):
        await self.play_sound(file_path)
        print("Sound has finished playing.")

    async def create_speech(self, text_input, play=True):
        result = await asyncio.gather(
            self.main_get(self.tts_url, text_input, play)
        )
        return result
