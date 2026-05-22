from datetime import datetime
import socket
import threading
import os
import stat

ip ="127.0.0.1"
port = 5000

clientes = []

usuarios = {
    "jere": "jere123",
    "marcos": "marcos123",
    "seba": "seba123",
    "aby": "aby123",
    "lucas": "lucas123",
    "mat": "mat123",
    "ariel": "ariel123",
    "luka": "luka123",
    "guille": "guille123"
}

def ejecutar_comandos(cliente, address):
   
    while True:
        try:
            comando = cliente.recv(1024).decode('utf-8')
            comando = comando.strip()
            print(f"|{address}| Ejecuto el comando: {comando}")
            match comando:
                case "exit":
                    cliente.shutdown(socket.SHUT_RDWR)
                    clientes.remove(cliente)
                    break
                case _ if comando.startswith("ls"):

                    comando = comando.split()
                    

                    if len(comando) == 1:
                    
                        if comando[0] == "ls":

                            archivos = os.listdir()

                            if archivos:
                                salida = "\n".join(archivos) #join() sirve para separar elementos de una lista, en este caso con un salto de linea
                            else:
                                salida = "[Directorio vacío]"

                            cliente.send(salida.encode("utf-8"))
                    if len(comando) == 2:

                        if  comando[1] == "-l":
                            salida = ""
                            for archivo in os.scandir("."):
                                info = archivo.stat()

                                
                                permisos = stat.filemode(info.st_mode)
                                tamaño = info.st_size
                                fecha = datetime.fromtimestamp(info.st_mtime)
        
                                salida += (f"{archivo.name} {permisos} {tamaño} {fecha}  \n")
                            
                            cliente.send(salida.encode("utf-8"))
                        
                        elif  comando[1] == "-lh" or comando[1] == "-hl":
                            """
                            La función human_read recibe el tamaño en bytes de el directorio o archivo y recorre un for que recorre los diferentes tamaños desde bytes a terabytes, si el tamaño recibido es menor a 1024,el comando retorna el tamaño en la primer variable del array (bytes), si es mayor a 1024, no entra en el el if y es dividido por 1024 para transformarlo en la siguiente unidad de medida y volver a recorrer el bucle hasta que se de con la unidad exacta
                            """
                            salida = ""
                            def human_read(bytes): 
                                for unidad in ['B', 'K', 'M', 'G', 'T']: 
                                    if bytes < 1024:
                                        return f"{bytes:.1f}{unidad}"
                                    bytes /= 1024
                            
                            for archivo in os.scandir("."):
                                    info = archivo.stat()
                                    
                                    permisos = stat.filemode(info.st_mode)
                                    tamaño = human_read(info.st_size)
                                    fecha = datetime.fromtimestamp(info.st_mtime)

                                    salida += (f"{archivo.name} {permisos} {tamaño} {fecha}  \n")
                            cliente.send(salida.encode("utf-8"))

                      
                            

                        else:
                            try:
                                archivos = os.listdir(comando[1])
                                if archivos:
                                    salida = "\n".join(archivos) #join() sirve para separar elementos de una lista, en este caso con un salto de linea
                                else:
                                    salida = "[Directorio vacío]"

                                cliente.send(salida.encode("utf-8"))
                            except NotADirectoryError:
                                cliente.send("Error Al ejecutar el comando ls: Está intentando listar un archivo, no un directorio".encode("utf-8"))

                            except FileNotFoundError:
                                cliente.send("Error Al ejecutar el comando ls: Archivo no encontrado".encode("utf-8"))

                    if len(comando) == 3:
                        
                        if  comando[2] == "-l":
                            try:
                                d = comando[1]
                                parent_d = os.getcwd()
                                path = os.path.join(parent_d, d)
                                salida = ""
                                for archivo in os.scandir(path):
                                    info = archivo.stat()

                                    
                                    permisos = stat.filemode(info.st_mode)
                                    tamaño = info.st_size
                                    fecha = datetime.fromtimestamp(info.st_mtime)
            
                                    salida += (f"{archivo.name} {permisos} {tamaño} {fecha}  \n")
                                
                                cliente.send(salida.encode("utf-8"))
                            except NotADirectoryError:
                                cliente.send("Error Al ejecutar el comando ls: Está intentando listar un archivo, no un directorio".encode("utf-8"))
                            except FileNotFoundError:
                                cliente.send("Error Al ejecutar el comando ls: Archivo no encontrado".encode("utf-8"))
                            except Exception as e:
                                cliente.send(f"Excepción del lado servidor al ejecutar ls: {str(e)}".encode("utf-8"))

                        
                        elif  comando[2] == "-lh" or comando[2] == "-hl":
                            try:
                                d = comando[1]
                                parent_d = os.getcwd()
                                path = os.path.join(parent_d, d)
                                salida = ""
                                def human_read(bytes): 
                                    for unidad in ['B', 'K', 'M', 'G', 'T']: 
                                        if bytes < 1024:
                                            return f"{bytes:.1f}{unidad}"
                                        bytes /= 1024
                                
                                for archivo in os.scandir(path):
                                        info = archivo.stat()
                                        
                                        permisos = stat.filemode(info.st_mode)
                                        tamaño = human_read(info.st_size)
                                        fecha = datetime.fromtimestamp(info.st_mtime)

                                        salida += (f"{archivo.name} {permisos} {tamaño} {fecha}  \n")
                                cliente.send(salida.encode("utf-8"))

                            except NotADirectoryError:
                                cliente.send("Error Al ejecutar el comando ls: Está intentando listar un archivo, no un directorio".encode("utf-8"))    
                            except FileNotFoundError:
                                cliente.send("Error Al ejecutar el comando ls: Archivo no encontrado".encode("utf-8"))
                            except Exception as e:
                                cliente.send(f"Excepción del lado servidor al ejecutar ls: {str(e)}".encode("utf-8"))

                case _ if comando.startswith("pwd"):
                    comando = comando.split()
                    if len(comando)==1:
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
                
                case _ if comando.startswith("help"):
                    comando = comando.split()
                    if len(comando) == 1:
                        salida = ("Comandos disponibles:\n"
                                "ls\n"
                                "pwd\n"
                                "cat\n"
                                "help\n"
                                "mkdir\n"
                                "exit\n"
                                )
                        cliente.send(salida.encode("utf-8"))

                    if len(comando)==2:
                        match comando[1]:
                            case "ls":
                                salida = (
                                "---USO BÁSICO---\n"
                                "ls -> Lista el directorio actual\n"
                                "ls *directorio* -> Lista el directorio especificado\n"
                                "---OPCIONES: Siempre despues del directorio a listar---\n"
                                "ls -l -> Lista el directorio especificado de manera detallada\n"
                                "ls -lh -> Lista el directorio especificado de manera detallada y con formato de tamaño legible\n"             
                                )
                                cliente.send(salida.encode("utf-8"))
                            case "mkdir":
                                salida = (
                                "---USO BÁSICO---\n"
                                "mkdir *directorio* -> Crea un nuevo directorio en la ubicación actual\n"  
                                )
                                cliente.send(salida.encode("utf-8"))
                                
                            case "cat" :
                                salida = (
                                "---USO BÁSICO---\n"
                                "cat *archivo* -> Lee el contenido de un archivo\n"  
                                )
                                cliente.send(salida.encode("utf-8"))
                                
                            case "pwd":
                                salida = (
                                "---USO BÁSICO---\n"
                                "pwd -> Muestra donde está ubicado el directorio actual\n"  
                                )
                                cliente.send(salida.encode("utf-8"))
                            case "exit":
                                salida = (
                                "---USO BÁSICO---\n"
                                "exit -> Cierra la sesión de shell remoto\n"  
                                )
                                cliente.send(salida.encode("utf-8"))

                case _ if comando.startswith("mkdir "):
                    try:
                        nombre_directorio = comando.split(" ", 1)[1]
                        d = nombre_directorio
                        parent_d = os.getcwd()
                        path = os.path.join(parent_d, d)
                        os.mkdir(path)
                        cliente.send(f"Directorio {nombre_directorio} creado exitosamente en el servidor".encode("utf-8"))
                    except Exception as e:
                            cliente.send(f"Excepción del lado servidor al ejecutar mkdir: {str(e)}".encode("utf-8"))
                case _:
                    cliente.send("Error: Comando no reconocido, intente nuevamente".encode("utf-8"))
        except (socket.error, OSError):
            clientes.remove(cliente)
            cliente.close()
            break



