import importlib, glob, os
from os.path import basename, isfile, dirname

def add_event_listeners(client, instance, whitelist=[], blacklist=[]):
    modules = glob.glob("BaseStruct/EventListeners/*.py")
    __all__ = [basename(f)[:-3] for f in modules if isfile(f)]

    for toImport in __all__:
        if not (whitelist and toImport not in whitelist) and (toImport not in blacklist):
            print('---Adding listener: {}'.format(toImport))    
            moduleToImport = 'BaseStruct.EventListeners.' + toImport
            listener = importlib.import_module(moduleToImport)
            listener.listen(client, instance)
