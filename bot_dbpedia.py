#!/usr/bin/env python

import discord
import random
import asyncio

import transformers
from transformers import pipeline
import re

import requests
import json

TOKEN = 'OTA4MDIyNzE0OTg2NTMyOTY0.YYvsDQ.-v1Sg_-y7hFmFS_qu2X7YzTIKD4'

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

			if "** " in topic.content:
				head, sep, tail = topic.content.partition('** ')
				topic.content = tail
			dash_topic = topic.content.title()
			dash_topic = dash_topic.replace(" ", "_")
			u = "http://dbpedia.org/data/{}.json".format(dash_topic)
			data = requests.get(u)
			json_data = json.loads(data.content)

			try:
				if 'http://dbpedia.org/ontology/abstract' not in json_data["http://dbpedia.org/resource/{}".format(dash_topic)]:
					try:
						if json_data["http://dbpedia.org/resource/{}".format(dash_topic)]['http://dbpedia.org/ontology/wikiPageRedirects']:
							link = 	[link['value'] for link in json_data["http://dbpedia.org/resource/{}".format(dash_topic)]['http://dbpedia.org/ontology/wikiPageRedirects']]
							print(link)
							dash_topic = link[0]
							dash_topic = dash_topic.split('dbpedia.org/resource/', 1)[1]
							u = "http://dbpedia.org/data/{}.json".format(dash_topic)
							data = requests.get(u)
							json_data = json.loads(data.content)
					except Exception as error:
						lookup_url = "https://lookup.dbpedia.org/api/search?maxResults=10&format=JSON&query={}".format(topic.content)
						lookup_page = requests.get(lookup_url, verify=False)
						lookup_data = json.loads(lookup_page.content)
						lookup_data = lookup_data['docs']
						lookup_data = lookup_data[0]['resource'][0]
						dash_topic = lookup_data.split('dbpedia.org/resource/', 1)[1]
						u = "http://dbpedia.org/data/{}.json".format(dash_topic)
						data = requests.get(u)
						json_data = json.loads(data.content)
			except KeyError as error:
				lookup_url = "https://lookup.dbpedia.org/api/search?maxResults=10&format=JSON&query={}".format(topic.content)
				lookup_page = requests.get(lookup_url, verify=False)
				lookup_data = json.loads(lookup_page.content)
				lookup_data = lookup_data['docs']
				print(lookup_data)
				lookup_data = lookup_data[0]['resource'][0]
				print(lookup_data)
				dash_topic = lookup_data.split('dbpedia.org/resource/', 1)[1]
				u = "http://dbpedia.org/data/{}.json".format(dash_topic)
				data = requests.get(u)
				json_data = json.loads(data.content)

			if not json_data:
				return await message.channel.send(f'I am sorry, I do not know much about {topic.content}')

			await message.channel.send(f'What would you like to know about {topic.content}?')

			try:
				question = await self.wait_for('message', timeout=15.0)
				if "** " in question.content:
					head, sep, tail = question.content.partition('** ')
					question.content = tail
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