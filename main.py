import discord
import validators
import requests
import json
import aiohttp
import io

async def get_image_at_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise RuntimeError()
            data = io.BytesIO(await resp.read())
            return data

data = json.load(open('local.settings.json'))
loginToken = data['LoginToken']

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    valid_file_extensions = ['png', 'jpg', 'jpeg', 'gif']

    if validators.url(message.content) and 'imgur.com' in message.content and message.content.split('.')[-1] in valid_file_extensions:
        data = await get_image_at_url(message.content)
        await message.channel.send(file=discord.File(data, 'hermes_image.png'), content=f'Sent by {message.author.name}')
        await message.delete()

    if '$hello' in message.content:
        await message.channel.send('Hello!')

client.run(loginToken)


# https://discord.com/api/oauth2/authorize?client_id=1044557030029000714&permissions=8589995008&scope=bot