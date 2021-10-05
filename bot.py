import discord
import random

TOKEN = 'ODk0ODkzNDM0MTMxODQxMDM1.YVwodQ.aRq8_dFxle6fdkc_TnmqTXqt_Zc'

client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	username = str(message.author).split('#')[0]
	user_message = str(message.content)
	channel = str(message.channel.name)
	print(f'{username}: {user_message}({channel})')

	if message.author == client.user:
		return

	if user_message.lower() == 'i have a question':
		await message.channel.send(f'Sure {username}, go ahead')
		return
	elif user_message.lower() == 'hello':
		await message.channel.send(f'Hi {username}!')
		return
	elif user_message.lower() == 'what is the capital of france?':
		await message.channel.send(f'Paris')
		return

client.run(TOKEN)