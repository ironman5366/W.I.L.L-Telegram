#Builtin imports
from logging import log
#Internal imports
from plugin_handler import subscribe
#External imports
import dataset

db = dataset.connect('sqlite://will.db')

@subscribe({"name":"shutdown", "keywords": ["shutdown"], "requirements": {"db":[lambda userdata: userdata["admin"]]}})
def shutdown(command_data):
    '''Shutdown W.I.L.Ls services'''
    log.info("Shutting down W.I.L.L")
    log.debug("Command data is {0}".format(
        command_data
    ))
    #Verify user is admin again for security
    update = command_data["update"]
    username = update.from_user.username
    userdata = db["userdata"]
    user_table = userdata.find_one(username=username)
    log.debug("Userdata table for user {0} is {1}".format(
        username, user_table
    ))
    if user_table["user_is_admin"]:
        pass
        #TODO: shutdown events