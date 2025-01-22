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

    # Función que guarda un nuevo registro en la tabla cardgame.
    # Esta función debería llamarse justo después de acabar una partida.

# 1 def insertBBDDCardgame esta ok
def insertBBDDCardgame(deck_id, num_players, num_rounds, end_time):
    try:
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game')

        if connection.is_connected():
            cursor = connection.cursor()

            query = """
                INSERT INTO games (start_time, end_time, num_players, num_rounds, id_deck)
                VALUES (NOW(), %s, %s, %s, %s);
            """
            cursor.execute(query, (end_time, num_players, num_rounds, deck_id))
            connection.commit()
            print("Game inserted successfully.")

    except Error as e:
        print(f"Error inserting the game: {e}")

    finally:
        if connection.is_connected():
            connection.close()
if __name__ == "__main__":
        try:
            # Llamamos a la función insertBBDDCardgame con parámetros de prueba
            deck_id = 2  # Ejemplo de ID de baraja
            num_players = 4  # Número de jugadores
            num_rounds = 5  # Número de rondas
            end_time = '2025-01-21 18:00:00'  # Hora de finalización de la partida (en formato de fecha y hora)

            # Llamada a la función
            insertBBDDCardgame(deck_id, num_players, num_rounds, end_time)

        except Exception as e:
            print(f"Unexpected error: {e}")

    # Función que guarda en la tabla player_game de la BBDD el diccionario
    # player_game.
    # Esta función debería llamarse justo después de acabar una partida

