import importlib, glob, os, sys
from os.path import basename, isfile, dirname

def add_event_listeners(client, instance, whitelist=[], blacklist=[]):
    """adds all event listeners found in the "EventListeners"
        dir and adds them to the bot"""

    modules = glob.glob("EventListeners/*.py")
    __all__ = [basename(f)[:-3] for f in modules if isfile(f)]

    for toImport in __all__:
        if not (whitelist and toImport not in whitelist) and (toImport not in blacklist):
            print('---Adding listener: {}'.format(toImport))
            moduleToImport = 'EventListeners.' + toImport
            listener = importlib.import_module(moduleToImport)
            listener.listen(client, instance)
