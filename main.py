# libraries! 
import discord
from discord.ext import commands
import random 
import os
import requests
import json
from datetime import datetime
import urllib.request
from webscraper import *

# default limit values for sending photos and articles
ARTICLE_COUNT = 5
PHOTO_COUNT = 3

# Chooses three random photos 
# from the plethora of photos taken from mars 
# rovers on a given date. If there are less than three 
# photos, then it sends what is available.
# @Returns a dictionary with the structure
# key           value 
# [photo URL] : [file name, Rover, Camera type, date taken] 
def composeURLPhotos(apiCall, photoType) :
  photo_data = json.loads(requests.get(apiCall).text)
  url_to_file = {}
  if len(photo_data[photoType]) == 0 :
    return None
  else :
    # Chooses 3 random photos from api call
    for photos in random.sample(range(0, len(photo_data[photoType])), (int) (PHOTO_COUNT)) :
      url = photo_data[photoType][photos]["img_src"]
      file_name = url.split("/")[-1:][0]
      rover = photo_data[photoType][photos]["rover"]["name"]
      camera = photo_data[photoType][photos]["camera"]["full_name"]
      date_taken = photo_data[photoType][photos]["earth_date"]
      url_to_file[url] = [file_name, rover, camera, date_taken]
  return url_to_file


# From the user response, mutates the passed list informing
# user of incorrect formating of bot commands. Additionaly, 
# creates api call based on cdiscord command.
# @Returns a dictionary described by composeURLPhotos()
def verfiyParam(param, informUser) :
  rover = "perseverance"
  dateFormat = True
  # informs user of any invalid command structure
  if len(param) == 0 :
    informUser.append("No args specified, defaulted to Perseverance and latest photos.")
  if len(param) >= 1 :
    if param[0].lower() != "perseverance" and param[0].lower() != "curiosity" :
      informUser.append("No active rover specified, defaulted to Perseverance.")
  if len(param) >= 2 :
    try :
      bool(datetime.strptime(param[1], "%Y-%m-%d"))
    except ValueError :
      dateFormat = False
      informUser.append("Invalid date Format. Enter as YYYY-MM-DD. Defaulted to latest photos.")
  # creates api calls based on commands
  url_to_file = {}
  if len(param) > 0 and param[0].lower() == "curiosity" :
    rover = 'curiosity'
  if len(param) > 1 and dateFormat :
    url_to_file = composeURLPhotos("https://api.nasa.gov/mars-photos/api/v1/rovers/{}/photos?api_key=4hvbdm3crmOBYueVE4FJSwRG3f1vhZykwNhgrqaW&earth_date={}".format(rover, param[1]), 'photos')
  else :
    url_to_file = composeURLPhotos('https://api.nasa.gov/mars-photos/api/v1/rovers/{}/latest_photos?api_key=4hvbdm3crmOBYueVE4FJSwRG3f1vhZykwNhgrqaW'.format(rover), 'latest_photos')
  return url_to_file

# Client side of the code

client = commands.Bot(command_prefix = '$')
client.remove_command('help')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# changes article limit to send to user
# command:
# $articleCount [number]
@client.command()
async def articleCount(ctx, count) :
  global ARTICLE_COUNT 
  ARTICLE_COUNT = count
  await ctx.channel.send("Article limit for $articles calls are now {}!".format(count)) 

# changes article limit to send to user
# command:
# $imgCount [number]
@client.command()
async def imgCount(ctx, count) :
  global PHOTO_COUNT
  PHOTO_COUNT = count
  await ctx.channel.send("Photo limit for $img calls are now {}!".format(count))

# Sends user list of valid commands
# command: $help
@client.command()
async def help(ctx) :
  await ctx.channel.send('List of Commands!')
  await ctx.channel.send('**$img** --- Sends latest photos from perseverance rover')
  await ctx.channel.send('**$imgCount [number]** --- Whens using $img, changes amount of photos sent by desired value')
  await ctx.channel.send('**$img perseverance** --- same functionality as above')
  await ctx.channel.send('**$img curiosity** --- sends latest photos from curiosity rover')
  await ctx.channel.send('**$img perseverance YYYY-MM-DD** --- sends photos from perseverance rover on specified date')
  await ctx.channel.send('**$img curiosity YYYY-MM-DD** --- sends photos from curiosity rover on specified date')
  await ctx.channel.send('**$articles [page number]** --- Sends mars articles from a desired page on google news')
  await ctx.channel.send('**$articleCount [number]** --- Whens using $article [page number], changes amount of articles sent by desired value')

# Sends up to three terrain photos of Mars. Users can change 
# amount of photos being sent using $imgCount [number]
# Users can query based on rover (perseverance, curiosity)
# and date.
# Commands:
# $img
# $img [roverName]
# $img [roverName] [date] 
@client.command()
async def img(ctx, *args) :
  # parses through args attached with user command
  params = []
  informUser = []
  for arg in args :
    params.append(arg)
    if len(params) == 2 : 
      break
  url_to_file = verfiyParam(params, informUser)
  # notifies user of any invalid formatting 
  for complaints in informUser :
    await ctx.channel.send(complaints)
  # sends terrain photos to user
  if url_to_file == None :
     await ctx.channel.send("No Photos Available")
  else :
       await ctx.channel.send('Here are some terrain images of Mars!')
       for urls in url_to_file :
         file_name = url_to_file[urls][0]
         urllib.request.urlretrieve(urls, file_name)
         await ctx.channel.send('_ _')
         await ctx.channel.send('Rover ' + url_to_file[urls][1] + ' \|| ' + url_to_file[urls][2] + ' || ' + url_to_file[urls][3])
         await ctx.channel.send(file=discord.File(file_name))
         os.remove(file_name)

# webscraping feature allows articles to be pulled from google 
# using the search term "mars"
# users can change the amount of articles to be sent from a page
# using $articleCount [page number]
# Commands:
# $articles [page number]
@client.command()
async def articles(ctx, pageNumber) :
  # readjusts invalid page requests  
  if int(pageNumber) < 1 :
    await ctx.channel.send('Sent a number less than one, defaulted to first page.')
    await ctx.channel.send('_ _')
    pageNumber = '1'
  elif int(pageNumber) > 10 :
    await ctx.channel.send('Sent a number Greater than 10, defaulted to 10th page.')
    await ctx.channel.send('_ _')
    pageNumber = '10'
  
  # assembles list of articles from desired page
  articles = MarsArticles(int(pageNumber), (int) (ARTICLE_COUNT))
  list_of_articles = articles.getArticles()
  await ctx.channel.send('Here are the articles from page ' + pageNumber + ".")
  await ctx.channel.send('_ _')

  for articles in list_of_articles :
    await ctx.channel.send(articles)
    await ctx.channel.send('_ _')
client.run(json.load(open('config.json'))["token"])