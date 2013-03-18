import time
import logging

__module__ = 'src'
__name__ = 'FolderComparatorStatus'
logger = logging.getLogger("main")


class FolderComparatorStatus:
    """The class will store the last update of the FolderComparator and keep track
    of the current status, for long running operations
    """

    def __init__(self):
        self.lastRun = 0
        self.status = None

    def setStatus(self, aStatus):
        self.status = aStatus
        logger.debug("folder status is %s" % self.status)

    def updateStatus(self, aNewStatus):
        self.status = aNewStatus
        self.lastRun = time.time()
        logger.debug("folder status is %s" % self.status)

    def getLastRun(self):
        return self.lastRun

    def getLastStatus(self):
        return self.status

