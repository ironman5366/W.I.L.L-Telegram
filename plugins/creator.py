from plugin_handler import subscribe
def is_creator(event):
    is_c = False
    is_c = "who is your creator" in event["command"]
    is_c = "who are you" in event["command"]
    is_c = "What are you?" in event["command"]
    is_c = "creator" in event["command"]
@subscribe({"name": "creator", "check":is_creator})
def say_name(event):
    return "I am W.I.L.L, and I am made my Will. We are one. "