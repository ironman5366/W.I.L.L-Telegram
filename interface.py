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
If not given a telegram command, W.I.L.L will try to interpret your command as a personal assistant
'''

db = dataset.connect('sqlite://will.db')

def help(bot, update):
    update.message.reply_text(help_str)

def alarm(bot, job):
    """Function to send the alarm message"""
    bot.sendMessage(job.context, text=)
    #TODO: find out what's in job.context to send a custom message

def set_job(bot, update, args, job_queue, chat_data, response_text, alarm_text):
    '''Adds a job to the job queue'''
    chat_id = update.message.chat_id
    #Time for the timer in seconds
    due = int(args[0])
    job = Job(alarm, due, repeat=False, context=chat_id)
    chat_data['job'] = job
    chat_data["alarm_text"] = alarm_text
    job_queue.put(job)
    update.message.reply_text(response_text)

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
    chat_id = update.message.chat_id
    user_is_admin = username == admin_username
    log.info("User data is as follows: username is {0}, first_name is {1}, user_is_admin is {2}, chat_id is {3}".format(
        username,first_name,user_is_admin, chat_id
    ))
    userdata.insert(dict(
        first_name=update.from_user.first_name,
        username=update.from_user.username,
        admin=user_is_admin
    ))


def error(bot, update, error):
    log.warn('Update "%s" caused error "%s"' % (update, error))

def parse(bot, update, args,job_queue, chat_data, response_text, alarm_text):
    pass

def initialize(bot_token):
    updater = Updater(bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(
        Filters.text, parse, pass_args=True, pass_job_queue=True,pass_chat_data=True
    ))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()