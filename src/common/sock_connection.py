
import socket
import asyncore


class Sock_connection(asyncore.dispatcher_with_send):
    
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
            asyncore.dispatcher_with_send.__init__(self, sock)
        elif host is not None and port is not None:
            asyncore.dispatcher_with_send.__init__(self)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.connect((host, port))
            except:
                self._keep_running = False
                return
        else:
            raise Exception("Invalid arguments")
        
        self._terminator = '\1\2\3'
        self._terminator_len = len(self._terminator)
        self._buffer = []
        self._keep_running = True
        self._finding_buffer = ''
    
    
    def handle_connect(self):
        self.on_connect()
    
    
    def handle_close(self):
        self._keep_running = False    
        self.on_close()
        self.close()
    
        
    def handle_read(self):
        data = self.recv(8192)
        if not data:
            return
        
        self._finding_buffer += data
        index = self._finding_buffer.find(self._terminator)
        while index > -1:
            data = self._finding_buffer[:index]
            if data:
                self._buffer.append(data)
            self._finding_buffer = self._finding_buffer[index + self._terminator_len:]
            index = self._finding_buffer.find(self._terminator)
            self._found_terminator()
        
        # added extra 10 just so not splitting data that was really small for no need
        if len(self._finding_buffer) > self._terminator_len + 10:
            self._buffer.append(self._finding_buffer[:-self._terminator_len])
            self._finding_buffer = self._finding_buffer[-self._terminator_len:]


    def _found_terminator(self):
        message = ''.join(self._buffer)
        self._buffer = []
        self.on_message(message)

        
    def send_message(self, message):
        # use this API
        if not self.connected:
            return
        try:
            self.send(message + self._terminator)
        except socket.error:
            self.handle_error()

        
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
