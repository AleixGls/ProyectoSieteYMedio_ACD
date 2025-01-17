import mysql.connector
from mysql.connector import Error


config = {
    'user': 'ACD_USER',
    'password': 'P@ssw0rd',
    'host': 'acd-game1.mysql.database.azure.com',
    'database': 'acd_game',
    'port': '3306'
}

try:
    conn = mysql.connector.connect(**config)
    print("Conexión exitosa")
    
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")  
    print("Tablas en la base de datos:")
    for table in cursor:
        print(table)
    
    cursor.execute("SELECT DATABASE()") 
    current_db = cursor.fetchone()
    print(f"Base de datos actual: {current_db[0]}")
    
except mysql.connector.Error as err:
    if err.errno == Error.ER_ACCESS_DENIED_ERROR:
        print("Algo está mal con tu usuario o contraseña")
    elif err.errno == Error.ER_BAD_DB_ERROR:
        print("La base de datos no existe")
    else:
        print(err)
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Conexión cerrada")

def insertBBDDCardgame(cardgame):
    # Función que guarda un nuevo registro en la tabla cardgame.
    # Esta función debería llamarse justo después de acabar una partida.
    pass

def insertBBDD_player_game(player_game,cardgame_id):
     #Función que guarda en la tabla player_game de la BBDD el diccionario
     #player_game.
     #Esta función debería llamarse justo después de acabar una partida
    pass
import mysql.connector
from mysql.connector import Error

def insert_player_game(dni, nombre, risk, human):
    try:
        # Conecta a la base de datos
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            query = """
                INSERT INTO jugadores (id_jugador, nombre, nivel_riesgo, es_humano)
                VALUES (%s, %s, %s, %s);
            """
            # Inserta el jugador en la base de datos
            cursor.execute(query, (dni, nombre, risk, human))
            connection.commit()
            print(f"Jugador {nombre} con id_jugador {dni} insertado correctamente.")
            cursor.close()

    except Error as e:
        # Manejando el error de duplicidad del id_jugador
        if "duplicate" in str(e).lower():
            print(f"Error: El id_jugador {dni} ya está registrado en la base de datos.")
        else:
            print(f"Error al insertar jugador: {e}")

    finally:
        # Cierra la conexión con la base de datos
        if connection.is_connected():
            connection.close()

def insertBBDD_player_game_round(player_game_round,cardgame_id):
    # Función que guarda en la tabla player_game_round de la BBDD el diccionario
    # player_game_round.
    # Esta función debería llamarse justo después de acabar una partida.

    # Una posible estrategia para esta función sería:
    # Establecer prioridades de los jugadores
    # Resetear puntos
    # Crear diccionarios cardgame,player_game,player_game_round
    # Crear un id de partida
    # Mientras hayan dos jugadores o más con puntos, y no nos pasemos del máximo de
    # rondas:
    # Ordenar jugadores, banca al final y resto de prioridad menor a mayor.
    #   Crear una lista con los id’s de cartas ( mazo).
    #   Barajar el mazo.
    #   Establecer apuestas
    #   Ejecutar jugadas de cada jugador.
    #   Repartir puntos.
    #   Eliminar los jugadores sin puntos.
    #   Establecer nueva banca si es necesario.
    # Insertar en BBDD los diccionarios creados para tal propósito.
    # Mostrar el ganador.
    pass

def removeBBDDPlayer():
    # Función que nos muestra los jugadores disponibles en BBDD, y elimina el que
    # seleccionemos
    pass

def savePlayer(nif,name,risk,human):
    # Función que guarda en BBDD un nuevo jugador.
    pass

def delBBDDPlayer(nif):
    # Función que elimina un jugador de la BBDD
    pass

def getBBDDRanking():
    # Función que crea la vista player_earnings, y retorna un diccionario con los datos de
    # ésta,
    # player_id | earnings | games_played | minutes_played.
    pass

def getPlayers():
    # Función que extrae los jugadores definidos en la BBDD y los almacena en el diccionario
    # contextGame[“players”]
    pass