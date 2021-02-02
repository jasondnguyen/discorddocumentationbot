import os
from pymongo import MongoClient
import discord
from dotenv import load_dotenv
from pprint import pprint


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
MONGO = os.getenv('MONGODBDOC')

intents = discord.Intents.all()
client = discord.Client(intents=intents)


class Connect(object):
    @staticmethod
    def get_connection():
        return MongoClient(MONGO)


connection = Connect.get_connection()
db = connection.DocLookup


def embed_text(query, response):
    '''
    Embeds the query and response as
    title and description
    '''
    embed = discord.Embed(color=0x4B8BBE)
    embed.title = f'{query}'
    embed.description = response
    return embed


@ client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('!python'):
        split_message = message.content.split()
        query = ' '.join(message.content.strip().split()[1:])
        response = db.Python.find({"name": f'{query}'})
        for item in response:
            if len(item['info']) > 2048:
                first_split = len(item['info'])//2
                embed = embed_text(item['name'], item['info'][:first_split])
                await message.channel.send(embed=embed)
                embed = embed_text('', item['info'][first_split:])
                await message.channel.send(embed=embed)
            else:
                embed = embed_text(item['name'], item['info'])
                await message.channel.send(embed=embed)
    elif message.content.lower().startswith('!javascript'):
        split_message = message.content.split()
        query = ' '.join(message.content.strip().split()[1:])
        response = db.JavaScript.find({"name": f'{query}'})
        for item in response:
            if len(item['info']) > 2048:
                first_split = len(item['info'])//2
                embed = embed_text(item['name'], item['info'][:first_split])
                await message.channel.send(embed=embed)
                embed = embed_text('', item['info'][first_split:])
                await message.channel.send(embed=embed)
            else:
                embed = embed_text(item['name'], item['info'])
                await message.channel.send(embed=embed)

client.run(TOKEN)
