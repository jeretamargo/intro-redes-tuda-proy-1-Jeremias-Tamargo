# Shell Remoto Multihilo V3 : Jeremías Tamargo

## Introducción

Este proyecto consiste en un servicio de Shell Remoto casero implementado puramente con Python, junto a sus librerías encargadas de generar hilos `threading` , crear sockets de red `sockets`, realizar acciones a nivel de sistema operativo `sys`, autenticar usuarios mediante base de datos local con `sqlite` y cifrar el trafico mediante TLS.

## Funcionamiento Última versión (V3):

El proyecto consiste en 2 principales scripts: uno encargado de las funcionalidades del cliente y otro de las funcionalidades del servidor, luego se compone de otros 3 modulos de servidor, encargados de realizar ele nvio de datos, las operaciones de la base de datos y la ejecucion de comandos.

#### Nueva versión:
Esta 3ra versión fue refactorizada, modularizando ciertas acciones del servidor en distintos archivos y agregando las siguientes caracterisitcas:
- Cifrado de trafico mediante TLS (Llave y certificado incluido para prueba rápida)
- Comando `cd` agregado
- Autenticacion mediante base de datos local
- Hashing y salting de contraseñas
- Sincronización de procesos (Thread Lock)
- Sanitización de entradas para evitar path traversal (Solo disponible en `cd ..`)
  
### `cli_shell.py`

El funcionamiento paso a paso del cliente es el siguiente:

1. Crea un socket tcp con una dirección ipv4 y un puerto especifico para conectarse al servidor
3. Dentro de un bloque try-except, intenta conectarse al server, si surgiera una excpeción devuelve un mensaje de error y finaliza la ejecucion del cliente
4. Una vez generada la conexion, se ejecuta el metodo `autenticar()` el cual es un bucle donde el usuario debe enviar sus credenciales, el bucle se corta cuando el servidor envía la bandera @uservalid, una vez recibida la bandera, se procede a ejecutar el metodo `enviar_comando()`
5. `enviar_comando()` ejecuta un bucle que permite al usuario enviarle comandos al servidor, si el usuario introduce el comando exit, el cliente es el que maneja la finalizacion de la conexión y la finalizacion del programa, un try-excpet maneja un posible error en el envío

### `srv_shell.py`

El funcionamiento paso a paso del servidor es el siguiente:

1. El server crea una conexión tcp y relaciona este socket con la ip de la interfaz y el puerto donde recibira las peticiones de los clientes
2. Se crea un contexto SLL y carga tanto la llave privada como el certificado
3. El servidor se pone a la escucha y a continuacion ejecuta la funcion `recibir_conexiones()`

4.`recibir_conexiones()`  ejecuta un bucle que primero asegura que la cantidad maxima de conexiones sea hasta 5, si en el array de clientes conectados hay un total de 5, acepta (envolviendolo en el contexto cifrado) al cliente pero para mandar un mensaje de conexión fallida, terminando por cerrar la conexión
En el caso se ser menos de 5 clientes totales, el servidor acepta al cliente,envuelve la conexion en el contexto de cifrado y loguea en la consola la conexion, agrega al nuevo cliente al array de clientes y genera un hilo nuevo para validar al usuario con la funcion `autenticar()`

5. `autenticar()` utiliza dos bucles, uno primero para validar de que el usuario exista dentro del array de usuarios validos, y una vez habiendo validado el usuario, pasa a verificar con el segundo bucle que la contraseña de el usuario indicado se valida, si se falla una cantidad total de 3 veces en la ejecucion de los 2 bucles, se cierra la conexion con el usuario, si el usuario logra completar exitosamente la validación, el servidor envía la bandera @uservalid para avisar al cliente que la validación fue exitosa y procede a crear un nuevo hilo para ejecutar la función `ejecutar_comando(cliente, address)`

6. La funcion `ejecutar_comando(cliente, address)` recibe la funcionalidad de el socket del cliente y su socket en formato string (para poder loguear en consola de manera mas legible).
   Esta funcion se encarga de recibir los comandos enviados por el cliente, parsearlos para eliminar espacios a los costados y compraralos mediante un match, que se encarga de verificar cual es el comando pedido por el cliente.
   
