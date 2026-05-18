import socket
import threading
import os

ip ="127.0.0.1"
port = 5000

clientes = []

def ejecutar_comandos(cliente, address):
    while True:
        try:
            comando = cliente.recv(1024).decode('utf-8')
            comando = comando.strip()
            print(f"|{address}| Ejecuto el comando: {comando}")
            match comando:
                case "exit":
                    cliente.shutdown(socket.SHUT_RDWR)
                    cliente.close()
                    clientes.remove(cliente)
                    break
                case "ls":

                    archivos = os.listdir()

                    if archivos:
                        salida = "\n".join(archivos) #join() sirve para separar elementos de una lista, en este caso con un salto de linea
                    else:
                        salida = "[Directorio vacío]"

                    cliente.send(salida.encode("utf-8"))

                case "pwd":
                    directorio = os.getcwd()

                    cliente.send(directorio.encode("utf-8"))
                case _ if comando.startswith("cat "):
                    try:
                        nombre_archivo = comando.split(" ", 1)[1] #divido el comando 1 sola vez entre espacios y me quedo con el primer elemento (argumento de cat)

                        with open(nombre_archivo, "r", encoding="utf-8") as archivo: #abro el archivo con el nombre que guarde anteriormente, en modo lectura y codeado en utf 8, lo guardo en una variable archivo, with me permite cerrarlo automaticamente
                            contenido = archivo.read()

                        cliente.send(contenido.encode("utf-8"))

                    except FileNotFoundError:
                        cliente.send("Error: Archivo no encontrado".encode("utf-8"))

                    except Exception as e:
                        cliente.send(f"Excepción del lado servidor al ejecutar cat: {str(e)}".encode("utf-8"))
                case _:
                    cliente.send("Error: Comando no reconocido, intente nuevamente".encode("utf-8"))
        except (socket.error, OSError):
            clientes.remove(cliente)
            cliente.close()
            break






    

def recibir_conexiones():
    while True:
        if(clientes.__len__() < 5):
            cliente, address = server.accept()
            print(f"Cliente desde la IP {address} conectado al servidor")
            cliente.send("Conexión exitosa: Bienvenido al Shell Remoto".encode("utf-8"))
            clientes.append(cliente)
            thread = threading.Thread(target=ejecutar_comandos, args=(cliente,address))
            thread.start()
        else:
            cliente, address = server.accept()
            cliente.send("Conexión fallida: Número máximo de clientes (5) alcanzado".encode("utf-8"))
            cliente.close()


server =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip,port))
server.listen()
recibir_conexiones()
