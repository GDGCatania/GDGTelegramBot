#!/usr/bin/env python
# -*- coding: utf-8 -*-


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from unidecode import unidecode
import json
import urllib2



# loading token from config file
tokenconf = open('token.conf', 'r').read()
tokenconf = tokenconf.replace("\n", "")
TOKEN = tokenconf

# Enable logging
logging.basicConfig(filename='gdgtgbot.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)

logger = logging.getLogger(__name__)





# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):

	
	bot.sendMessage(update.message.chat_id, text="Start")


def help(bot, update):
	bot.sendMessage(update.message.chat_id, text='Help!')

#/gdg-get ezine (last||num)
def ezine_handle(bot,update):

	logger.info('Serving: %s message: %s\n' % (update.message.from_user.id,update.message.text))
	
	try:

		msg=update.message.text.split(' ')

		base_url='http://gdgcatania.org/gdg-get.php?res=ezine-'
		
		

		if msg[2]=='last':
			url=base_url+"last"
		else:
			url=base_url+msg[2]
	
		logger.info('Connecting to %s\n' % url)

		response = urllib2.urlopen(url)

		resource_url=response.read()

		logger.info('Response is %s\n' % resource_url)

		if  not 'ERROR:' in resource_url:

		
			temp_file='/tmp/%s_%s.pdf'% (resource_url.split('/')[-1].split('.')[0],update.message.from_user.id)
		
			logger.info('Temp file is %s\n' % temp_file)

			logger.info('Downloading %s\n' % resource_url)			

			response = urllib2.urlopen(resource_url)

			with open(temp_file,'w') as f:
				f.write(response.read())
				f.close()
				logger.info('Downloaded %s\n' % temp_file)
	
			with open(temp_file,'r') as f:
				logger.info('Sending to user %s\n' % update.message.from_user.id)
				bot.sendDocument(chat_id=update.message.chat_id,document=f)
				logger.info('%s sendend to %s\n' % (temp_file,update.message.from_user.id))
		else:
			bot.sendMessage(update.message.chat_id, text='Inserisci il comando corretto!')
			logger.info('File not found!')	
		
	except Exception as e:
		logger.exception('Update "%s" caused an error "%s"' % (update,e))


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():

	



	updater = Updater(TOKEN)

	dp = updater.dispatcher


	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))

	dp.add_handler(CommandHandler("gdg-get", ezine_handle))
	



	dp.add_error_handler(error)


	updater.start_polling()

	logger.info('Bot started!')

	updater.idle()


if __name__ == '__main__':
	main()
