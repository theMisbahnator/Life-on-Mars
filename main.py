# Discord Bot: 
# Role: Provides daily photo images of mars using NASA API
# Implements a webscraper to pull recent articles of mars that day
# Also use the mars weather API

import discord
from discord.ext import commands
import random 
import os
import requests
import json
from datetime import datetime
import urllib.request

'''
Chooses three random photos 
from the plethora of photos taken from mars 
rovers on a given date. If there are less than three 
photos, then it sends what is available.

Returns a dictionary with the structure
key           value 
[photo URL] : [file name, Rover, Camera type, date taken]  
'''
def composeURLPhotos(apiCall, photoType) :
  response = requests.get(apiCall)
  obj = json.loads(response.text)
  url_to_file = {}
  numOfPhotos = len(obj[photoType])
  if numOfPhotos == 0 :
    return None
  if numOfPhotos < 3 :
    for photos in obj[photoType] :
      url_to_file[photos['img_src']] = photos['img_src'].split("/")[-1:][0]
  else :
    for photos in random.sample(range(0, numOfPhotos), 3) :
      url = obj[photoType][photos]["img_src"]
      file_name = url.split("/")[-1:][0]
      rover = obj[photoType][photos]["rover"]["name"]
      camera = obj[photoType][photos]["camera"]["full_name"]
      date_taken = obj[photoType][photos]["earth_date"]

      url_to_file[url] = [file_name, rover, camera, date_taken]
  return url_to_file

def verfiyParam(*param) :
  params = []
  for arg in param :
    params.append(arg)
    if len(params) == 2 : 
      break
  rover = "perseverance"
  print(params)
  url_to_file = {} 
  if len(param) > 0 and param[0].lower() == "curiosity" :
    rover = 'curiosity'
  if len(param) > 1 and bool(datetime.strptime(param[1], "%Y-%m-%d")) == True :
    url_to_file = composeURLPhotos("https://api.nasa.gov/mars-photos/api/v1/rovers/{}/photos?api_key=4hvbdm3crmOBYueVE4FJSwRG3f1vhZykwNhgrqaW&earth_date={}".format(rover, param[1]), 'photos')
  else :
    url_to_file = composeURLPhotos('https://api.nasa.gov/mars-photos/api/v1/rovers/{}/latest_photos?api_key=4hvbdm3crmOBYueVE4FJSwRG3f1vhZykwNhgrqaW'.format(rover), 'latest_photos')
  return url_to_file




# Client side of the code

client = commands.Bot(command_prefix = '$')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def imgTest(ctx, arg1, arg2) :
  await ctx.send('You passed {} and {}'.format(arg1, arg2))


'''
$img [roverName] []
sends up to 3 latest random photos of Mars
to server with rover name, camera type, and date taken 
'''
@client.command()
async def img(ctx, *args) :
  url_to_file = verfiyParam(*args)
  if url_to_file == None :
     await ctx.channel.send("No Photos Available")
  else :
       await ctx.channel.send('Here are the latest Photos of Mars!')
       for urls in url_to_file :
         file_name = url_to_file[urls][0]
         urllib.request.urlretrieve(urls, file_name)
         await ctx.channel.send('_ _')
         await ctx.channel.send('Rover ' + url_to_file[urls][1] + ' \|| ' + url_to_file[urls][2] + ' || ' + url_to_file[urls][3])
         await ctx.channel.send(file=discord.File(file_name))
         os.remove(file_name)

''' 
$photo : sends up to 3 latest random photos of Mars
to server with rover name, camera type, and date taken 

@client.command()
async def img(ctx, rover, date) :
   url_to_file = composeURLPhotos('https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key=4hvbdm3crmOBYueVE4FJSwRG3f1vhZykwNhgrqaW', 'latest_photos')
   if url_to_file == None :
     await ctx.channel.send("No Photos Available")
   else :
       await ctx.channel.send('Here are the latest Photos of Mars!')
       for urls in url_to_file :
         file_name = url_to_file[urls][0]
         urllib.request.urlretrieve(urls, file_name)
         await ctx.channel.send('_ _')
         await ctx.channel.send('Rover ' + url_to_file[urls][1] + ' \|| ' + url_to_file[urls][2] + ' || ' + url_to_file[urls][3])
         await ctx.channel.send(file=discord.File(file_name))
         os.remove(file_name)

'''
''' 
$photosDate YYYY-MM-DD : sends up to three random mars
photos from a specified date 
'''
@client.command()
async def photosDate(ctx, date) :
   if bool(datetime.strptime(date, "%Y-%m-%d")) :
    url_to_file = composeURLPhotos("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?api_key=4hvbdm3crmOBYueVE4FJSwRG3f1vhZykwNhgrqaW&earth_date={}".format(date), 'photos')
    if url_to_file == None :
     await ctx.channel.send("No Photos Available")
    else :
        await ctx.channel.send('Here are Mars Photos from '+date+'!')
        for urls in url_to_file :
          file_name = url_to_file[urls][0]
          urllib.request.urlretrieve(urls, file_name)
          await ctx.channel.send('_ _')
          await ctx.channel.send('Rover ' + url_to_file[urls][1] + ' \|| ' + url_to_file[urls][2] + ' || ' + url_to_file[urls][3])
          await ctx.channel.send(file=discord.File(file_name))
          os.remove(file_name)
   else :
     await ctx.channel.send('Please enter a valid date in the following format: YYYY-MM-DD')

client.run(os.getenv('TOKEN'))