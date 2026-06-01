import socket
import protocolo as proto
import os
import stat
import datetime

def ls(comando, cliente,  actual_path):
    if (
                    "/" in comando
                    or "\\" in comando
                    or ".." in comando
                    or ":" in comando
                    ):
                        salida = "Error al ejecutar comando ls:  No se permiten rutas"
                        proto.enviar_mensaje(cliente, salida)
                        return True

    comando = comando.split()
                    

    if len(comando) == 1:
                    
                        if comando[0] == "ls":

                            archivos = os.listdir(path=actual_path)

                            if archivos:
                                salida = "\n".join(archivos) #join() sirve para separar elementos de una lista, en este caso con un salto de linea
                            else:
                                salida = "[Directorio vacío]"

                            proto.enviar_mensaje(cliente, salida)
                            
    if len(comando) == 2:

                        if  comando[1] == "-l":
                            salida = ""
                            for archivo in os.scandir(path=actual_path):
                                info = archivo.stat()

                                
                                permisos = stat.filemode(info.st_mode)
                                tamaño = info.st_size
                                fecha = datetime.fromtimestamp(info.st_mtime)
        
                                salida += (f"{archivo.name} {permisos} {tamaño} {fecha}  \n")
                            
                            proto.enviar_mensaje(cliente, salida)
                        
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
                            
                            for archivo in os.scandir(path=actual_path):
                                    info = archivo.stat()
                                    
                                    permisos = stat.filemode(info.st_mode)
                                    tamaño = human_read(info.st_size)
                                    fecha = datetime.fromtimestamp(info.st_mtime)

                                    salida += (f"{archivo.name} {permisos} {tamaño} {fecha}  \n")
                            proto.enviar_mensaje(cliente, salida)

                      
                            

                        else:
                            try:
                                archivos = os.listdir(comando[1])
                                if archivos:
                                    salida = "\n".join(archivos) #join() sirve para separar elementos de una lista, en este caso con un salto de linea
                                else:
                                    salida = "[Directorio vacío]"

                                proto.enviar_mensaje(cliente, salida)
                            except NotADirectoryError:
                                salida = "Error Al ejecutar el comando ls: Está intentando listar un archivo, no un directorio"
                                proto.enviar_mensaje(cliente, salida)
                                

                            except FileNotFoundError:
                                salida="Error Al ejecutar el comando ls: Archivo no encontrado"
                                proto.enviar_mensaje(cliente, salida)
                                

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
                                
                                proto.enviar_mensaje(cliente, salida)
                            except NotADirectoryError:
                                salida="Error Al ejecutar el comando ls: Está intentando listar un archivo, no un directorio"
                                proto.enviar_mensaje(cliente, salida)
                                
                            except FileNotFoundError:
                                salida = "Error Al ejecutar el comando ls: Archivo no encontrado"
                                proto.enviar_mensaje(cliente, salida)
                                
                            except Exception as e:
                                salida = f"Excepción del lado servidor al ejecutar ls: {str(e)}"
                                proto.enviar_mensaje(cliente, salida)
                                

                        
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
                                proto.enviar_mensaje(cliente, salida)

                            except NotADirectoryError:
                                salida ="Error Al ejecutar el comando ls: Está intentando listar un archivo, no un directorio"
                                proto.enviar_mensaje(cliente, salida)
                                  
                            except FileNotFoundError:
                                salida = "Error Al ejecutar el comando ls: Archivo no encontrado"
                                proto.enviar_mensaje(cliente, salida)
                                
                            except Exception as e:
                                salida = f"Excepción del lado servidor al ejecutar ls: {str(e)}"
                                proto.enviar_mensaje(cliente, salida)
    pass
def cat(comando, cliente):
    if (
                    "/" in comando
                    or "\\" in comando
                    or ".." in comando
                    or ":" in comando
                    ):
                        salida = "Error al ejecutar comando ls:  No se permiten rutas"
                        proto.enviar_mensaje(cliente, salida)
                        return True

    try:
                        nombre_archivo = comando.split(" ", 1)[1] #divido el comando 1 sola vez entre espacios y me quedo con el primer elemento (argumento de cat)
                    

                        with open(nombre_archivo, "r", encoding="utf-8") as archivo: #abro el archivo con el nombre que guarde anteriormente, en modo lectura y codeado en utf 8, lo guardo en una variable archivo, with me permite cerrarlo automaticamente
                            salida = archivo.read()

                        proto.enviar_mensaje(cliente, salida)

    except FileNotFoundError:
                        salida="Error: Archivo no encontrado"
                        proto.enviar_mensaje(cliente, salida)
                        

    except Exception as e:
                        salida = f"Excepción del lado servidor al ejecutar cat: {str(e)}"
                        proto.enviar_mensaje(cliente, salida)
    pass
