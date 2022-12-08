import socket
import time
import queue
import threading

MSG_END = '\n'

class SocketChecker:
    def __init__(self, IP, port):
        self.IP = IP
        self.port = port
        self.val = None

    def check(self):    
        s = socket.socket()
        s.connect((self.IP, self.port))
        # TODO get everything 
        def get_msg(connection):
            msg = ""
            q = queue.Queue()
            while True:
                if q.empty():
                    buffer = connection.recv(1024).decode()
                    for i in buffer:
                        q.put(i)
                item = q.get()
                if item == MSG_END:
                    break
                msg += item
            self.val = msg
        thread = threading.Thread(target=get_msg, args=(s,))
        thread.start()
        thread.join(timeout=3)
        msg = self.val
        self.val = None
        if msg is None:
            raise Exception("Did not receive an answer")
        return msg

    def identify(self):
        return self.IP + ":" + str(self.port)
        
