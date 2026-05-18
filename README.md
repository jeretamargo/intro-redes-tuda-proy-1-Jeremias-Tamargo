# Shell Remoto Multihilo : Jeremías Tamargo

## Introducción
Este proyecto consiste en un servicio de Shell Remoto casero implementado puramente con Python, junto a sus librerías encargadas de generar hilos `threading` , crear sockets de red `sockets` y realizar acciones a nivel de sistema operativo `sys`

## Funcionamiento
El proyecto consiste en 2 scripts: uno encargado de las funcionalidades del cliente y otro de las funcionalidades del servidor:

### `cli_shell.py`
El funcionamiento paso a paso del cliente es el siguiente:
1. Crea un socket tcp con una direccion ipv4 y un puerto especifico para conectarse al servidor
2. Dentro de un bloque try-except, intenta conectarseal server, si surgiera una excpecion devuelve un mensaje de error y finaliza la ejecucion del cliente
3. Una vez generada la conexion, crea 2 hilos para los procesos recibir_salida() y enviar_comando() y procede a ejecutarlos para que funcionen en simultaneo
4. enviar_comando() ejecuta un bucle que permite al usuario enviarle comandos al servidor, si el usuario introduce el comando exit, el cliente es el que maneja la finalizacion de la conexión y la finalizacion del programa
5. recibir_salida() ejecuta un bucle que espera constantemente la llegada del output de los comandos enviados, mostrandolos en pantalla. En caso de un error del servidor, mostrara un mensaje de error y cerrará la conexion
