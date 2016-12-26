#Internal imports
from plugin_handler import subscribe
import logging

#External imports
import wolframalpha

log = logging.getLogger()

def search_wolfam():
    pass
    #TODO: use dataset to search the db for the wolfram api key

def is_search(event):
    '''Determine whether it's a search command'''
    command = event["command"]
    if "search" in event["verbs"]:
        return True
    question_words = [
        "what",
        "when",
        "why",
        "how",
        "who",
        "are",
        "is"
    ]
    first_word = command.split(" ").lower()
    log.debug("First word in command is {0}".format(first_word))
    if first_word in question_words:
        return True
    return False

@subscribe({"name":"search", "check":is_search})
def main(query):
    '''Start the search'''
    log.info("In main search function with query {0}".format(query))