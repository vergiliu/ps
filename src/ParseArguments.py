import getopt #as getopt
import logging

__name__ = 'ParseArguments'
logger = logging.getLogger("main")

class ParseArguments:
    """This is a test"""

    def __init__(self, aParamsArray):
        """init"""
        if len(aParamsArray) == 1:
            self.theArguments = []
        else:
            self.theArguments = aParamsArray[1:]
        logger.info("found %s", self.theArguments)


    def getVariable(self):
        """parse cli params"""
        try:
            myOptions, myOther = getopt.getopt(self.theArguments, 'ht:', ['help', 'test='])
            logger.debug("%s", myOptions)
            logger.info("%s" % myOptions)
        except getopt.GetoptError as err:
            print(err)
            logger.error(err)

        for myArguments, myArgumentsValues in myOptions:
            if myArgumentsValues in ('-h', '--help'):
                logger.info("help")
                self.showUsage()
            else:
                logger.debug("not help")

    def showUsage(self):
        """show usage"""
        logger.debug("help me")

if __name__ == "__main__":
    logging.error("should not be called directly")
