#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from unidecode import unidecode
import json
import urllib2

# Enable logging
logging.basicConfig(filename='bot.log',
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)

logger = logging.getLogger(__name__)

# loading token from config file
logger.info('Loading token from file...')
tokenconf = open('token.conf', 'r').read()
tokenconf = tokenconf.replace("\n", "")
TOKEN = tokenconf

def is_int(s):
	"""Checks if a string is an integer"""
	try: 
		int(s)
		return True
	except ValueError:
		return False

def download_file(bot, update, url):
	"""Downloads a file from a given URL"""
	try:
		logger.info('Connecting to %s\n' % url)

		response = urllib2.urlopen(url)
		resource_url=response.read()

		logger.info('Response is %s\n' % resource_url)

		if  not 'ERROR:' in resource_url:
			filename = resource_url.split('/')[-1].split('.')[0]
			extension = resource_url.split('/')[-1].split('.')[-1]
			tmp_filename='/tmp/%s_%s.%s'% (filename,
										update.message.from_user.id, 
										extension)
		
			logger.info('Temp file is %s\n' % tmp_filename)
			logger.info('Downloading %s\n' % resource_url)			

			response = urllib2.urlopen(resource_url)

			with open(tmp_filename,'w') as file:
				file.write(response.read())
				file.close()
				logger.info('Downloaded %s\n' % tmp_filename)
	
			with open(tmp_filename,'r') as file:
				logger.info('Sending to user %s\n' % update.message.from_user.id)
				bot.sendDocument(chat_id = update.message.chat_id, document = file)
				logger.info('%s sendend to %s\n' % (tmp_filename, update.message.from_user.id))
		else:
			bot.sendMessage(update.message.chat_id, text=resource_url.split(':')[-1])
			logger.info('File not found!')	
		
	except Exception as e:
		logger.exception('Update "%s" caused an error "%s"' % (update,e))

def start_handle(bot, update):
	"""Return a welcome message to the user"""
	bot.sendMessage(update.message.chat_id, text=
		"Hello and Welcome to the GDGCatania's Bot!\n" \
		"Type /help for more")

def help_handle(bot, update):
	"""Return a list of instruction on how to use the bot"""
	help = 'Hello! This is the GDG Bot :) \n\n'\
			'The available commands are: \n'\
			'/gdg-get ezine [last | number]'
	bot.sendMessage(update.message.chat_id, text=help)

def ezine(bot, update, tokens):
	"""Downloads an issue of the ezine on behalf of the user"""
	if len(tokens) == 1:
		if is_int(tokens[0]) or tokens[0] == 'last':
			issue = tokens[0]
		elif tokens[0] != 'last':
			bot.sendMessage(update.message.chat_id, 
				text='The ezine command takes either \'last\' or a number as parameters')
			logger.info('Wrong parameters for the ezine command')	
	
	elif len(tokens) == 0 or len(tokens) > 1:
		bot.sendMessage(update.message.chat_id,
							text='The ezine command allows you to download all our ezines.'\
							' Just append \'last\' or the issue number to the command')
		logger.info('Wrong number of commands for the ezine command')	

	base_url='http://gdgcatania.org/gdg-get.php?res=ezine-'	
	url = base_url + issue

	download_file(bot, update, url)

# Sub-commands for /gdg-get
gdg_get_options = {
	'ezine' : ezine
}

def gdg_get_handle(bot, update):
	"""Handles all gdg-get requests that take the form /gdg-get COMMAND [params]"""
	logger.info('Serving: %s message: %s\n' % (update.message.from_user.id, update.message.text))
	
	tokens = update.message.text.lower().split(' ')

	if len(tokens) >= 2 and tokens[1] in gdg_get_options:
		gdg_get_options[tokens[1]](bot, update, tokens[2:])
	else:
		commands = ""
		for key, value in gdg_get_options.iteritems():
			commands += '-' + key + '\n'

		output = 'The /gdg-get command takes the following commands: \n' + commands
		bot.sendMessage(update.message.chat_id, 
				text=output)

def error_handle(bot, update, error):
	"""Handle errors"""
	logger.warn('Update "%s" caused error "%s"' % (update, error))

# Top level commands for the bot
START_CMD = "start"
HELP_CMD = "help"
GDG_GET_CMD = "gdg-get"

def main():
	logger.info('Starting Bot!')
	updater = Updater(TOKEN)

	dp = updater.dispatcher

	dp.add_handler(CommandHandler(START_CMD, start_handle))
	dp.add_handler(CommandHandler(HELP_CMD, help_handle))
	dp.add_handler(CommandHandler(GDG_GET_CMD, gdg_get_handle))
	dp.add_error_handler(error_handle)

	updater.start_polling()
	logger.info('Bot started!')

	updater.idle()

if __name__ == '__main__':
	main()
