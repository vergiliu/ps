import logging
from multiprocessing import Queue
from FolderComparator import FolderComparator

#class Singleton(object):
#  _instance = None
#  def __new__(class_, *args, **kwargs):
#    if not isinstance(class_._instance, class_):
#        class_._instance = object.__new__(class_, *args, **kwargs)
#    return class_._instance

__module__ = 'src'
__name__ = 'Quu'
logger = logging.getLogger("main")

class Quu(): #Singleton
    def __init__(self):
        self.queue = Queue()
        logger.debug('new queue')

    def addFolders(self, aLeftFolder, aRightFolder):
        logger.debug('adding new item in the quu')
        myComparator = FolderComparator(aLeftFolder, aRightFolder)
        myComparator.setSyncType("keepboth")
        self.queue.put(myComparator)

    def getQuu(self):
        return self.queue

    def getNext(self):
        """
        @return FolderComparator the folder
        """
        try:
            return self.queue.get_nowait()
        except BaseException:
            return None

    def getSize(self):
        return self.queue.qsize()
