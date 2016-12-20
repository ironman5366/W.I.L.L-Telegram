#Builtin imports
import logging
#External imports
import dataset
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, Job)

#Internal imports

log = logging.getLogger()

events = {}

help_str = '''
Commands:
/help: Print this string
/start: Start the bot and create a userdata table with your username
/settings: Change user settings
If not given a telegram command, W.I.L.L will yry to interperet your command as a personal assistant
'''

db = dataset.connect('sqlite://will.db')

def help(bot, update):
    update.message.reply_text(help_str)


def start(bot,update):
    '''First run commands'''
    log.info("Setting up bot")
    userdata = db['userdata']
    admin = bot.getMe()
    admin_username = admin.username
    log.info("Admin user is {0}, admin username is {1}".format(
        admin, admin_username
    ))
    username = update.from_user.username
    first_name = update.from_user.first_name
    user_is_admin = username == admin_username
    log.info("User data is as follows: username is {0}, first_name is {1}, user_is_admin is {2}".format(
        username,first_name,user_is_admin
    ))
    userdata.insert(dict(
        first_name=update.from_user.first_name,
        username=update.from_user.username,
        admin=user_is_admin
    ))


def error(bot, update, error):
    log.warn('Update "%s" caused error "%s"' % (update, error))

def parse(bot, update):
    pass
def initialize(bot_token):
    updater = Updater(bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, parse))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()