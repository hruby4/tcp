import socket
import threading
import commands as c
from Address import Address


class Server:
    def __init__(self,address,port):
        self.address = address
        self.port = port
        self.clients = []

    def start(self):
        server_inet_address = (self.address,self.port)
        server_socket = socket.socket()
        server_socket.bind(server_inet_address)
        server_socket.listen()
        self.accept(server_socket)
        print("Server started")
        return True

    def accept(self,server_socket):
        while True:
            connection, client_inet_address = server_socket.accept()
            t = threading.Thread(target=self.run,args=[connection,server_socket,client_inet_address])
            t.start()
            print("Client connection accepted from " + str(client_inet_address[0]) + ":" + str(client_inet_address[1]))
            self.clients.append(Address(client_inet_address[0],client_inet_address[1]))

    def run(self,connection,server_socket,client_inet_address):
        while True:
            message = "AHOJ\r\n"
            message_as_bytes = bytes(message, "utf-8")
            connection.sendall(message_as_bytes)
            while True:
                try:
                    x = connection.recv(60)
                    if x.decode() != "\r\n":
                        print("User: " + x.decode())
                        if x.decode() == "exit":
                            connection.close()
                            for x in self.clients:
                                if x.address == client_inet_address[0] and x.port == client_inet_address[1]:
                                    self.clients.remove(x)
                        elif x.decode() == "help":
                            message = "exit - leave\r\nshutdown-server - vypne server\r\ndate - vypise aktualni datum\r\ncitat - napise nahodny citat ze sbirky\r\n"
                            message_as_bytes = bytes(message, "utf-8")
                            connection.sendall(message_as_bytes)
                        elif x.decode() == "date":
                            message = c.date() + "\r\n"
                            message_as_bytes = bytes(message, "utf-8")
                            connection.sendall(message_as_bytes)
                        elif x.decode() == "citat":
                            message = c.citat() + "\r\n"
                            message_as_bytes = bytes(message, "utf-8")
                            connection.sendall(message_as_bytes)
                        elif x.decode() == "shutdown-server":
                            connection.close()
                            server_socket.close()
                        elif x.decode() == "clients":
                            for x in self.clients:
                                if x.address == client_inet_address[0] and x.port == client_inet_address[1]:
                                    continue
                                message = (x.address + ":" + str(x.port) + "\n")
                                message_as_bytes = bytes(message, "utf-8")
                                connection.sendall(message_as_bytes)
                        else:
                            message = "neznamy prikaz\r\n"
                            message_as_bytes = bytes(message, "utf-8")
                            connection.sendall(message_as_bytes)
                except WindowsError:
                    print("User " + client_inet_address[0] + str(client_inet_address[1]) + " ukoncil spojeni")
                    return
