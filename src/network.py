
import socket
import asyncore
import asynchat


class Handler(asynchat.async_chat):
    
    def __init__(self, *args, **kwargs):
        # host, port, sock
        
        self.keep_running = True
        
        host = None
        port = None
        sock = None
        
        if 'host' in kwargs and kwargs.get('host') is not None:
            host = kwargs.get('host')
        elif len(args) > 0 and args[0] is not None:
            host = args[0]
        
        if 'port' in kwargs and kwargs.get('port') is not None:
            port = kwargs.get('port')
        elif len(args) > 1 and args[1] is not None:
            port = args[1]
            
        if 'sock' in kwargs and kwargs.get('sock') is not None:
            sock = kwargs.get('sock')
        elif len(args) > 2 and args[2] is not None:
            sock = args[2]
        
        if sock is not None:
            asynchat.async_chat.__init__(self, sock)
        elif host is not None and port is not None:
            asynchat.async_chat.__init__(self)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect((host, port))
        else:
            raise Exception("Invalid arguments")
        
        self.set_terminator('\1\2\3')
        self._buffer = []
    
    def handle_connect(self):
        self.on_connect()
    
    def handle_close(self):
        self.keep_running = False    
        self.on_close()
        self.close()
        
    def collect_incoming_data(self, data):
        self._buffer.append(data)

    def found_terminator(self):
        message = ''.join(self._buffer)
        self._buffer = []
        self.on_message(message)
        
    def send_message(self, message):
        self.push(message + '\1\2\3')
        
    def poll(self, timeout=.2, count=10):
        # use this API
        asyncore.loop(timeout=timeout, count=count)
        
    def run(self, timeout=.2, count=10):
        # use this API
        while self.keep_running:
            asyncore.loop(timeout=timeout, count=count)
        asyncore.loop(timeout=.2, count=2)            
        self.close()    
    
    def stop(self):
        # use this API
        self.keep_running = False

    def on_accept(self):
        # override on_accept method
        pass
    
    def on_connect(self):
        # override on_connect method
        pass
    
    def on_close(self):
        # override on_close method
        pass
        
    def on_message(self, message):
        # override on_message method
        pass


class Listener(asyncore.dispatcher):

    def __init__(self, host, port, handler_class):
        self.keep_running = True
        
        asyncore.dispatcher.__init__(self)
        self.handler_class = handler_class
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))        
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            raise Exception("Invalid connection")
        
        handler = self.handler_class(sock=pair[0])
        handler.on_accept()
    
    def run(self):
        # use this API
        while self.keep_running:
            asyncore.loop(timeout=.2, count=10)
        self.close()
    
    def stop(self):
        # use this API
        self.keep_running = False
