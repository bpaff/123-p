
import socket
import asyncore


from common.asynchat import async_chat 


class Sock_connection(async_chat):
    
    def __init__(self, *args, **kwargs):
        # host, port, sock
        
        host = None
        port = None
        sock = None
        
        if 'host' in kwargs:
            host = kwargs.get('host')
        elif len(args) > 0:
            host = args[0]
        
        if 'port' in kwargs:
            port = kwargs.get('port')
        elif len(args) > 1:
            port = args[1]
            
        if 'sock' in kwargs:
            sock = kwargs.get('sock')
        elif len(args) > 2:
            sock = args[2]
        
        if sock is not None:
            async_chat.__init__(self, sock)
        elif host is not None and port is not None:
            async_chat.__init__(self)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.connect((host, port))
            except:
                self._keep_running = False
                return
        else:
            raise Exception("Invalid arguments")
        
        self.set_terminator('\1\2\3')
        self._buffer = []
        self._keep_running = True
    
    
    def handle_connect(self):
        self.on_connect()
    
    
    def handle_close(self):
        self._keep_running = False    
        self.on_close()
        self.close()
    
        
    def collect_incoming_data(self, data):
        self._buffer.append(data)


    def found_terminator(self):
        message = ''.join(self._buffer)
        self._buffer = []
        self.on_message(message)

        
    def send_message(self, message):
        # use this API
        self.push(message + '\1\2\3')

        
    def poll(self, timeout=0.1, count=2):
        # use this API
        asyncore.loop(timeout=timeout, count=count)

        
    def run(self, timeout=0.1, count=10):
        # use this API
        while self._keep_running:
            asyncore.loop(timeout=timeout, count=count)
        asyncore.loop(timeout=0.1, count=2)            
        self.close()    

    
    def stop(self):
        # use this API
        self._keep_running = False


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