def mkdir(comando, cliente, actual_path):
    if (
                    "/" in comando
                    or "\\" in comando
                    or ".." in comando
                    or ":" in comando
                    ):
                        salida = "Error al ejecutar comando ls:  No se permiten rutas"
                        proto.enviar_mensaje(cliente, salida)
                        return True

    try:
                        nombre_directorio = comando.split(" ", 1)[1]
                        d = nombre_directorio
                        path = os.path.join(actual_path, d)
                        os.mkdir(path)
                        salida=f"Directorio {nombre_directorio} creado exitosamente en el servidor"
                        proto.enviar_mensaje(cliente, salida)
                        
    except Exception as e:
                            salida=f"Excepción del lado servidor al ejecutar mkdir: {str(e)}"
                            proto.enviar_mensaje(cliente, salida)

    pass
def help(comando, cliente):
    comando = comando.split()
    if len(comando) == 1:
                        salida = ("Comandos disponibles:\n"
                                "cd\n"                         
                                "ls\n"
                                "pwd\n"
                                "cat\n"
                                "help\n"
                                "mkdir\n"
                                "exit\n"
                                )
                        proto.enviar_mensaje(cliente, salida)

    if len(comando)==2:
                        match comando[1]:
                                
                            case "cd":
                                salida = (
                                "---USO BÁSICO---\n"
                                "cd *directorio* -> Se mueve del directorio actual al especificado\n"
                                "cd .. -> Se mueve del directorio actual al directorio padre\n"     
                                )
                                proto.enviar_mensaje(cliente, salida)
                                
                            case "ls":
                                salida = (
                                "---USO BÁSICO---\n"
                                "ls -> Lista el directorio actual\n"
                                "ls *directorio* -> Lista el directorio especificado\n"
                                "---OPCIONES: Siempre despues del directorio a listar---\n"
                                "ls -l -> Lista el directorio especificado de manera detallada\n"
                                "ls -lh -> Lista el directorio especificado de manera detallada y con formato de tamaño legible\n"             
                                )
                                proto.enviar_mensaje(cliente, salida)
                            case "mkdir":
                                salida = (
                                "---USO BÁSICO---\n"
                                "mkdir *directorio* -> Crea un nuevo directorio en la ubicación actual\n"  
                                )
                                proto.enviar_mensaje(cliente, salida)
                                
                            case "cat" :
                                salida = (
                                "---USO BÁSICO---\n"
                                "cat *archivo* -> Lee el contenido de un archivo\n"  
                                )
                                proto.enviar_mensaje(cliente, salida)
                                
                            case "pwd":
                                salida = (
                                "---USO BÁSICO---\n"
                                "pwd -> Muestra donde está ubicado el directorio actual\n"  
                                )
                                proto.enviar_mensaje(cliente, salida)
                            case "exit":
                                salida = (
                                "---USO BÁSICO---\n"
                                "exit -> Cierra la sesión de shell remoto\n"  
                                )
                                proto.enviar_mensaje(cliente, salida)

    pass
def pwd(comando,cliente):
    comando = comando.split()
    if len(comando)==1:
        salida = os.getcwd()
        proto.enviar_mensaje(cliente, salida)
    pass
def cd(comando, cliente, actual_path):

    if ("/" in comando or "\\" in comando or ":" in comando):

        salida = "Error al ejecutar comando cd: No se permiten rutas"

        proto.enviar_mensaje(cliente, salida)

        return actual_path, True

    try:

        directorio = comando.split(" ", 1)[1]

        if directorio == "..":

            actual_path = os.path.dirname(actual_path)

            salida = f"Directorio actual cambiado: {actual_path}"

            proto.enviar_mensaje(cliente, salida)

            return actual_path, False

        else:

            lista = os.listdir(path=actual_path)

            path = os.path.join(actual_path, directorio)

            if directorio in lista and not os.path.isfile(path):

                actual_path = path

                salida = f"Directorio actual cambiado: {actual_path}"

                proto.enviar_mensaje(cliente, salida)

                return actual_path, False

            else:

                salida = (
                    "Error - El directorio especificado no existe "
                    "en el directorio actual"
                )

                proto.enviar_mensaje(cliente, salida)

                return actual_path, True

    except Exception as e:

        salida = (
            f"Excepción del lado servidor "
            f"al ejecutar cd: {str(e)}"
        )

        proto.enviar_mensaje(cliente, salida)

        return actual_path, True
def exit(cliente, clientes, socket):
    cliente.shutdown(socket.SHUT_RDWR)
    clientes.remove(cliente)
    pass