import socket
import sys
import protocolo as proto
import ssl


IP="127.0.0.1"
PORT=5000


def enviar_comando():
    print("Comandos disponibles:\n"
            "cd\n"
            "ls\n"
            "pwd\n"
            "cat\n"
            "help\n"
            "mkdir\n"
            "exit\n"
            )
    while True:
        try:
         comando = input("shell>")
         if comando == "exit":
              cliente.send(comando.encode('utf-8'))
              cliente.close()
              sys.exit()
         proto.enviar_mensaje(cliente, comando)
         salida = proto.recibir_mensaje(cliente)  
         print(f"\n{salida}")
         sys.stdout.flush()
        except (socket.error, OSError):

            print('\n[Conexión perdida con el servidor]')
            cliente.close()
            break

def autenticarse():
    while True:
        try:
            
                salida = proto.recibir_mensaje(cliente)  
                if not salida:
                     cliente.close()
                     sys.exit()

                
                sys.stdout.flush()
                
                if salida == "@kicked":
                     print("Desconectado: Expulsado del servidor")
                     break
                elif salida == "@uservalid":
                    enviar_comando()
                    return
                    
                print(f"\n{salida}")
                respuesta = input(">")
                proto.enviar_mensaje(cliente, respuesta)
        except (socket.error, OSError):

                print('\n[Conexión perdida con el servidor]')
                cliente.close()
                break
            
        

    
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
cliente = context.wrap_socket(cliente, server_hostname="localhost")
try:
     cliente.connect((IP, PORT))
     
except ConnectionRefusedError:
    print("No se pudo conectar al servidor. Verificar que esté encendido.")
    sys.exit()

autenticarse()
