# Discord Bot: 
# Role: Provides daily photo images of mars using NASA API
# Implements a webscraper to pull recent articles of mars that day
# Also use the mars weather API

import discord
import random 
import os
import requests
import json
from PIL import Image
import urllib.request


response = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?api_key=DEMO_KEY&earth_date=2021-7-21")

obj = json.loads(response.text)

url_to_file = {}

numOfPhotos = len(obj["photos"])
if numOfPhotos == 0 :
  print('TRy agAin')
if numOfPhotos < 3 :
  for photos in obj["photos"] :
    url_to_file[photos['img_src'] : photos['img_src'].split("/")[-1:][0]]
else :
  for photos in random.sample(range(0, numOfPhotos), 3) :
    url = obj["photos"][photos]["img_src"]
    file_name = url.split("/")[-1:][0]
    url_to_file[url] = file_name

print(url_to_file)
  


'''urllib.request.urlretrieve(url, file_name)
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
'''