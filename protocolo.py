import struct

def enviar_mensaje(cliente,mensaje):

    data = mensaje.encode("utf-8")

    longitud = len(data)

    cabecera = struct.pack("!I",longitud) #con struct creamos el header junto a la longitud del mensaje

    cliente.sendall(cabecera + data) #procura enviar todos los datos


def recibir_mensaje(cliente):
    cabecera = cliente.recv(4) #recibimos la cabecera

    longitud = struct.unpack("!I",cabecera)[0] #desesctructuramos la cabecera y nso quedamos con la longitud del mensaje

    data = b"" #data codificada

    while len(data) < longitud: #bucle que recibe toda la data hasta llegar al tamaño de total del paquete (longitud recibida en la cabecera)

        fragmento = cliente.recv(longitud - len(data))

        data += fragmento

    return data.decode("utf-8")