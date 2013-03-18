import getopt
import logging

__module__ = 'src'
__name__ = 'ParseArguments'
logger = logging.getLogger("main")

class ParseArguments:
    """Parse command line arguments, at least one parameter is needed"""

    def __init__(self, aParamsArray):
        """init"""
#        logger.debug(aParamsArray)
        self.thePortNumber = 45678
        self.theHostName = 'localhost'
        if len(aParamsArray) == 1:
            # self.theArguments = []
            self.showUsage()
            self.doShutdown()
        else:
            self.theArguments = aParamsArray[1:]
        logger.debug("found %s", self.theArguments)

    def processCommandArguments(self):
        """process cli arguments"""
        try:
            myOptions, myOther = getopt.getopt(self.theArguments, 'ht:p:H:', ['help', 'test=', 'port=', 'host='])
            logger.debug("%s", myOptions)
        except getopt.GetoptError as err:
            logger.error(err)

        for myArguments, myArgumentsValues in myOptions:
            if   myArguments in ('-h', '--help'):
                logger.debug("help")
                self.showUsage()
            elif myArguments in ('-p', '--port'):
                logger.debug("port is %s" % myArgumentsValues)
                self.thePortNumber = int(myArgumentsValues)
            elif myArguments in ('-H', '--host'):
                logger.debug("host is %s" % myArgumentsValues)
                self.theHostName = myArgumentsValues
            elif myArguments in ('-t', '--test'):
                logger.debug("test string is %s" % myArgumentsValues)
            else:
                logger.debug("not help")

    def getPort(self):
        return self.thePortNumber

    def getHostname(self):
        return self.theHostName

    def showUsage(self):
        """show usage"""
        logger.info("\nInstructions: app\n\
         \t[-h|--help] show this help\n\
         \t[-p NUMBER|--port=NUMBER] define port to run on\n\
         \t[abcdef]    some options\n")
        self.doShutdown()

    def doShutdown(self):
        """exit"""
        logger.critical("will stop")
        exit(1)

if __name__ == "__main__":
    logging.error("should not be called directly")