# 2 def insert_player_game esta ok (inserta los datos en la tabla partidas jugadores)
def insert_player_game(dni, game_id, initial_points, final_points, is_bank):
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
                INSERT INTO game_players (id_game, id_player, initial_points, final_points, is_bank)
                VALUES (%s, %s, %s, %s, %s);
            """
            # Inserta el jugador en la base de datos
            cursor.execute(query, (game_id, dni, initial_points, final_points, is_bank))
            connection.commit()
            print(f"Player {dni} inserted successfully in game {game_id}.")
            cursor.close()

    except Error as e:
        # Manejo de errores
        if "duplicate" in str(e).lower():
            print(f"Error: The player {dni} is already registered in the game {game_id}.")
        else:
            print(f"Error inserting player in game: {e}")

    finally:
        # Cierra la conexión con la base de datos
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    try:
        # Llamada a la función insert_player_game con parámetros de prueba
        dni = '419236335S'  # DNI del jugador
        game_id = 2  # ID del juego
        initial_points = 30  # Puntos iniciales del jugador
        final_points = 45  # Puntos finales del jugador
        is_bank = 0  # 0 si no es el banco, 1 si es el banco

        # Llamada a la función
        insert_player_game(dni, game_id, initial_points, final_points, is_bank)

    except Exception as e:
        print(f"Unexpected error: {e}")



# 3 def insert_player esta esta ok funcion inserta un jugador en la bbdd

import mysql.connector
from mysql.connector import Error

def insert_player(dni, player_name, risk_level, is_human):
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Verificar que risk_level es uno de los valores permitidos ('30', '40', '50')
            if risk_level not in ['30', '40', '50']:
                print(f"Error: 'risk_level' must be one of ['30', '40', '50'].")
                return

            # Insert the player into the database
            query = """
                INSERT INTO players (id_player, player_name, risk_level, is_human)
                VALUES (%s, %s, %s, %s);
            """
            # Insert the player into the database
            cursor.execute(query, (dni, player_name, risk_level, is_human))
            connection.commit()
            print(f"Player {player_name} with id_player {dni} inserted successfully.")
            cursor.close()

    except Error as e:
        # Handle duplicate player error
        if "duplicate" in str(e).lower():
            print(f"Error: The player with id_player {dni} is already registered in the database.")
        else:
            print(f"Error inserting player: {e}")

    finally:
        # Close the database connection
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    try:
        # Call the insert_player_game function with test parameters
        dni = '419236335S'  # Player's DNI
        player_name = 'pepe'  # Player's name
        risk_level = '30'  # Player's risk level (must be '30', '40', or '50')
        is_human = 1  # 1 if human, 0 if not

        # Call the function
        insert_player(dni, player_name, risk_level, is_human)

    except Exception as e:
        print(f"Unexpected error: {e}")

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
# 4 def insertBBDD_player_game_round esta ok introduce los datos de la ronda llamar al final de la ronda
import mysql.connector
from mysql.connector import Error

import mysql.connector
from mysql.connector import Error

def updateGameEndTime(id_game, end_time, num_players, num_rounds, id_deck):
    try:
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game')

        if connection.is_connected():
            cursor = connection.cursor()

            query = """
                UPDATE games
                SET end_time = %s, num_players = %s, num_rounds = %s, id_deck = %s
                WHERE id_game = %s;
            """
            cursor.execute(query, (end_time, num_players, num_rounds, id_deck, id_game))
            connection.commit()
            print("Game end time and details updated successfully.")

    except Error as e:
        print(f"Error updating the game: {e}")

    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    try:
        # Llamamos a la función updateGameEndTime con parámetros de prueba
        id_game = 50  # ID del juego a actualizar
        end_time = '2025-01-21 20:00:00'  # Hora de finalización de la partida (en formato de fecha y hora)
        num_players = 4  # Número de jugadores
        num_rounds = 5  # Número de rondas
        id_deck = 2  # Ejemplo de ID de baraja

        # Llamada a la función
        updateGameEndTime(id_game, end_time, num_players, num_rounds, id_deck)

    except Exception as e:
        print(f"Error: {e}")

def insertBBDD_player_game_round(id_round, id_player, bet, initial_points, final_points, won):
    try:
        # Establish the database connection
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Insert the round data for the player into the round_players table
            query = """
                INSERT INTO round_players (id_round, id_player, bet, initial_points, final_points, won)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE bet = %s, initial_points = %s, final_points = %s, won = %s
            """
            cursor.execute(query, (id_round, id_player, bet, initial_points, final_points, won, bet, initial_points, final_points, won))
            connection.commit()
            print(f"Round data for player {id_player} inserted or updated successfully.")

    except Error as e:
        print(f"Error inserting or updating round data: {e}")

    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    try:
        # Test the function insertBBDD_player_game_round with sample data
        id_round = 15  # Round ID
        id_player = '61930705P'  # Player's DNI (or player ID)
        bet = 100  # Bet placed by the player
        initial_points = 50  # Initial points of the player in this round
        final_points = 70  # Final points of the player in this round
        won = 1  # 1 if the player won the round, 0 if not

        # Call the function
        insertBBDD_player_game_round(id_round, id_player, bet, initial_points, final_points, won)

    except Exception as e:
        print(f"Unexpected error: {e}")


'''

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

import mysql.connector
from mysql.connector import Error


# Borrar Jugador
# 5 def removeBBDDPlayer esta ok
import mysql.connector
from mysql.connector import Error

def removePlayer():
    try:
        # Establish the database connection
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Query all players
            cursor.execute("SELECT id_player, player_name FROM players;")
            players = cursor.fetchall()

            if players:
                # Display the available players
                print("Player ID | Name")
                for player in players:
                    print(f"{player[0]} | {player[1]}")

                # Request the player ID to delete
                player_id = input("Enter the ID of the player you want to delete: ")

                # Check if the player exists in the list
                if any(player[0] == player_id for player in players):
                    # Check if the player has any related records in other tables
                    cursor.execute("""
                        SELECT COUNT(*) FROM game_players WHERE id_player = %s
                    """, (player_id,))
                    game_player_count = cursor.fetchone()[0]

                    cursor.execute("""
                        SELECT COUNT(*) FROM round_players WHERE id_player = %s
                    """, (player_id,))
                    round_player_count = cursor.fetchone()[0]

                    cursor.execute("""
                        SELECT COUNT(*) FROM card_players WHERE id_player = %s
                    """, (player_id,))
                    card_player_count = cursor.fetchone()[0]

                    # If the player has related records, prevent deletion
                    if game_player_count > 0 or round_player_count > 0 or card_player_count > 0:
                        print(f"Player with ID {player_id} cannot be deleted as they are associated with data in other parts of the system, including games, rounds, or cards.")
                    else:
                        # If no related records exist, delete the player
                        cursor.execute("DELETE FROM players WHERE id_player = %s;", (player_id,))
                        connection.commit()
                        print(f"Player with ID {player_id} deleted successfully.")
                else:
                    print("The player entered does not exist.")
            else:
                print("No players found in the database.")

    except Error as e:
        print(f"Error while deleting player: {e}")
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    try:
        # Call the removePlayer function
        removePlayer()

    except Exception as e:
        print(f"Unexpected error: {e}")

#6 def savePlayer esta ok
# Función que guarda en BBDD un nuevo jugador.
import mysql.connector
from mysql.connector import Error

def savePlayer(nif, name, risk, human):
    try:
        # Establish the database connection
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Check if the player already exists in game_players, round_players, or card_players
            cursor.execute("""
                SELECT COUNT(*) FROM game_players WHERE id_player = %s
            """, (nif,))
            game_player_count = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*) FROM round_players WHERE id_player = %s
            """, (nif,))
            round_player_count = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*) FROM card_players WHERE id_player = %s
            """, (nif,))
            card_player_count = cursor.fetchone()[0]

            # If the player is already linked to other records, do not allow insertion
            if game_player_count > 0 or round_player_count > 0 or card_player_count > 0:
                print(f"Player with ID {nif} cannot be registered because they are already linked to existing game, round, or card data.")
            else:
                # If no related records exist, insert the player into the database
                query = """
                    INSERT INTO players (id_player, player_name, risk_level, is_human)
                    VALUES (%s, %s, %s, %s);
                """
                cursor.execute(query, (nif, name, risk, human))
                connection.commit()
                print(f"Player {name} registered successfully.")

    except Error as e:
        print(f"Error saving player: {e}")

    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    try:
        # Test the function savePlayer with sample data
        nif = '72533364N'  # Player's NIF (ID)
        name = 'paco'  # Player's name
        risk = '30'  # Player's risk level ('30', '40', or '50')
        human = 1  # 1 if human, 0 if not

        # Call the function
        savePlayer(nif, name, risk, human)

    except Exception as e:
        print(f"Unexpected error: {e}")


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



# funcion ranking puntos mayor a menor y tiempo jugado
import mysql.connector
from mysql.connector import Error

# 7 getBBDDRankingPoint() esta ok

import mysql.connector
from mysql.connector import Error
# ranking por puntos opcion 1 getBBDDRankingPoints()
def getBBDDRankingPoints():
    try:
        # Conexión a la base de datos
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )

        if connection.is_connected():
            # Crear el cursor
            cursor = connection.cursor()

            # Consultar el ranking de jugadores ordenados por puntos
            query_ranking = """
                SELECT p.id_player, p.player_name, 
                       IFNULL(SUM(gp.final_points - gp.initial_points), 0) AS points
                FROM players p
                LEFT JOIN game_players gp ON p.id_player = gp.id_player
                GROUP BY p.id_player, p.player_name
                ORDER BY points DESC;
            """
            cursor.execute(query_ranking)
            players = cursor.fetchall()

            # Mostrar encabezado
            print("*" * 60)
            print(f"{' ':<20}{'Ranking by Points'}".center(40))
            print("-" * 60)
            print(f"{'ID':<20}{'Name':<30}{'Points':<10}")
            print("-" * 60)

            # Mostrar los jugadores ordenados por puntos
            for player in players:
                print(f"{player[0]:<20} {player[1]:<30} {player[2]:<10}")

            print("*" * 60)

    except Error as e:
        print(f"Error al obtener el ranking: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Conexión cerrada.")

# Código principal para ejecutar la función
if __name__ == "__main__":
    try:
        getBBDDRankingPoints()
    except Exception as e:
        print(f"Error inesperado: {e}")




import mysql.connector
from mysql.connector import Error

#ranking por minutos opcion 3 getBBDDRankingByMinutes()

def getBBDDRankingByMinutes():
    try:
        # Conexión a la base de datos
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )

        if connection.is_connected():
            # Crear el cursor
            cursor = connection.cursor()

            # Consulta para obtener jugadores y minutos jugados
            query_players = """
                SELECT p.id_player, p.player_name, 
                       IFNULL(SUM(TIMESTAMPDIFF(MINUTE, g.start_time, g.end_time)), 0) AS minutes_played
                FROM players p
                LEFT JOIN game_players gp ON p.id_player = gp.id_player
                LEFT JOIN games g ON g.id_game = gp.id_game
                GROUP BY p.id_player, p.player_name
                ORDER BY minutes_played DESC;
            """
            cursor.execute(query_players)
            players = cursor.fetchall()

            # Mostrar encabezado
            print("*" * 60)
            print(f"{' ':<20}{'Ranking by Minutes Played'}".center(40))
            print("-" * 60)
            print(f"{'ID':<20}{'Name':<30}{'Minutes Played':<10}")
            print("-" * 60)

            # Mostrar los jugadores ordenados
            for player in players:
                print(f"{player[0]:<20} {player[1]:<30} {player[2]:<10}")

            print("*" * 60)

    except Error as e:
        print(f"Error al obtener el ranking: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Conexión cerrada.")

# Ejecutar la función
if __name__ == "__main__":
    try:
        getBBDDRankingByMinutes()
    except Exception as e:
        print(f"Error inesperado: {e}")


import mysql.connector
from mysql.connector import Error

# ranking ordenado por partidas opcion 2
# ranking ordenado por partidas opcion 2
def getPlayersByGamesPlayed():
    try:
        # Conexión a la base de datos
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )

        if connection.is_connected():
            # Crear el cursor
            cursor = connection.cursor()

            # Consultar todos los jugadores ordenados por partidas jugadas
            query_players = """
                SELECT p.id_player, p.player_name, 
                       COUNT(gp.id_game) AS games_played
                FROM players p
                LEFT JOIN game_players gp ON p.id_player = gp.id_player
                GROUP BY p.id_player, p.player_name
                ORDER BY games_played DESC;
            """
            cursor.execute(query_players)
            players = cursor.fetchall()

            # Mostrar encabezado
            print("*" * 80)
            print(f"{' ':<20}{'Players Ranked by Games Played'}".center(40))
            print("-" * 80)
            print(f"{'ID':<20}{'Name':<30}{'Games Played':<15}")
            print("-" * 80)

            # Mostrar jugadores ordenados
            for player in players:
                print(f"{player[0]:<20} {player[1]:<30} {player[2]:<15}")

            print("*" * 80)

    except Error as e:
        print(f"Error al obtener jugadores: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Conexión cerrada.")

# Ejecutar la función
if __name__ == "__main__":
    try:
        getPlayersByGamesPlayed()
    except Exception as e:
        print(f"Error inesperado: {e}")

# Función que extrae los jugadores definidos en la BBDD y los almacena en el diccionario
# contextGame[“players”]

import mysql.connector
from mysql.connector import Error

# 9 def getPlayers esta ok
# Diccionario para almacenar el contexto del juego
contextGame = {}

def getPlayers():
    """Fetches players and stores them in a dictionary with id_player as the key and name as the value."""
    try:
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT id_player, player_name FROM players;")
            players = cursor.fetchall()

            # Save the players in a dictionary with id_player as the key
            contextGame["players"] = {player[0]: player[1] for player in players}
            return contextGame["players"]
    except Error as e:
        print(f"Error fetching players: {e}")
        return {}  # Return an empty dictionary in case of an error
    finally:
        if connection.is_connected():
            connection.close()


# Main code to execute the function
if __name__ == "__main__":
    try:
        # Call the function to fetch players
        players = getPlayers()

        # Check if there are players in the dictionary
        if isinstance(players, dict) and players:
            print("Players fetched:")
            for player_id, player_name in players.items():
                print(f"ID: {player_id}, Name: {player_name}")
        else:
            print("No players found or there was an error.")

    except Exception as e:
        print(f"Unexpected error: {e}")


# funcion detallada de los jugadores
import mysql.connector
from mysql.connector import Error
def getPlayerDetails():
    """Obtiene los detalles de los jugadores y los guarda en un diccionario estructurado."""
    try:
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                    j.id_player,
                    j.player_name,
                    j.is_human AS human,
                    gp.is_bank AS bank,
                    IFNULL(MAX(c.name), '') AS initial_card,  -- Cambié de card_name a name
                    rj.player_priority AS priority,  -- Cambié j.priority por rj.player_priority
                    tb.type_name AS card_type,
                    IFNULL(MAX(rj.bet), 0) AS bet,
                    IFNULL(SUM(rj.final_points - rj.initial_points), 0) AS round_points,
                    IFNULL(SUM(gp.final_points - gp.initial_points), 0) AS total_points,
                    IFNULL(GROUP_CONCAT(c.name SEPARATOR ', '), '') AS cards  -- Cambié de card_name a name
                FROM players j
                LEFT JOIN game_players gp ON j.id_player = gp.id_player
                LEFT JOIN games g ON gp.id_game = g.id_game
                LEFT JOIN round_players rj ON j.id_player = rj.id_player  -- Ahora se toma player_priority desde esta tabla
                LEFT JOIN card_players cj ON j.id_player = cj.id_player
                LEFT JOIN cards c ON cj.id_card = c.id_card
                LEFT JOIN deck_types tb ON c.id_deck_type = tb.id_deck_type
                GROUP BY j.id_player, j.player_name, j.is_human, gp.is_bank, rj.player_priority, tb.type_name
                ORDER BY j.id_player;
            """
            cursor.execute(query)
            players = cursor.fetchall()

            # Comprobación si se han obtenido jugadores
            if not players:
                print("No players found or there was an error retrieving data.")
                return {}

            # Formatear los datos como un diccionario estructurado
            contextGame["players"] = {
                player["id_player"]: {
                    "name": player["player_name"],
                    "human": bool(player["human"]),
                    "bank": bool(player["bank"]),
                    "initialCard": player["initial_card"],
                    "priority": player["priority"],
                    "type": player["card_type"],
                    "bet": player["bet"],
                    "points": player["total_points"],
                    "cards": player["cards"].split(', ') if player["cards"] else [],
                    "roundPoints": player["round_points"],
                }
                for player in players
            }
            return contextGame["players"]
    except Error as e:
        print(f"Error fetching player details: {e}")
        return {}
    finally:
        if connection.is_connected():
            connection.close()
            print("Connection closed.")


