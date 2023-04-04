from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
from discord.ext import commands
import os
import time
from bs4 import BeautifulSoup
import requests
from discord.ext import tasks

load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

bot = commands.Bot(command_prefix = PREFIX,intents=discord.Intents.all())

marker = 30
url = "https://quasarzone.com/bbs/qb_saleinfo?page=1"
dUrl = 'https://quasarzone.com'

previous_top = ''
channel = ''

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}.')

@bot.command()
async def init(ctx):
    global channel, previous_top
    channel = ctx.channel
    init_response = requests.get(url)
    if init_response.status_code == 200:
        html = init_response.text
        soup = BeautifulSoup(html, 'html.parser')
        imgs = soup.select('.maxImg')
        info_price = soup.select('.text-orange')
        info_category = soup.select('.category')
        info_title = soup.select('.ellipsis-with-reply-cnt')
        info_link = soup.select('.subject-link')

        current_top = str(info_link[2]['href'])
        if previous_top != current_top:
            for k in range(2, len(info_link)):
                if info_link[k]['href'] == previous_top:
                    marker = k-2
                    break
        
            for i in range(0, marker):
                s = [""]
                s.append(info_category[i].contents[0])
                s.append('\n')
                s.append(info_price[i].contents[0])
                s.append('\n')
                s.append(dUrl + info_link[i+2]['href'])
                embed = discord.Embed(title = info_title[i].contents[0])
                embed.set_image(imgs[i]["src"])
                await channel.send(embed=embed)
            
            previous_top = current_top
        else :
            print("nothing to update")
    else : 
        print(init_response.status_code)
    
        
    

try:
    bot.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")