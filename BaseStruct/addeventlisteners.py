import importlib, glob, os
from os.path import basename, isfile, dirname

def addListeners(client, MAIN):
    modules = glob.glob("BaseStruct/Listeners/*.py")
    __all__ = [basename(f)[:-3] for f in modules if isfile(f)]

    for toImport in __all__:
        moduleToImport = 'BaseStruct.Listeners.' + toImport
        listener = importlib.import_module(moduleToImport)
        listener.listen(client, MAIN)
