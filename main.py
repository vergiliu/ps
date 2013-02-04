import logging
import sys
from src.ParseArguments import ParseArguments

def setupGlobalLogger():
    """abc def"""
    #theLoggingHandler = logging.StreamHandler()
    #theLoggingFormatter = theLoggingHandler.setFormatter("%(asctime)s %(levelname)s:%(message)s") #,datefmt="%H:%M:%S")
    #theLogger = logging.getLogger('root')
    #theLogger.setLevel(logging.DEBUG)
    #theLogger.addHandler(theLoggingHandler)

    formatter = logging.Formatter(fmt="%(asctime)s %(module)-20s %(levelname)s: %(message)s", datefmt="%d-%m %H:%M:%S")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

if __name__ == "__main__":
    setupGlobalLogger()
    myArguments = ParseArguments(sys.argv)
    myArguments.getVariable()
