
import socket
import threading
import os
import db
import protocolo as proto
import ssl
import comandos

ip ="127.0.0.1"
port = 5000

clientes = []
clientes_lock = threading.Lock()


def ejecutar_comandos(cliente, address):
    actual_path = os.getcwd()
   
    while True:
        try:
            comando = proto.recibir_mensaje(cliente)
            comando = comando.strip()
            print(f"|{address}| Ejecuto el comando: {comando}")
            match comando:
                case "exit":
                    with clientes_lock:
                        comandos.exit(cliente, clientes)
                    break
                case _ if comando.startswith("ls"):
                    tiene_pathtraversal = comandos.ls(comando, cliente, actual_path)
                    if tiene_pathtraversal:
                        break

                case _ if comando.startswith("pwd"):
                    
                    comandos.pwd(comando, cliente)
                      
                case _ if comando.startswith("cat "):
                    tiene_pathtraversal = comandos.cat(comando, cliente)
                    if tiene_pathtraversal:
                        break    
                case _ if comando.startswith("help"):
                    comandos.help(comando, cliente)
                case _ if comando.startswith("mkdir "):
                    tiene_pathtraversal =comandos.mkdir(comando, cliente, actual_path)
                    if tiene_pathtraversal:
                        break
                case _ if comando.startswith("cd "):
                    resultado,tiene_pathtraversal = comandos.cd(comando, cliente, actual_path)
                    if tiene_pathtraversal:
                        break
                    if resultado:
                        actual_path=resultado  
                case _:
                    salida = "Error: Comando no reconocido, intente nuevamente"
                    proto.enviar_mensaje(cliente, salida)
                   
        except (socket.error, OSError):
            with clientes_lock:
                clientes.remove(cliente)
            cliente.close()
            break



def recibir_conexiones():
    while True:
        
        cliente, address = server.accept()
        cliente_ssl = context.wrap_socket (cliente,server_side=True) #envuelve el socket de texto plano a uno con funcionalidad tls
        permitir = False

        with clientes_lock:

            if len(clientes) < 5:
                clientes.append(cliente_ssl)
                permitir = True

        if permitir:

            print(f"Cliente desde la IP {address} conectado al servidor")

            thread = threading.Thread(
                target=autenticar,
                args=(cliente_ssl, address)
            )

            thread.start()

        else:

            cliente.send(
                "Conexión fallida: Número máximo de clientes (5) alcanzado"
                .encode("utf-8")
            )

            cliente.close()

def autenticar(cliente, address):
    intentos = 0
    isUserInvalid = True
    isPasswordInvalid = True
    try:
        proto.enviar_mensaje(cliente, "Conexión exitosa: Bienvenido al Shell Remoto\nIntrouzca su nombre de usuario")
        
        
        while isUserInvalid:
            username = proto.recibir_mensaje(cliente)
            userDB = db.buscar_usuario(username)
            print(repr(username))
            print(type(username))
            if userDB:
                isUserInvalid = False
                print(f"Resultado DB: {userDB}")
            else:
                intentos = intentos + 1
                if intentos < 3:
                    
                    proto.enviar_mensaje(cliente, "Usuario incorrecto, intente de nuevo")
                    
                if intentos >= 3:
                    proto.enviar_mensaje(cliente, "@kicked")
                    
                    with clientes_lock:
                        clientes.remove(cliente)
                    cliente.close()
        proto.enviar_mensaje(cliente, "Introuzca su contraseña de usuario")            
        
        while isPasswordInvalid:
            password = proto.recibir_mensaje(cliente)
            if db.verificar_contraseña(userDB, password):
                isPasswordInvalid = False
                proto.enviar_mensaje(cliente, "@uservalid")   
                thread = threading.Thread(target=ejecutar_comandos, args=(cliente,address))
                thread.start()

            else:
                intentos = intentos + 1
                if intentos < 3:
                    proto.enviar_mensaje(cliente, "Contraseña incorrecta, intente de nuevo")
                    
                if intentos >= 3:
                    proto.enviar_mensaje(cliente, "@kicked")
                    
                    with clientes_lock:
                        clientes.remove(cliente)
                    cliente.close()
    except(socket.error, OSError):
            with clientes_lock:
                clientes.remove(cliente)
            cliente.close()
    except Exception as e:
            print(f"Error por excepcion: {e}")
            with clientes_lock:
                clientes.remove(cliente)
            cliente.close()


server =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
context = ssl.SSLContext(
    ssl.PROTOCOL_TLS_SERVER
)
context.load_cert_chain(
    certfile="cert.pem",
    keyfile="key.pem"
)
server.bind((ip,port))

server.listen()

print("Servidor encendido y a la escucha de conexiones")

recibir_conexiones()