7. En el caso de que el cliente se desconecte o surja un error dentro de la función ejecutar_comandos(), se eliminara al cliente del array de clientes y finalmente se cerrará la conexion con el socket

### db.py
Este script es el encargado de crear la base de datos y cargar los usuarios (no es necesario si se clona el proyecto, debido a que ya esta creada y cargada), buscar usuaurios y verificar las contraseñas de los mismos, usado mediante el proceso de autenticación en el script de servidor, en la función `autenticar()` 

### protocolo.py
Este script es usado tanto en el cliente como el servidor para todas las transferencias de datos y contiene 2 funciones:
`enviar_mensaje`: Es una funcion que recibe al cliente a envíar el mensaje y el respectivo mensaje. Su objetivo es calcular el tamaño del mensaje, agregarlo como cabecera y enviar el mensaje al receptor.
`recibir_mensaje`: Esta funcion recibe al cliente y a el mensaje del cliente. Primero recibe la cabecera, lee el tamaño del paquete, y mediante uj bucle procede a reconstruir el mensaje hasta recibirlo entero, para finalmente devolver la salida completa

### `comandos.py`
Este script contiene modularizados en funciones los comandos usados por el script de servidor, dentro de `ejecutar_comando(cliente, address)`

- En el caso de un `exit`, se apaga el socket del cliente y se elimina al cliente del array de clientes

- En el caso de un `ls`, se divide el comando en la cantidad de partes que posea y se utiliza la funcion `os.listdir()` para traer la lista de archivos y directorios actuales, si existen, los separa con salto de linea mediante un join() y los envia, de lo contrario, envia un mensaje indicando que el directorio esta vacio.
  Las variantes de `ls` son `ls -l` , `ls -lh ` o `ls -hl ` y las mismas junto a un directorio, especifico (`ls *directorio* -l ` /`ls *directorio* -lh `), en estas variantes se utilizan métodos para obtener más informacion sobre los archivos (`os.scandir`, `stat()` ) para extraer informacion detallada de cada archivo y también se usa la función `human_read()` para convertir los tamaños de archivos a un resultado mas legible en unidades

- En el caso de un `pwd`, se usa la funcion `os.getcwd()`, se guarda en una variable y se envía al cliente

- En el caso de un `cat *archivo*`, es necesario primero dividir el comando en 2, para separar el comando del argumento. Dentro de un try-except utilizamos split y dividimos el comando en el primer espacio que encuentre para poder acceder al argumento. Una vez, obtenido el argumento, utilizamos la funcion open() para abrir el archivo, le pasamos el argumento anteriormente extraido del comando (nombre del archivo), la funcion de lectura (r) y el formato en el que queremos leer (utf-8), finalmente guardamos el contenido del archivo con la funcion .read() y se lo enviamos al cliente. Este bloque utiliza un with para manejar automaticamente el cerrado del archivo luego de utilizarlo. Luego le siguen dos except que manejan casos de error en donde el archivo no exista o suceda alguna otra excepcion del S.O

- En el caso de un `help` se devuelve la ayuda de los comandos disponibles en el servidor, sus variantes son la ayuda extendida del uso y funcionamiento de los diferentes comandos que provee el servidor (`help cat / help ls / help pwd etc`)

- En el caso de un `mkdir` se crea una carpeta en la raiz del servidor, primero se extrae el argumento (nombre de nueva carpeta), luego se arma el path donde sera creado uniendo el directorio actual del servidor y el nombre de la nueva carpeta, finalmente, con el metodo `os.mkdir(path)` se crea la carpeta con el nombre enviado por el cliente

- En el caso de un `cd`, se extrae el argumento y primero se valida que sea un `..`, si es así, se cambia automaticamente al directorio padre la variable `actual_path`, si es otro directorio, se valida que el directorio exista en la carpeta actual y se cambia la variable `actual_path` al directorio especificado

- Si ninguno el comando enviado por el cliente no entra en ninguno de los 3 casos anteriores, el servidor envía un mensaje de error indicando que el comando recibido no es reconocido




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

openssl req -x509 -newkey rsa:2048 -nodes -days 365 -keyout key.pem -out cert.pem
