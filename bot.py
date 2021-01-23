import os

import discord
from dotenv import load_dotenv
import webscraper

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)


def embed_text(query, response):
    '''
    Embeds the query and response as 
    title and description
    '''
    embed = discord.Embed(color=0x4B8BBE)
    embed.title = f'{query}'
    embed.description = response
    return embed


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('!python'):
        split_message = message.content.split()
        query = ' '.join(message.content.strip().split()[1:])
        response = webscraper.python_lookup()
        if len(response) > 2048:
            first_split = len(response)//2
            embed = embed_text(query, response[:first_split])
            await message.channel.send(embed=embed)
            embed = embed_text('', response[first_split:])
            await message.channel.send(embed=embed)
        else:
            embed = embed_text(query, response)
            await message.channel.send(embed=embed)

client.run(TOKEN)
