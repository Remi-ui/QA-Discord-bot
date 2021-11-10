import discord
import random
import asyncio

import transformers
from transformers import pipeline
import re

import requests
import json

TOKEN = 'ODk0ODkzNDM0MTMxODQxMDM1.YVwodQ.JwMwZxcWWUe6523Yg5ak15dCCtI'

client = discord.Client()

class MyClient(discord.Client):
	@client.event
	async def on_ready(self):
		print('We have logged in as {0.user}'.format(client))

	@client.event
	async def on_message(self, message):
		username = str(message.author).split('#')[0]
		user_message = str(message.content)
		channel = str(message.channel.name)
		print(f'{username}: {user_message}({channel})')

		if message.author.id == self.user.id:
			return

		if 'hi quan' in user_message.lower():
			await message.channel.send(f'Hi {username}, what would you like to know something about?')
			
			try:
				topic = await self.wait_for('message', timeout=10.0)
			except asyncio.TimeoutError:
				return await message.channel.send(f'Sorry I did not get that')

			head, sep, tail = topic.content.partition('** ')
			topic.content = tail
			dash_topic = topic.content.replace(" ", "_")
			u = "http://dbpedia.org/data/{}.json".format(dash_topic)
			data = requests.get(u)
			json_data = json.loads(data.content)

			if not json_data:
				return await message.channel.send(f'I am sorry, I do not know much about {topic.content}')

			await message.channel.send(f'What would you like to know about {topic.content}?')

			try:
				question = await self.wait_for('message', timeout=15.0)
				head, sep, tail = question.content.partition('** ')
				question.content = tail
				print(question.content)
			except asyncio.TimeoutError:
				return await message.channel.send(f'Sorry I did not get that')

			nlp = pipeline("question-answering", model = 'distilbert-base-cased-distilled-squad')

			for j in json_data["http://dbpedia.org/resource/{}".format(dash_topic)]:
				if(j == "http://dbpedia.org/ontology/abstract"):
					context = [abstract['value'] for abstract in json_data["http://dbpedia.org/resource/{}".format(dash_topic)]["http://dbpedia.org/ontology/abstract"] if abstract['lang'] == 'en'][0]

			await message.channel.send(nlp(question=question.content.lower(), context=context)['answer'])

			try:
				source_msg = await self.wait_for('message', timeout=10.0)
				if source_msg.content.lower() == '!source':
					return await message.channel.send(f'I got this information from: http://dbpedia.org/resource/{dash_topic}')
			except asyncio.TimeoutError:
				return

			return

client = MyClient()

client.run(TOKEN)