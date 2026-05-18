import socket
import threading

ip ="127.0.0.1"
port = 5000


def ejecutar_comandos():
    pass

def recibir_conexiones():
    while True:
        client, address = server.accept()

        thread = threading.Thread(target=recibir_conexiones, args=(client,))
        thread.start()

server =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip,port))
server.listen()
recibir_conexiones()