# Código principal para ejecutar la función y verificar los datos
if __name__ == "__main__":
    try:
        # Llamamos a la función para obtener los detalles de los jugadores
        players = getPlayerDetails()

        # Verificamos si se obtuvieron datos correctamente
        if isinstance(players, dict) and players:
            print("Player details retrieved successfully:")
            for player_id, details in players.items():
                print(f"\nID: {player_id}")
                for key, value in details.items():
                    print(f"  {key.capitalize()}: {value}")
        else:
            print("No players found or an error occurred.")
    except Exception as e:
        print(f"Unexpected error: {e}")

# def get_all_players():
#     try:
#         # Conexión a la base de datos
#         connection = mysql.connector.connect(
#             host='acd-game1.mysql.database.azure.com',
#             user='ACD_USER',
#             password='P@ssw0rd',
#             database='acd_game'
#         )
#
#         if connection.is_connected():
#             # Ut.clear_terminal()
#
#             cursor = connection.cursor()
#
#             # Consultar jugadores humanos
#             query_humanos = "SELECT id_jugador, nombre, nivel_riesgo FROM jugadores WHERE es_humano = TRUE;"
#             cursor.execute(query_humanos)
#             humanos = cursor.fetchall()
#
#             # Consultar jugadores bots
#             query_bots = "SELECT id_jugador, nombre, nivel_riesgo FROM jugadores WHERE es_humano = FALSE;"
#             cursor.execute(query_bots)
#             bots = cursor.fetchall()
#
#             # Imprimir encabezado
#             print("*" * 140)
#             print("*" * 140)
#             print("*" * 63 + "Select Players" + "*" * 64)
#             print(" " * 29 + "Boot Players" + " " * 29 + "||" + " " * 29 + "Human Players")
#             print("-" * 140)
#             print(
#                 "ID                  Name                     Type                     || ID                  Name                     Type")
#             print("*" * 140)
#
#             max_rows = max(len(bots), len(humanos))
#             for i in range(max_rows):
#                 bot_data = bots[i] if i < len(bots) else ("", "", "")
#                 human_data = humanos[i] if i < len(humanos) else ("", "", "")
#
#                 # Formatear las filas
#                 bot_line = f"{bot_data[0]:<20} {bot_data[1]:<25} {bot_data[2]:<25}"
#                 human_line = f"{human_data[0]:<20} {human_data[1]:<25} {human_data[2]:<25}"
#
#                 print(f"{bot_line} || {human_line}")
#
#             print("*" * 140)
#
#             opc = input("Option ( -id to remove player, -1 to exit): ")
#
#             if opc == "-1":
#                 return {"humanos": humanos, "bots": bots}
#             else:
#                 delete_player(connection, opc.strip())
#                 print(f"Jugador con ID {opc} eliminado, recarga la lista para verificar.")
#                 # Ut.clear_terminal()
#                 get_all_players()
#     except Error as e:
#         print(f"Error al listar jugadores: {e}")
#         return {"humanos": [], "bots": []}
#     finally:
#         if 'connection' in locals() and connection.is_connected():
#             connection.close()
#             print("Conexión cerrada.")
#
#

