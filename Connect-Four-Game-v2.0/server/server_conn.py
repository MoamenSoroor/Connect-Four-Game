import threading as thr
import socket as soc
import sys , trace


class ServerComm(thr.Thread):

    def __init__(self, addr):
        super().__init__()
        self.type = "server"
        self.addr = addr
        self.host = addr[0]
        self.port = addr[1]
        self.peer_addr = None
        self.peer_host = None
        self.peer_port = None
        self.server_soc = None
        self.conn_soc = None
        self.play = False

        self.closed = False

    def run(self):

        try:
            self.play = False
            self.server_soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
            self.server_soc.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)

            self.server_soc.bind((self.host, self.port))

            self.server_soc.listen(1)
            print("Server now can listen at {}".format(self.server_soc.getsockname()))

            # establish a connection
            # it return connection socket and tuple with (host address, port)
            # ------------------ blocking function --------------------
            self.conn_soc, self.peer_addr = self.server_soc.accept()
            self.peer_host = self.peer_host
            self.peer_port = self.peer_port
            print("server connected to:",self.peer_addr)
            self.play = True

        except soc.error as e:
            print(e)
            sys.exit(0)

        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            sys.exit(0)
        except:
            print(trace.print_exc())
            sys.exit(0)

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

    def is_play(self):
        return self.play

    # close sockets
    def close(self):
        self.play = False
        self.closed = True
        if not (self.server_soc is None):
            self.server_soc.close()
        if not (self.conn_soc is None):
            self.conn_soc.close()


