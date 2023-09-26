#!/bin/python3
# -*- coding: utf-8 -*-
#
# hugchat-bot.py - by:proxlu

from hugchat import hugchat
from hugchat.login import Login
import subprocess
import discord

# Carregamento
intents = discord.Intents.default()
intents.messages = True  # Habilita a intenção de mensagens de guilda
client = discord.Client(intents=intents)

# Faz login no huggingface
sign = Login('EMAIL_AQUI', 'SENHA_AQUI')

# Cria um chatbot
chatbot = hugchat.ChatBot(sign.login())

# Bot
@client.event
async def on_message(message):
	if message.author == client.user:
		return

	canal = message.channel
	texto = message.clean_content

	# Verifica se o bot foi mencionado
	bot_mention = f"<@{client.user.id}>"
	if bot_mention in texto:
		texto = texto.replace(bot_mention, "").strip()  # Remove a menção ao bot

	# Solicita api
	if texto.strip():
		saida_da_api = chatbot.chat(texto)

		# Comando a ser executado no terminal usando subprocess
		comando = ['trans', '-b', saida_da_api]
		saida = subprocess.check_output(comando, stderr=subprocess.DEVNULL)
		saida_decodificada = saida.decode('utf-8')
		saida_corrigida = saida_decodificada.replace('u003d', '=')

		# Recebe a mensagem do usuário
		await canal.send(saida_corrigida)

		# Cria nova conversa para descartar a atual
		id = chatbot.new_conversation()
		chatbot.change_conversation(id)

client.run('TOKEN_AQUI')