import mysql.connector
from mysql.connector import Error

def execute_query(query):
    """
    Ejecuta una consulta SQL en la base de datos y devuelve los resultados.
    :param query: La consulta SQL a ejecutar.
    :return: Lista de diccionarios con los resultados de la consulta.
    """
    try:
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )

        if connection.is_connected():
            print("Conexión exitosa a la base de datos.")
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results

    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []


import mysql.connector
import mysql.connector
from mysql.connector import Error

def card_database():
    """
    Establishes a connection to the database, retrieves the cards, and classifies them
    into three separate dictionaries based on their type (es_cards, en_cards, al_cards).

    :return: Three dictionaries with the cards in the specified format.
    """
    try:
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )

        if connection.is_connected():
            print("Successfully connected to the database.")

            cursor = connection.cursor(dictionary=True)

            query = """
            SELECT id_card, name, game_value, priority, realValue
            FROM cards
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            sp_cards = {}
            en_cards = {}
            ge_cards = {}

            for row in rows:
                card_data = {
                    "literal": row['name'],
                    "value": float(row['game_value']),
                    "priority": row['priority'],
                    "realValue": float(row['realValue'])
                }
                if row['id_card'].startswith("SP_"):
                    sp_cards[row['id_card']] = card_data
                elif row['id_card'].startswith("EN_"):
                    en_cards[row['id_card']] = card_data
                elif row['id_card'].startswith("GE_"):
                    ge_cards[row['id_card']] = card_data

            cursor.close()
            connection.close()
            print("Connection closed successfully.")

            return sp_cards, en_cards, ge_cards

    except Error as e:
        print(f"Error while retrieving cards: {e}")
        return {}, {}, {}

# Example call to the function and print the results
sp_cards, en_cards, ge_cards = card_database()

# Check if data was retrieved and print the results
if sp_cards or en_cards or ge_cards:
    print("Spanish cards:", sp_cards)
    print("English cards:", en_cards)
    print("Alemania cards:", ge_cards)
else:
    print("No cards were retrieved.")


# Función para exportar los datos a un archivo XML
import mysql.connector
import xml.etree.ElementTree as ET

# Función para exportar datos a un archivo XML
def export_to_xml(data, filename):
    root = ET.Element("Results")

    for item in data:
        record = ET.SubElement(root, "Record")
        for key, value in item.items():
            field = ET.SubElement(record, key)
            field.text = str(value)

    tree = ET.ElementTree(root)
    tree.write(filename)
    print(f"Data exported to {filename}")


# Función para obtener la carta más repetida (menu opcion 1)
def most_repeated_initial_card(cursor):
    query = """
    SELECT name, COUNT(*) AS count
    FROM cards
    GROUP BY name
    ORDER BY count DESC
    LIMIT 1;
    """
    cursor.execute(query)
    result = cursor.fetchone()
    print(f"Most Repeated Initial Card: {result[0]} with {result[1]} occurrences.")
    return [{'name': result[0], 'count': result[1]}]


# Función para obtener la apuesta más alta por partida (menu opcion 2)
def highest_bet_per_game(cursor):
    query = """
    SELECT r.id_game, p.player_name, MAX(rp.bet) AS highest_bet
    FROM round_players rp
    JOIN rounds r ON rp.id_round = r.id_round
    JOIN players p ON rp.id_player = p.id_player
    GROUP BY r.id_game, p.player_name;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    data = [{'id_game': row[0], 'player_name': row[1], 'highest_bet': row[2]} for row in results]
    print(f"Highest Bet per Game: {data}")
    return data

