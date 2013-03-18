import time #for sleep
import asyncore
import logging
import re
from Quu import Quu
from FolderComparator import FolderComparator

__module__ = 'src'
__name__ = 'ClientHandler'
logger = logging.getLogger("main")


class ClientHandler(asyncore.dispatcher_with_send):
    def __init__(self, sock):
        asyncore.dispatcher_with_send.__init__(self, sock)
        #self.quu  = None
        #asyncore.dispatcher.__init__(self)
        self.queue = Quu()
        self.fc = None

    def handleSync(self):
        myComp = self.queue.getNext()
        if myComp is not None:
            time.sleep(1)
            #self.send(str(myComp.isInSync()).encode())
            myComp.runComparison()
            #myComp.isInSync():
            myComp.syncNow()
            myComp.printReport()

        self.send(b' done\n')

    def new(self, anInputString):
        mySearch = re.search('add l(eft){0,1}:(.*) r(ight){0,1}:(.*)', anInputString)
        if type(mySearch) != type(None):
            # len(mySearch.groups()) == 4
            #('ana/are mere/saptezeci', 'costel vine/si_cere/10')
            self.fc = FolderComparator(mySearch.group(2), mySearch.group(4))
            self.queue.addFolders(mySearch.group(2), mySearch.group(4))

    def handle_read(self):
        data = self.recv(8192)
        myIncomingData = str(data.decode('utf-8').lower().strip())
        logger.debug("incoming data %s" %  myIncomingData)

        if myIncomingData == "quit":
            self.send(b'')
            self.close()

        elif myIncomingData.startswith('add'):
            self.new(myIncomingData)

        elif myIncomingData == "test":
            self.send(b'this is a test\n')

        elif myIncomingData.startswith('sync'):
            self.send(b'sync-ing...')
            self.handleSync()

        else:
            self.send(b'command is not valid\n') # send data to echo

    def handle_accepted(self):
        self.send(b'Hello there stranger\n')

    def handle_connect(self):
        logger.debug('server-connect')
