import socket
import sys
import threading



IP="127.0.0.1"
PORT=5000


def enviar_comando():
    print("Comandos disponibles:\n"
            "ls\n"
            "pwd\n"
            "cat\n"
            "help\n"
            "mkdir\n"
            "exit\n")
    while True:
        try:
         comando = input("shell>")
         if comando == "exit":
              cliente.close()
              sys.exit()
         cliente.send(comando.encode('utf-8'))
         salida = cliente.recv(1024).decode('utf-8')  
         print(f"\n{salida}")
         sys.stdout.flush()
        except (socket.error, OSError):

            print('\n[Conexión perdida con el servidor]')
            cliente.close()
            break

def autenticarse():
    while True:
        try:
            
                salida = cliente.recv(1024)
                if not salida:
                     cliente.close()
                     sys.exit()

                salida = salida.decode("utf-8")
                sys.stdout.flush()
                
                if salida == "@uservalid":
                    enviar_comando()
                    return
                    
                print(f"\n{salida}")
                respuesta = input(">")
                cliente.send(respuesta.encode("utf-8"))
        except (socket.error, OSError):

                print('\n[Conexión perdida con el servidor]')
                cliente.close()
                break
        

    
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
     cliente.connect((IP, PORT))
except ConnectionRefusedError:
    print("No se pudo conectar al servidor. Verificar que esté encendido.")
    sys.exit()

autenticarse()
