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



#def insertBBDDCardgame(cardgame):
    # Función que guarda un nuevo registro en la tabla cardgame.
    # Esta función debería llamarse justo después de acabar una partida.

def insertBBDDCardgame(baraja_id, num_jugadores, num_rondas, hora_fin):
    try:
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game')

        if connection.is_connected():
            cursor = connection.cursor()

            query = """
                INSERT INTO partidas (hora_inicio, hora_fin, num_jugadores, num_rondas, id_baraja)
                VALUES (NOW(), %s, %s, %s, %s);
            """
            cursor.execute(query, (hora_fin, num_jugadores, num_rondas, baraja_id))
            connection.commit()
            print("Partida insertada correctamente.")

    except Error as e:
        print(f"Error al insertar la partida: {e}")

    finally:
        if connection.is_connected():
            connection.close()




'''
#def insertBBDD_player_game(player_game,cardgame_id):
     #Función que guarda en la tabla player_game de la BBDD el diccionario
     #player_game.
     #Esta función debería llamarse justo después de acabar una partida
'''

def insertBBDD_player_game(id_partida, id_jugador, puntos_iniciales, puntos_finales, es_banca):
    try:
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game')
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            query = """
                INSERT INTO partidas_jugadores (id_partida, id_jugador, puntos_iniciales, es_banca)
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(query, (id_partida, id_jugador, puntos_iniciales, puntos_finales, es_banca))
            connection.commit()
            print(f"Jugador {id_jugador} insertado correctamente en la partida {id_partida}.")
            
    except Error as e:
        print(f"Error al insertar jugador en la partida: {e}")
    
    finally:
        if connection.is_connected():
            connection.close()



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

#def insertBBDD_player_game_round(player_game_round,cardgame_id):
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



import mysql.connector
from mysql.connector import Error

def insertBBDD_player_game_round(id_ronda, id_jugador, apuesta, puntos_inicio, puntos_fin, gano):
    try:
        # Establecer la conexión con la base de datos
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Verificar si el registro ya existe
            cursor.execute("""
                SELECT * FROM rondas_jugadores 
                WHERE id_ronda = %s AND id_jugador = %s
            """, (id_ronda, id_jugador))

            result = cursor.fetchone()

            if result:
                # Si el registro existe, actualizamos los valores
                query = """
                    UPDATE rondas_jugadores 
                    SET apuesta = %s, puntos_inicio = %s, puntos_fin = %s, gano = %s
                    WHERE id_ronda = %s AND id_jugador = %s
                """
                cursor.execute(query, (apuesta, puntos_inicio, puntos_fin, gano, id_ronda, id_jugador))
                connection.commit()
                print(f"Registro de ronda para el jugador {id_jugador} actualizado correctamente.")
            else:
                # Si el registro no existe, lo insertamos
                query = """
                    INSERT INTO rondas_jugadores (id_ronda, id_jugador, apuesta, puntos_inicio, puntos_fin, gano)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (id_ronda, id_jugador, apuesta, puntos_inicio, puntos_fin, gano))
                connection.commit()
                print(f"Datos de ronda para el jugador {id_jugador} insertados correctamente.")

    except Error as e:
        print(f"Error al insertar o actualizar los datos de ronda: {e}")

    finally:
        if connection.is_connected():
            connection.close()



'''
****
#inserte tanto los datos de la partida como de la ronda, de acuerdo con la lógica de las partidas y las rondas.
def insertBBDD_player_game_round(player_game_round, partida_id):
    # player_game_round es un diccionario con la información de la ronda y los jugadores
    try:
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Se insertan primero los datos de la partida y luego de la ronda.
            query_partida = """
                INSERT INTO partidas (hora_inicio, num_jugadores, num_rondas, id_baraja)
                VALUES (NOW(), %s, %s, %s);
            """
            cursor.execute(query_partida,
                           (player_game_round["num_jugadores"], player_game_round["num_rondas"], partida_id))
            connection.commit()

            # Insertar datos de cada jugador en la ronda
            for jugador in player_game_round["jugadores"]:
                insert_player_game_round(player_game_round["ronda_id"], jugador["id"], jugador["apuesta"],
                                         jugador["puntos_iniciales"], jugador["puntos_finales"], jugador["gano"])

            print("Datos de partida y ronda insertados correctamente.")

    except Error as e:
        print(f"Error al insertar datos de partida y ronda: {e}")

    finally:
        if connection.is_connected():
            connection.close()
*****
'''
#def removeBBDDPlayer():
    # Función que nos muestra los jugadores disponibles en BBDD, y elimina el que
    # seleccionemos