def recibir_conexiones():
    while True:
        if(clientes.__len__() < 10):
            cliente, address = server.accept()
            print(f"Cliente desde la IP {address} conectado al servidor")
            clientes.append(cliente)
            thread = threading.Thread(target=autenticar, args=(cliente,address))
            thread.start()
        else:
            cliente, address = server.accept()
            cliente.send("Conexión fallida: Número máximo de clientes (10) alcanzado".encode("utf-8"))
            cliente.close()

def autenticar(cliente, address):
    intentos = 0
    isUserInvalid = True
    isPasswordInvalid = True
    try:
        cliente.send("Conexión exitosa: Bienvenido al Shell Remoto\nIntrouzca su nombre de usuario".encode("utf-8"))
        
        while isUserInvalid:
            user = cliente.recv(1024).decode('utf-8')
            if user in usuarios:
                isUserInvalid = False
            else:
                intentos = intentos + 1
                if intentos < 3:
                    
                    cliente.send("Usuario incorrecto, intente de nuevo".encode("utf-8"))
                if intentos >= 3:
                    cliente.send("Usuario incorrecto: Desconectando del servidor".encode("utf-8"))
                    cliente.close()
        cliente.send("Introuzca su contraseña de usuario".encode("utf-8"))  
        while isPasswordInvalid:
            password = cliente.recv(1024).decode('utf-8')
            if usuarios[user] == password:
                isPasswordInvalid = False
                cliente.send("@uservalid".encode("utf-8"))
                thread = threading.Thread(target=ejecutar_comandos, args=(cliente,address))
                thread.start()

            else:
                intentos = intentos + 1
                if intentos < 3:
                    
                    cliente.send("Contraseña incorrecta, intente de nuevo".encode("utf-8"))
                if intentos >= 3:
                    cliente.send("Contraseña incorrecta: Desconectando del servidor".encode("utf-8"))
                    cliente.close()
    except(socket.error, OSError):
            clientes.remove(cliente)
            cliente.close()
        

    
    

        







server =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip,port))
server.listen()
recibir_conexiones()