# Función para calcular las partidas ganadas por bots (menu opcion 5)
def games_won_by_bots(cursor):
    query = """
    SELECT g.id_game, COUNT(*) AS games_won
    FROM game_players gp
    JOIN players p ON gp.id_player = p.id_player
    JOIN games g ON gp.id_game = g.id_game
    WHERE p.is_human = 0 AND gp.is_bank = 0 AND gp.final_points =
          (SELECT MAX(gp2.final_points)
           FROM game_players gp2
           WHERE gp2.id_game = gp.id_game)
    GROUP BY g.id_game;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    data = [{'id_game': row[0], 'games_won': row[1]} for row in results]
    print(f"Games Won by Bots: {data}")
    return data

# Función para listar los usuarios que han sido banca (menu opcion 7)
def users_who_have_been_bank(cursor):
    query = """
    SELECT DISTINCT p.id_player, p.player_name
    FROM players p
    JOIN game_players gp ON p.id_player = gp.id_player
    WHERE gp.is_bank = 1;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    data = [{'id_player': row[0], 'player_name': row[1]} for row in results]
    print(f"Users Who Have Been Bank: {data}")
    return data


# Función para calcular las rondas ganadas por la banca (menu opcion 6)
def rounds_won_by_bank(cursor):
    query = """
    SELECT r.id_round, COUNT(*) AS rounds_won_by_bank
    FROM round_players rp
    JOIN rounds r ON rp.id_round = r.id_round
    JOIN players p ON rp.id_player = p.id_player
    JOIN game_players gp ON gp.id_player = p.id_player AND gp.id_game = r.id_game
    WHERE rp.won = 1 AND gp.is_bank = 1
    GROUP BY r.id_round;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    data = [{'id_round': row[0], 'rounds_won_by_bank': row[1]} for row in results]
    print(f"Rounds Won by Bank: {data}")
    return data

#  Función jugadores con mas derrotas (menu opcion 8)
def players_with_most_losses(cursor):
    query = """
    SELECT p.player_name, COUNT(*) AS total_losses
    FROM round_players rp
    JOIN players p ON rp.id_player = p.id_player
    WHERE rp.won = 0
    GROUP BY p.player_name
    ORDER BY total_losses DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    data = [{'player_name': row[0], 'total_losses': row[1]} for row in results]
    print(f"Players with the Most Losses: {data}")
    return data


