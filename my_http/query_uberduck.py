from io import BytesIO
import asyncio
import json
import time
import os
import aiohttp

# Your Uberduck API key and API secret.
# You can create a new key and secret at https://app.uberduck.ai/account/manage
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
API_ROOT = "https://api.uberduck.ai"



async def query_uberduck(text, voice="zwf"):
    max_time = 60
    print(f'!!!!!!!!!!!!!!!!!!!!! {text}')
    async with aiohttp.ClientSession() as session:
        url = f"{API_ROOT}/speak"
        data = json.dumps(
            {
                "speech": text,
                "voice": voice,
            }
        )

        start = time.time()
        async with session.post(
            url,
            data=data,
            auth=aiohttp.BasicAuth(API_KEY, API_SECRET),
        ) as r:
            if r.status != 200:
                print('fucking up at first speak query')
                raise Exception("Error synthesizing speech", await r.json())
                
            uuid = (await r.json())["uuid"]
        while True:
            if time.time() - start > max_time:
                raise Exception("Request timed out!")
            await asyncio.sleep(1)
            status_url = f"{API_ROOT}/speak-status"
            async with session.get(status_url, params={"uuid": uuid}) as r:
                if r.status != 200:
                    continue
                response = await r.json()
                print(type(response))
                if response["path"]:
                    async with session.get(response["path"]) as r:
                        return BytesIO(await r.read())
                    

        


# async def get_available_voices(self):
#     url = "https://api.uberduck.ai/voices"
#     headers = {
#         "API-KEY": API_KEY,
#         "API-SECRET": API_SECRET,
#     }
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, headers=headers) as response:
#             if response.status == 200:
#                 data = await response.json()
#                 return data
#             else:
#                 print(f"Error: {response.status}")
#                 return []


# async def get_available_voices(self):
#     url = "https://api.uberduck.ai/voices"
#     headers = {
#          "accept": "application/json",
#     "authorization": aiohttp.BasicAuth(API_KEY, API_SECRET),
# }
    
#     params = {
#         "mode": "tts-all",  # or any other mode you prefer
#         "language": "english"
#     }
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, headers=headers, params=params) as response:
#             if response.status == 200:
#                 data = await response.json()
#                 return data
#             else:
#                 print(f"Error: {response.status}")
#                 return []

async def get_available_voices(self):
    url = "https://api.uberduck.ai/voices"
    headers = {
        "x-api-key": API_KEY,
        "x-api-secret": API_SECRET,
    }
    params = {
        "mode": "tts-all",  # or any other mode you prefer
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                print(data)
                return data
            else:
                print(f"Error: {response.status}")
                return []

