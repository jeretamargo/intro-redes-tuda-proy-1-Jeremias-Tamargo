# Shell Remoto Multihilo : Jeremías Tamargo

## Introducción
Este proyecto consiste en un servicio de Shell Remoto casero implementado puramente con Python, junto a sus librerías encargadas de generar hilos `threading` , crear sockets de red `sockets` y realizar acciones a nivel de sistema operativo `sys`

## Funcionamiento
El proyecto consiste en 2 scripts: uno encargado de las funcionalidades del cliente y otro de las funcionalidades del servidor:

### `cli_shell.py`
El funcionamiento paso a paso del cliente es el siguiente:

1. Crea un socket tcp con una dirección ipv4 y un puerto especifico para conectarse al servidor
2. Dentro de un bloque try-except, intenta conectarse al server, si surgiera una excpeción devuelve un mensaje de error y finaliza la ejecucion del cliente
3. Una vez generada la conexion, crea 2 hilos para los procesos `recibir_salida()` y `enviar_comando()` y procede a ejecutarlos para que funcionen en simultaneo
4. `enviar_comando()` ejecuta un bucle que permite al usuario enviarle comandos al servidor, si el usuario introduce el comando exit, el cliente es el que maneja la finalizacion de la conexión y la finalizacion del programa, un try-excpet maneja un posible error en el envío
5. `recibir_salida()` ejecuta un bucle que espera constantemente la llegada del output de los comandos enviados, mostrandolos en pantalla.  un try-except maneja un posible error de servidor al intentar recibir la salida, mostrando un mensaje de error y cerrando la conexión

### `srv_shell.py`
El funcionamiento paso a paso del servidor es el siguiente:

1.El server crea una conexión tcp y relaciona este socket con la ip de la interfaz y el puerto donde recibira las peticiones de los clientes

2.El servidor se pone a la escucha y a continuacion ejecuta la funcion `recibir_conexiones()`

3.`recibir_conexiones()` ejecuta un bucle que primero asegura que la cantidad maxima de conexiones sea hasta 5, si en el array de clientes conectados hay un total de 5, el servidor acepta al cliente pero para mandar un mensaje de conexión fallida, terminando por cerrar la conexión
En el caso se ser menos de 5 clientes totales, el servidor acepta al cliente, loguea en la consola la conexion, agrega al nuevo cliente al array de clientes y genera un hilo nuevo para poder ejecutar sus comandos con la funcion `ejecutar_comando(cliente, address)`

4. La funcion `ejecutar_comando(cliente, address)` recibe la funcionalidad de el socket del cliente y su socket en formato string (para poder loguear en consola de manera mas legible).
Esta funcion se encarga de recibir los comandos enviados por el cliente, parsearlos para eliminar espacios a los costados y compraralos mediante un match, que se encarga de verificar cual es el comando pedido por el cliente:
  - En el caso de un `ls`, se utiliza la funcion `os.listdir()` para traer la lista de archivos y directorios actuales, si existen, los separa con salto de linea mediante un join() y los envia, de lo contrario, envia un mensaje indicando que el directorio esta vacio
  - En el caso de un `pwd`, se usa la funcion `os.getcwd()`, se guarda en una variable y se envía al cliente
  - En el caso de un `cat *archivo*`, es necesario primero dividir el comando en 2, para separar el comando del argumento. Dentro de un try-except utilizamos split y dividimos el comando en el primer espacio que encuentre para poder acceder al argumento. Una vez, obtenido el argumento, utilizamos la funcion open() para abrir el archivo, le pasamos el argumento anteriormente extraido del comando (nombre del archivo), la funcion de lectura (r) y el formato en el que queremos leer (utf-8), finalmente guardamos el contenido del archivo con la funcion .read() y se lo enviamos al cliente. Este bloque utiliza un with para manejar automaticamente el cerrado del archivo luego de utilizarlo. Luego le siguen dos except que manejan casos de error en donde el archivo no exista o suceda alguna otra excepcion del S.O
  - Si ninguno el comando enviado por el cliente no entra en ninguno de los 3 casos anteriores, el servidor envía un mensaje de error indicando que el comando recibido no es reconocido

5. En el caso de que el cliente se desconecte o surja un error dentro de la función ejecutar_comandos(), se eliminara al cliente del array de clientes y finalmente se cerrará la conexion con el socket

## Prueba
Para probar el shell remoto:

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/jeretamargo/intro-redes-tuda-proy-1-Jeremias-Tamargo.git
   ```
   
2. ejecutar en terminales separadas, primer el script del servidor, y en segundo lugar, el script del cliente
 ```bash
   python proy-1-srv_shell.py
   python proy-1-cli_shell.py
   ```



