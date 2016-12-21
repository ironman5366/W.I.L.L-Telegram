#Builtin imports
import logging
import os
import sys
import time
import threading

#External imports
import importlib
from Queue import Queue
import dataset

#Internal imports
import main
import interface

log = logging.getLogger()

dir_path = 'plugins'

plugin_subscriptions = []

events_queue = Queue()

db = dataset.connect('sqlite://will.db')

user_table = db['userdata']

class subscriptions():
    '''Manage plugin subscriptions and events'''
    def check_requirements(self, plugin, event):
        '''Check if the event meets the requirments that the event sets'''
        if "requirements" not in plugin.keys():
            return True
        plugin_requirements = plugin["required"]
        required_categories = plugin_requirements.keys()
        #Try to find if the db table for that category exists
        log.info("Finding db tables for categories {0}".format(required_categories))
        requirements_found = {}
        for category in required_categories:
            #Check if user has column for this kind of data in their database
            if category in user_table.columns:
                log.debug("Found category {0} in database for user {1}".format(
                    category, user_table["first_name"]
                ))
                found_category = user_table[category]
                category_data_type = type(found_category)
                if category_data_type == dict:
                    requirements_found.update({
                        category: found_category[
                            plugin_requirements[category]
                        ]
                    })
                else:
                    if plugin_requirements[category]:
                        if plugin_requirements[category] != user_table[category]:
                            return False
                    requirements_found.udpate({
                        category: plugin_requirements[category]
                    })
            else:
                log.error("Category {0} wasn't found for user {1}".format(
                    category, user_table["first_name"]
                ))
        return requirements_found



    def subscriptions_thread(self):
        '''The seperate thread that monitors the events queue'''
        log.info("In subscriptions thread, starting loop")
        while True:
            time.sleep(0.1)
            #If the queue is empty, pass
            if not events_queue.empty():
                event = events_queue.get()
                assert type(event) == dict
                event_command = event["command"]
                username = event['update'].from_user.username
                log.info("Processing event with command {0}, user {1}".format(
                    event_command, username))
                user_table = db.find_one(username=username)
                if event_command == "shutdown":
                    #If the thread tells to shut down, make sure the user is admin
                    if user_table['admin']:
                        log.info("Shutting down the subscriptions thread")
                        main.shutdown()
                        break
                else:
                    #Iterate through plugin descriptions and determine if they should be run
                    found_plugin = None
                    for plugin in plugin_subscriptions:
                        log.debug("Parsing plugin {0}".format(plugin))
                        required_check = self.check_requirements(plugin, event)
                        if not required_check:
                            continue
                        if "required_data" in event.keys():
                            event["required_data"] = required_check
                        else:
                            event.update({"required_data": required_check})
                        if "command" in plugin.keys():
                            #If the plugin calls for the exact command passed
                            if plugin["command"].lower() == event_command.lower():
                                log.info("Plugin {0} calls for exact command {1}, calling plugin".format(
                                    plugin, event_command
                                ))
                                found_plugin = plugin
                                break
                            #If the plugin is correct, call it with all the data
                        if "verbs" in plugin.keys():
                            plugin_verbs = set(plugin["verbs"])
                            verb_check = event['verbs'].issuperset(plugin_verbs)
                            if verb_check:
                                found_plugin = plugin
                                break
                    if not found_plugin:
                        pass
                        #TODO: specify search plugin
                    try:
                        log.info("Calling appropriate function")
                        response = found_plugin["function"](event)
                    except Exception as e:
                        log.info("Error {0}, {1} occurred while calling plugin {2}".format(
                                e.message,e.args, found_plugin
                            ))
                        log.info("Response is {0}".format(response))
                        bot = event["bot"]
                        chat_id = event["chat_data"]["chat_id"]
                        if not response:
                            response = "Done"
                        interface.send_message(bot,chat_id,response)

    def send_event(self, event):
        '''Take incoming event'''
        assert(type(event) == "dict")
        assert "comamnd" in event.keys()
        command = event["command"]
        log.info("Putting event for command {0} in event queue".format(
            command
        ))
        events_queue.put(event)
    def initialize(self):
        '''Start the subscriptions thread'''
        log.info("Starting plugin subscription monitoring thread")
        s_thread = threading.Thread(target=self.subscriptions_thread)
        s_thread.start()
        log.info("Started subscriptions thread")

def process_plugins(path):
    '''Process and import the plugins'''
    log.info("Processing plugin {0}".format(path))
    python_loader = PythonLoader(path)
    try:
        python_loader.load()
    except IOError:
        return

def subscribe(subscription_data):
    '''Wrapper for adding plugins to my event system'''
    assert(type(subscription_data) == dict)
    def wrap(f):
        log.info("Subscribing function {0} to data {1}".format(
            f, subscription_data
        ))
        plugin_subscriptions.append(subscription_data.update({
            'function': f
        }))
    return wrap

def load(dir_path):
    '''Loads plugins'''
    log.info("Finding plugins in directory {0}".format(dir_path))
    plugins = lambda: (os.path.join(dir_path, module_path)
                       for module_path in os.listdir(dir_path))
    map_plugins(plugins())
    log.info("Finished parsing and loading plugins, processing subscriptions")
    subscriptions.initialize()
    log.info("Plugin initialization finished")

def map_plugins(plugin_paths):
    log.info("Mapping plugins to processing function")
    map(lambda plugin: process_plugins(plugin), plugin_paths)

class PythonLoader:
    '''The class that loads the plugins'''

    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        if self.is_plugin():
            log.info("Loading plugin: {0}".format(self.file_path))
            self.update_path()
            importlib.import_module(self.import_name())

    def is_plugin(self, fs_tools=os.path):
        if fs_tools.exists(self.file_path):
            if fs_tools.isfile(self.file_path) and \
                    self.file_path.endswith('.py'):
                return True
            if fs_tools.isdir(self.file_path):
                init_file = os.path.join(self.file_path, "__init__.py")
                if fs_tools.exists(init_file) and fs_tools.isfile(init_file):
                    return True
        return False

    def import_name(self):
        if self.file_path.endswith('.py'):
            return os.path.basename(self.file_path).split('.')[0]
        else:
            return os.path.basename(self.file_path)

    def update_path(self):
        lib_path = self._lib_path()
        if lib_path not in sys.path:
            sys.path.append(lib_path)

    def _lib_path(self):
        return os.path.normpath(
            os.sep.join(os.path.normpath(self.file_path).split(os.sep)[:-1])
        )



