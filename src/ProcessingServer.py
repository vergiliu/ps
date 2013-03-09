import asyncore
import socket
import signal
import logging

__name__ = 'ProcessingServer'
logger = logging.getLogger("main")


class ClientHandler(asyncore.dispatcher_with_send):
    """The class will take care of dispatching work from clients connected to the
    ProcessingServer class and adding tasks to a Queue 
    TODO add queue
    TODO add meaningful processing
    TODO move class out of this file
    """
    def handle_read(self):
        data = self.recv(8192)
        myIncomingData = str(data.decode('utf-8').lower().strip())
        print("r= %s" %  myIncomingData)
        if myIncomingData == "quit":
            self.send(b'')
            self.close()
        elif myIncomingData == "test":
            self.send(b'this is a test\n')
        elif myIncomingData.startswith('sync'):
            self.send(b'sync-ing\n')
        else:
            self.send(b'command is not valid\n') # send data to echo

    def handle_accepted(self):
        self.send(b'Hello there stranger\n')
    
    def handle_connect(self):
        logger.debug('server-connect')


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
