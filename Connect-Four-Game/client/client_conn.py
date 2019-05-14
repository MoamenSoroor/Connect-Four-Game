
import threading as thr
import socket as soc
import sys , trace


class ClientComm(thr.Thread):
    def __init__(self, peer_addr):
        super().__init__()
        self.type = "client"
        self.addr = None
        self.host = None
        self.port = None
        self.peer_addr = peer_addr
        self.peer_host = peer_addr[0]
        self.peer_port = peer_addr[1]
        self.conn_soc = None

        self.play = False
        self.closed = False


    def run(self):
        try:

            play = False
            self.conn_soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)

            self.conn_soc.connect((self.peer_host, self.peer_port))

            self.addr = self.conn_soc.getsockname()
            self.host = self.addr[0]
            self.port = self.addr[1]

            self.play = True

            print("Client Started at ", self.conn_soc.getsockname())
            print("Connection with Server:", self.conn_soc.getpeername())


        except soc.error as e:
            print(e)
            sys.exit(0)

        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            sys.exit(0)
        except:
            print(trace.print_exc())
            sys.exit(0)

    def is_play(self):
        return self.play

    def send(self, data):
        if self.conn_soc is None:
            return
        try:
            self.conn_soc.send(str(data).encode("utf-8"))
        except Exception as e:
            print(e)

    def recv(self):
        # ------------------ blocking function --------------------
        if self.conn_soc is None:
            return None
        try:
            msg = self.conn_soc.recv(1024).decode("utf-8")
            return msg
        except Exception as e:
            print(e)
        return None

    # close sockets
    def close(self):
        self.closed = True
        self.play = False
        if not (self.conn_soc is None):
            self.conn_soc.close()

