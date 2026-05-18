import socket
import sys
import threading

IP="127.0.0.1"
PORT=5000


def enviar_comando():
    while True:
        try:
         
         comando = input("shell>")
         if comando.strip() == "exit":
            client.send(comando.encode('utf-8'))
            print("Conexión remota finalizada")
            client.close()
            sys.exit(0)
         

         client.send(comando.encode('utf-8'))
        except (socket.error, OSError):
            break


def recibir_salida():
    while True:
        try:
            salida = client.recv(1024).decode('utf-8')
            
            print(f"\n{salida}")
            sys.stdout.flush()
        except (socket.error, OSError):
            print('\n[Conexión perdida con el servidor]')
            client.close()
            break
  
    
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
     client.connect((IP, PORT))
except ConnectionRefusedError:
    print("No se pudo conectar al servidor. Verificar que esté encendido.")
    sys.exit()


receive_thread = threading.Thread(target=recibir_salida, daemon=True)
receive_thread.start()

write_thread = threading.Thread(target=enviar_comando, daemon=True)
write_thread.start()
receive_thread.join()