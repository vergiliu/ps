import asyncore
import socket
import signal
import logging
from ClientHandler import ClientHandler

__module__ = 'src'
__name__ = 'ProcessingServer'
logger = logging.getLogger("main")

class ProcessingServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        signal.signal(signal.SIGINT, self.interruptExecution)
        logger.debug("host is %s port is %d" % (host, port))
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind( (host, port) )
        self.listen(5)

    def handle_accepted(self, sock, addr):
        logger.debug('Incoming connection from %s' % repr(addr))
        handler = ClientHandler(sock)

    def interruptExecution(self, signal, frame):
        # import multiprocessing
        #p = multiprocessing.current_process()
        #print ("alive %s pid %d" % (p.is_alive(), p.pid))
        #p.terminate()
        #    c = multiprocessing.Process(target=starttel, args=())
        # c.start()
        # join()
        logger.info("server is exiting\n")
        exit(1)

    def startServer(self):
        asyncore.loop()

# server = ProcessingServer('localhost', 8080)
# asyncore.loop()