# Función rondas con mas jugadores (menu opcion 9)
def rounds_with_most_players(cursor):
    query = """
    SELECT r.id_round, COUNT(rp.id_player) AS total_players
    FROM round_players rp
    JOIN rounds r ON rp.id_round = r.id_round
    GROUP BY r.id_round
    ORDER BY total_players DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    data = [{'id_round': row[0], 'total_players': row[1]} for row in results]
    print(f"Rounds with the Most Players: {data}")
    return data

# Función total apuestas por jugador (menu opcion 10)
def total_bets_by_player(cursor):
    query = """
    SELECT p.player_name, SUM(rp.bet) AS total_bets
    FROM round_players rp
    JOIN players p ON rp.id_player = p.id_player
    GROUP BY p.player_name;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    data = [{'player_name': row[0], 'total_bets': row[1]} for row in results]
    print(f"Total Bets by Player: {data}")
    return data




# Función para calcular el porcentaje de victorias por ronda (menu opcion 4)
def win_percentage_per_round(cursor):
    query = """
    SELECT r.id_round, p.player_name,
           (SUM(rp.won) / COUNT(*)) * 100 AS win_percentage
    FROM round_players rp
    JOIN rounds r ON rp.id_round = r.id_round
    JOIN players p ON rp.id_player = p.id_player
    GROUP BY r.id_round, p.player_name;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    data = [{'id_round': row[0], 'player_name': row[1], 'win_percentage': round(row[2], 2)} for row in results]
    print(f"Win Percentage per Round: {data}")
    return data


# Configuración de conexión a MySQL
config = {
    'user': 'ACD_USER',  # Usuario
    'password': 'P@ssw0rd',  # Contraseña
    'host': 'acd-game1.mysql.database.azure.com',  # Host
    'database': 'acd_game',  # Base de datos
    'port': '3306'  # Puerto
}

# Función para obtener la apuesta más baja por partida (menu opcion 3)
def lowest_bet_per_game(cursor):
    query = """
    SELECT r.id_game, p.player_name, MIN(rp.bet) AS lowest_bet
    FROM round_players rp
    JOIN rounds r ON rp.id_round = r.id_round
    JOIN players p ON rp.id_player = p.id_player
    GROUP BY r.id_game, p.player_name
    LIMIT 0, 50000;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Preparar los resultados para exportarlos a XML
    data = []
    for row in results:
        data.append({
            'id_game': row[0],
            'player_name': row[1],
            'lowest_bet': row[2]
        })

    print(f"Lowest Bet per Game: {data}")
    return data


