
import socket
import asyncore


class Sock_listener(asyncore.dispatcher):

    def __init__(self, host, port, sock_connection_class):
        asyncore.dispatcher.__init__(self)
        self._sock_connection_class = sock_connection_class
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))        
        self.listen(5)
        self._keep_running = True


    def handle_accept(self):
        if not self._keep_running:
            self.close()
            return
        pair = self.accept()
        if pair is None:
            print 'Invalid connection'
            return
        sock_connection = self._sock_connection_class(sock=pair[0])
        sock_connection.on_accept()

    
    def run(self):
        # use this API
        while self._keep_running:
            asyncore.loop(timeout=0.1, count=10)
        self.close()

    
    def stop(self):
        # use this API
        self._keep_running = False


    def poll(self, timeout=0.1, count=2):
        # use this API
        asyncore.loop(timeout=timeout, count=count)