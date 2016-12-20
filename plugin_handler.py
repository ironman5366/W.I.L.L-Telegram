#Internal imports
import logging
import os
import sys
import time

#External imports
import importlib
from Queue import Queue

log = logging.getLogger()

dir_path = 'plugins'

plugin_subscriptions = []

events_queue = Queue()

class subscriptions():
    '''Manage plugin subscriptions and events'''
    def subscriptions_thread(self):
        while True:
            time.sleep(0.1)
            event = events_queue.get()
            if event == "shutdown":
                break
            else:
                pass
            #TODO: process event
    def send_event(self, event):
        '''Take incoming event'''
        assert(type(event) == "dict")
        pass
    def initialize(self):

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



