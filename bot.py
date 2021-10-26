import discord
import random

import transformers
from transformers import pipeline

TOKEN = 'ODk0ODkzNDM0MTMxODQxMDM1.YVwodQ.IQtlTUT-tPXWbX5LuWQegULbqWk'

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
	else:
		nlp = pipeline("question-answering", model = 'distilbert-base-cased-distilled-squad')
		with open('train.txt', encoding="utf8") as file:
			context = file.read()
		await message.channel.send(nlp(question=user_message.lower(), context=context)['answer'])
		return

	# elif user_message.lower() == 'hello':
	# 	await message.channel.send(f'Hi {username}!')
	# 	return
	# elif user_message.lower() == 'who developed league of legends?':
	# 	await message.channel.send(f'Riot games')
	# elif user_message.lower() == 'how many people play fifa?':
	# 	await message.channel.send(f'25 milion')
	# 	return

client.run(TOKEN)