# Bloque principal del script
try:
    # Establecer conexión a la base de datos
    conn = mysql.connector.connect(**config)
    print("Conexión exitosa")
    cursor = conn.cursor()

    # Ejecutar las funciones y exportar los resultados a XML

    total_bets_by_player_data = total_bets_by_player(cursor)
    export_to_xml(total_bets_by_player_data, "total_bets_by_player.xml")

    rounds_with_most_players_data = rounds_with_most_players(cursor)
    export_to_xml(rounds_with_most_players_data, "../XML/rounds_with_most_players.xml")

    players_with_most_losses_data = players_with_most_losses(cursor)
    export_to_xml(players_with_most_losses_data, "../XML/players_with_most_losses.xml")


    data_users_who_have_been_bank = users_who_have_been_bank(cursor)
    export_to_xml(data_users_who_have_been_bank, "../XML/users_who_have_been_bank.xml")

    data_rounds_won_by_bank = rounds_won_by_bank(cursor)
    export_to_xml(data_rounds_won_by_bank, "../XML/rounds_won_by_bank.xml")

    data_games_won_by_bots = games_won_by_bots(cursor)
    export_to_xml(data_games_won_by_bots, "../XML/games_won_by_bots.xml")

    data_win_percentage = win_percentage_per_round(cursor)
    export_to_xml(data_win_percentage, "../XML/win_percentage_per_round.xml")

    data_lowest_bet = lowest_bet_per_game(cursor)
    export_to_xml(data_lowest_bet, "../XML/lowest_bet_per_game.xml")


    most_repeated_card_data = most_repeated_initial_card(cursor)
    export_to_xml(most_repeated_card_data, "most_repeated_initial_card.xml")

    highest_bet_data = highest_bet_per_game(cursor)
    export_to_xml(highest_bet_data, "../XML/highest_bet_per_game.xml")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Cerrar conexión si está activa
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("Conexión cerrada")

# Función para obtener la apuesta más baja por partida
def lowest_bet_per_game(cursor):
    query = """
    SELECT r.id_partida, p.player_name, MIN(rp.bet) AS lowest_bet
    FROM round_players rp
    JOIN rounds r ON rp.id_round = r.id_round
    JOIN players p ON rp.id_player = p.id_player
    GROUP BY r.id_partida, p.player_name
    LIMIT 0, 50000;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Preparar los resultados para exportarlos a XML
    data = []
    for row in results:
        data.append({
            'id_partida': row[0],
            'player_name': row[1],
            'lowest_bet': row[2]
        })

    print(f"Lowest Bet per Game: {data}")
    return data