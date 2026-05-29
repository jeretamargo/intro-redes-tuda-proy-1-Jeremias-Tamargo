import sqlite3
import bcrypt

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

def crear_bd():

    conn = sqlite3.connect("usuarios.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    conn.commit()

    for username, password in usuarios.items():
        agregar_usuario(
            username,
            password
        )

    conn.close()

def agregar_usuario(username, password):

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    conn = sqlite3.connect("usuarios.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO usuarios(
            username,
            password_hash
        )
        VALUES (?,?)
        """,
        (
            username,
            password_hash.decode()
        )
    )

    conn.commit()
    conn.close()

def buscar_usuario(username):
    conn = sqlite3.connect("usuarios.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username, password_hash  
        FROM usuarios
        WHERE username = ?
        """,
        (username,)
    )

    usuario = cursor.fetchone() # si hay un usuario lo devuelve, sino, devuelve NONE

    conn.close()

    return usuario
    

def verificar_contraseña(usuario, password):
    password_hash = usuario[1]
    return bcrypt.checkpw(
        password.encode(),
        password_hash.encode()
    )
    