import mysql.connector
from mysql.connector import Error

# Borrar Jugador

def removeBBDDPlayer():
    try:
        # Establecer la conexión con la base de datos
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )
        if connection.is_connected():
            cursor = connection.cursor()

            # Consultar todos los jugadores
            cursor.execute("SELECT id_jugador, nombre FROM jugadores;")
            jugadores = cursor.fetchall()

            if jugadores:
                # Mostrar los jugadores disponibles
                print("ID Jugador | Nombre")
                for jugador in jugadores:
                    print(f"{jugador[0]} | {jugador[1]}")

                # Solicitar el ID del jugador a eliminar
                jugador_id = input("Introduce el ID del jugador que deseas eliminar: ")

                # Verificar si el jugador existe en la lista
                if any(jugador[0] == jugador_id for jugador in jugadores):
                    # Eliminar el jugador de la base de datos
                    cursor.execute("DELETE FROM jugadores WHERE id_jugador = %s;", (jugador_id,))
                    connection.commit()
                    print(f"Jugador con ID {jugador_id} eliminado correctamente.")
                else:
                    print("El jugador ingresado no existe.")
            else:
                print("No hay jugadores en la base de datos.")

    except Error as e:
        print(f"Error al eliminar jugador: {e}")
    finally:
        if connection.is_connected():
            connection.close()


    # Función que guarda en BBDD un nuevo jugador.


def savePlayer(nif, name, risk, human):
    try:
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
            cursor.execute(query, (nif, name, risk, human))
            connection.commit()
            print(f"Jugador {name} registrado correctamente.")
    except Error as e:
        print(f"Error al guardar jugador: {e}")
    finally:
        if connection.is_connected():
            connection.close()

'''
Funcion duplicada con remove

#def delBBDDPlayer(nif):
    # Función que elimina un jugador de la BBDD


def delBBDDPlayer(nif):
    try:
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("DELETE FROM jugadores WHERE id_jugador = %s;", (nif,))
            connection.commit()
            print(f"Jugador con ID {nif} eliminado correctamente.")
    except Error as e:
        print(f"Error al eliminar jugador: {e}")
    finally:
        if connection.is_connected():
            connection.close()


#def getBBDDRanking():
    # Función que crea la vista player_earnings, y retorna un diccionario con los datos de
    # ésta,
    # player_id | earnings | games_played | minutes_played.
'''


import mysql.connector
from mysql.connector import Error
import time


def getBBDDRanking():
    try:
        # Conexión a la base de datos
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )

        if connection.is_connected():
            # Creamos el cursor
            cursor = connection.cursor()

            # Consultar jugadores (humanos y bots)
            query_players = """
                          SELECT j.id_jugador, j.nombre, 
                          IFNULL(SUM(pj.puntos_finales - pj.puntos_iniciales), 0) AS puntos
                          FROM jugadores j
                          LEFT JOIN partidas_jugadores pj ON j.id_jugador = pj.id_jugador
                          GROUP BY j.id_jugador, j.nombre
                          ORDER BY puntos DESC;
                      """
            cursor.execute(query_players)
            players = cursor.fetchall()

            # Ordenar los jugadores por puntos (nivel_riesgo) de mayor a menor
            players_sorted = sorted(players, key=lambda x: x[2], reverse=True)

            # Mostrar título centrado
            print("*" * 140)
            print(f"{' ' * 50}{'Ranking'.center(40)}")
            print("-" * 140)
            print(f"{'ID':<20}{'Name':<30}{'Points':<10}")
            print("-" * 140)

            # Mostrar los jugadores ordenados
            for player in players_sorted:
                print(f"{player[0]:<20} {player[1]:<30} {player[2]:<10}")

            print("*" * 140)

    except Error as e:
        print(f"Error al obtener jugadores o ranking: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Conexión cerrada.")

    # Código principal para ejecutar la función


if __name__ == "__main__":
    try:
        # Llamamos a la función de jugadores y ranking
        getBBDDRanking()

    except Exception as e:
        print(f"Error inesperado: {e}")

'''

#def getPlayers():
    # Función que extrae los jugadores definidos en la BBDD y los almacena en el diccionario
    # contextGame[“players”]
'''

import mysql.connector
from mysql.connector import Error

# Diccionario para almacenar el contexto del juego
contextGame = {}

import mysql.connector
from mysql.connector import Error

# Diccionario para almacenar el contexto del juego
contextGame = {}


