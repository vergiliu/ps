import getopt #as getopt
import logging

__name__ = 'ParseArguments'
logger = logging.getLogger("main")

class ParseArguments:
    """This is a test"""

    def __init__(self, aParamsArray):
        """init"""
        if len(aParamsArray) == 1:
            # self.theArguments = []
            self.showUsage()
            self.doShutdown()
        else:
            self.theArguments = aParamsArray[1:]
        logger.debug("found %s", self.theArguments)

    def getVariable(self):
        """parse cli params"""
        try:
            myOptions, myOther = getopt.getopt(self.theArguments, 'ht:', ['help', 'test='])
            logger.debug("%s", myOptions)
        except getopt.GetoptError as err:
            logger.error(err)

        for myArguments, myArgumentsValues in myOptions:
            if myArguments in ('-h', '--help'):
                logger.debug("help")
                self.showUsage()
            else:
                logger.debug("not help")

    def showUsage(self):
        """show usage"""
        logger.warning("\nInstructions: app\n\
         \t[-h|--help] show this help\n\
         \t[abcdef]    some options\n")
    
    def doShutdown(self):
        """exit"""
        logger.critical("will stop")
        exit(1)

if __name__ == "__main__":
    logging.error("should not be called directly")
