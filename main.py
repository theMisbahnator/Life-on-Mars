# Discord Bot: 
# Role: Provides daily photo images of mars using NASA API
# Implements a webscraper to pull recent articles of mars that day
# Also use the mars weather API

import discord
import os
import requests
import json
from PIL import Image
import urllib.request


response = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key=DEMO_KEY")

obj = json.loads(response.text)


url = obj["photos"][0]['img_src']
file_name = url.split("/")[-1:][0]

print(file_name)

urllib.request.urlretrieve(url, file_name)



img = Image.open(file_name)

img.show()

os.remove(file_name)

# print(obj)


#client = discord.Client()

#@client.event
#async def on_ready():
#    print('We have logged in as {0.user}'.format(client))

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return

#    if message.content.startswith('$hello'):
#        await message.channel.send('Hello!')

#client.run(os.getenv('TOKEN'))