def getPlayers():
    """Obtiene los jugadores y los guarda en un diccionario con id_jugador como clave y nombre como valor."""
    try:
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT id_jugador, nombre FROM jugadores;")
            players = cursor.fetchall()

            # Guardar los jugadores en un diccionario con id_jugador como clave
            contextGame["players"] = {player[0]: player[1] for player in players}
            return contextGame["players"]
    except Error as e:
        print(f"Error al obtener jugadores: {e}")
        return {}  # Devolver un diccionario vacío en caso de error
    finally:
        if connection.is_connected():
            connection.close()


# Código principal para ejecutar la función
if __name__ == "__main__":
    try:
        # Llamamos a la función para obtener los jugadores
        players = getPlayers()

        # Verificamos si hay jugadores en el diccionario
        if isinstance(players, dict) and players:
            print("Jugadores obtenidos:")
            for player_id, player_name in players.items():
                print(f"ID: {player_id}, Nombre: {player_name}")
        else:
            print("No se han encontrado jugadores o hay un error.")

    except Exception as e:
        print(f"Error inesperado: {e}")

import mysql.connector
from mysql.connector import Error

import mysql.connector
from mysql.connector import Error

def get_all_players():
    try:
        # Conexión a la base de datos
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )
        
        if connection.is_connected():
            #Ut.clear_terminal()

            cursor = connection.cursor()
            
            # Consultar jugadores humanos
            query_humanos = "SELECT id_jugador, nombre, nivel_riesgo FROM jugadores WHERE es_humano = TRUE;"
            cursor.execute(query_humanos)
            humanos = cursor.fetchall()
            
            # Consultar jugadores bots
            query_bots = "SELECT id_jugador, nombre, nivel_riesgo FROM jugadores WHERE es_humano = FALSE;"
            cursor.execute(query_bots)
            bots = cursor.fetchall()
            
            # Imprimir encabezado
            print("*" * 140)
            print(" " * 35 + " _____  __                            ____                                         ____   __")
            print(" " * 34 + "/ ___/ / /_   ____  _      __        / __ \\ ___   ____ ___   ____  _   __ ___     / __ \\ / /____ _ __  __ ___   _____ _____")
            print(" " * 33 + "\\__ \\ / __ \\ / __ \\| | /| / /______ / /_/ // _ \\ / __ `__ \\ / __ \\| | / // _ \\   / /_/ // // __ `// / / // _ \\ / ___// ___/")
            print(" " * 33 + "___/ // / / // /_/ /| |/ |/ //_____// _, _//  __// / / / / // /_/ /| |/ //  __/  / ____// // /_/ // /_/ //  __// /   (__  )")
            print(" " * 32 + "/____//_/ /_/ \\____/ |__/|__/       /_/ |_| \\___//_/ /_/ /_/ \\____/ |___/ \\___/  /_/    /_/ \\__,_/ \\__, / \\___//_/   /____/")
            print(" " * 96 + "/____/")
            print("*" * 140)
            print("*" * 63 + "Select Players" + "*" * 64)
            print(" " * 29 + "Boot Players" + " " * 29 + "||" + " " * 29 + "Human Players")
            print("-" * 140)
            print("ID                  Name                     Type                     || ID                  Name                     Type")
            print("*" * 140)

            # Combinar y mostrar datos de bots y humanos
            max_rows = max(len(bots), len(humanos))
            for i in range(max_rows):
                # Obtener los datos de cada lista
                bot_data = bots[i] if i < len(bots) else ("", "", "")
                human_data = humanos[i] if i < len(humanos) else ("", "", "")
                
                # Formatear las filas
                bot_line = f"{bot_data[0]:<20} {bot_data[1]:<25} {bot_data[2]:<25}"
                human_line = f"{human_data[0]:<20} {human_data[1]:<25} {human_data[2]:<25}"
                
                print(f"{bot_line} || {human_line}")
            
            print("*" * 140)
            
            # Entrada del usuario para eliminar jugador
            opc = input("Option ( -id to remove player, -1 to exit): ")
            
            if opc == "-1":
                return {"humanos": humanos, "bots": bots}
            else:
                delete_player(connection, opc.strip())
                print(f"Jugador con ID {opc} eliminado, recarga la lista para verificar.")
                #Ut.clear_terminal()
                get_all_players()
    except Error as e:
        print(f"Error al listar jugadores: {e}")
        return {"humanos": [], "bots": []}
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Conexión cerrada.")


# Función para eliminar jugador
def delete_player(connection, id_jugador):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM jugadores WHERE id_jugador = %s;"
        cursor.execute(query, (id_jugador,))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Jugador con ID {id_jugador} eliminado correctamente.")
        else:
            print(f"No se encontró ningún jugador con ID {id_jugador}.")
    except Error as e:
        print(f"Error al eliminar jugador: {e}")
