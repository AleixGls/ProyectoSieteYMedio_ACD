import mysql.connector
import SC.Utilidad as Ut
from mysql.connector import Error
import xml.etree.ElementTree as ET
import SC.Datos as Dt
import SC.Cabeceras as Cb
import time
import os



def savePlayer(dni, player_name, risk_level, is_human):
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

            if risk_level not in ['30', '40', '50']:
                print(f"Error: 'risk_level' must be one of ['30', '40', '50'].".center(127))
                return
            
            query = """
                INSERT INTO players (id_player, player_name, risk_level, is_human)
                VALUES (%s, %s, %s, %s);
            """
            # Inserta el jugador en la base de datos
            cursor.execute(query, (dni, player_name, risk_level, is_human))
            connection.commit()
            print(f"Player {player_name} con ID {dni} inserted correctly.".center(127))
            cursor.close()
            time.sleep(1)
            
    except Error as e:
        # Manejando el error de duplicidad del id_jugador
        if "duplicate" in str(e).lower():
            print(f"Error: The ID {dni} it is already registered in the database.".center(127))
        else:
            print(f"Error inserting player: {e}".center(127))

    finally:
        # Cierra la conexión con la base de datos
        if connection.is_connected():
            connection.close()
            player_database()


def removeBBDDPlayer():
    try:
        # Conexión a la base de datos
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )
        
        if connection.is_connected():
            Ut.clear_terminal()

            cursor = connection.cursor()
            
            # Consultar jugadores humanos
            query_humanos = "SELECT id_player, player_name, risk_level FROM players WHERE is_human = TRUE;"
            cursor.execute(query_humanos)
            humanos = cursor.fetchall()
            
            # Consultar jugadores bots
            query_bots = "SELECT id_player, player_name, risk_level FROM players WHERE is_human = FALSE;"
            cursor.execute(query_bots)
            bots = cursor.fetchall()
            
            # Imprimir encabezado
            print(Cb.cabecera01)
            print( "Select Players ".center(127,"="))
            print("Bot Players".center(63) + "|"+"Human Players".center(63))
            print("-"*127)
            print("ID".center(21)+"Name".center(21)+"Type".center(21)+"|"+"ID".center(21)+"Name".center(21)+"Type".center(21))
            print("-"*127)

            # Combinar y mostrar datos de bots y humanos
            max_rows = max(len(bots), len(humanos))
            for i in range(max_rows):
                # Obtener los datos de cada lista
                bot_data = bots[i] if i < len(bots) else ("", "", "")
                human_data = humanos[i] if i < len(humanos) else ("", "", "")
                
                # Formatear las filas
                bot_line = f"{bot_data[0].center(21)}{bot_data[1].center(21)}{bot_data[2].center(21)}"
                human_line = f"{human_data[0].center(21)}{human_data[1].center(21)}{human_data[2].center(21)}"
                
                print(f"{bot_line}|{human_line}")
            
            print()
            print("0) Leave this menu".center(127)) 
            
            # Entrada del usuario para eliminar jugador
            opc = input("Write the ID of the player you want do delete: ".rjust(88))
            
            if opc == "0":
                return {"humanos": humanos, "bots": bots}
            else:
                delBBDDPlayer(connection, opc.strip())                
                Ut.clear_terminal()
                removeBBDDPlayer()

    except Error as e:
        print(f"Error listing players: {e}".center(127))
        return {"humanos": [], "bots": []}
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            player_database()
            

# Función para eliminar jugador
def delBBDDPlayer(connection, id_jugador):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM players WHERE id_player = %s;"
        cursor.execute(query, (id_jugador,))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Player with ID {id_jugador} successfully removed.".center(127))
            time.sleep(1)
        else:
            print(f"No player found with ID {id_jugador}.".center(127))
            time.sleep(1)
    except Error as e:
        print(f"Error when deleting player: This player had matches played. You can't delete this user".center(127))
        input("Enter to continue... ".center(127))
        time.sleep(1)

def card_database():
    # Establece una conexión con la base de datos, recupera las tarjetas y las clasifica
    # en tres diccionarios separados en función de su tipo (es_cards, en_cards, al_cards).
    # Return: Tres diccionarios con las tarjetas en el formato especificado.

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
            SELECT id_card, name, game_value, priority, realValue
            FROM cards
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                card_data = {
                    "literal": row['name'],
                    "value": float(row['game_value']),
                    "priority": row['priority'],
                    "realValue": float(row['realValue'])
                }
                if row['id_card'].startswith("SP_"):
                    Dt.cartas_es[row['id_card']] = card_data
                elif row['id_card'].startswith("EN_"):
                    Dt.cartas_en[row['id_card']] = card_data
                elif row['id_card'].startswith("GE_"):
                    Dt.cartas_al[row['id_card']] = card_data

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Error while retrieving cards: {e}".center(127))

def player_database():
    # Inicializar el diccionario con "players" vacío y "game" como una lista vacía
    Dt.context_game = {
        "cards_deck":{},    #Baraja de cartas seleccionada
        "mazo":[],          #Mazo de carta de la partida

        "players":{},       #Jugadores extraidos de la base de datos
        "game":[],          #Jugadores en partida

        "round":0,          #Ronda actual
        "maxRounds":5,      #Rondas maximas de la partida
        "round_history":[]  #Historial de la ronda
    }
    
    try:
        # Conexión a la base de datos
        connection = mysql.connector.connect(
            host='acd-game1.mysql.database.azure.com',
            user='ACD_USER',
            password='P@ssw0rd',
            database='acd_game'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Consultar jugadores
            query_players = "SELECT id_player, player_name, risk_level, is_human FROM players;"
            cursor.execute(query_players)
            players = cursor.fetchall()
            
            # Añadir cada jugador al diccionario context_game
            for player in players:
                id_player, player_name, risk_level, is_human = player
                Dt.context_game["players"][id_player] = {
                    "name": player_name,
                    "human": bool(is_human),
                    "bank": False,
                    "initialCard": "",
                    "priority": 0,
                    "type": int(risk_level),
                    "bet": 0,
                    "points": 0,
                    "cards": [],
                    "roundPoints": 0
                }
            
            cursor.close()
            connection.close()
            Dt.context_game["cards_deck"] = Dt.cartas_es
            
    except Error as e:
        print(f"Error while importing players: {e}".center(127))
        return None  # Retornar None en caso de error
    


# Función para exportar datos a un archivo XML
def export_to_xml(data, filename):
    # Define la ruta de la carpeta ../XML
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'XML')
    
    # Crea la carpeta si no existe
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Define la ruta completa del archivo
    file_path = os.path.join(folder_path, filename)
    
    # Crea el elemento raíz
    root = ET.Element("Results")

    # Recorre los datos y crea los elementos XML
    for item in data:
        record = ET.SubElement(root, "Record")
        for key, value in item.items():
            field = ET.SubElement(record, key)
            field.text = str(value)

    # Crea el árbol XML y escribe el archivo
    tree = ET.ElementTree(root)
    tree.write(file_path)
    
    # Imprime un mensaje centrado
    print(f"Data exported to {file_path}".center(127))
    time.sleep(1)
    



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
    return data

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
    return data

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
            while True:
                Ut.clear_terminal()
                print(Cb.cabecera03)
                print(' Ranking by Points '.center(127))
                print("-" * 127)
                print('ID'.center(42)+'Name'.center(43)+'Points'.center(42))
                print("-" * 127)

                # Mostrar los jugadores ordenados por puntos
                for player in players:
                    print(f"{player[0]}".center(42)+f"{player[1]}".center(43)+f"{player[2]}".center(42))
                print()
                input("Press Enter to continue...".center(127))
                break

    except Error as e:
        print(f"Error obtaining ranking: {e}".center(127))
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

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
            while True:
                Ut.clear_terminal()
                print(Cb.cabecera03)
                print(' Players Ranked by Games Played '.center(127))
                print("-" * 127)
                print('ID'.center(42)+'Name'.center(43)+'Games Played'.center(42))
                print("-" * 127)

                # Mostrar jugadores ordenados
                for player in players:
                    print(f"{player[0]}".center(42) + f"{player[1]}".center(43) + f"{player[2]}".center(42))
                print()
                input("Press Enter to continue...".center(127))
                break

    except Error as e:
        print(f"Error getting players: {e}".center(127))
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

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

            while True:
                # Mostrar encabezado
                Ut.clear_terminal()
                print(Cb.cabecera03)
                print(' Ranking by Minutes Played '.center(127))
                print("-" * 127)
                print('ID'.center(42)+'Name'.center(43)+'Minutes Played'.center(42))
                print("-" * 127)

                # Mostrar los jugadores ordenados
                for player in players:
                    print(f"{player[0]}".center(42)+f"{player[1]}".center(43)+f"{player[2]}".center(42))

                print()
                input("Press Enter to continue...".center(127))
                break

    except Error as e:
        print(f"Error obtaining ranking: {e}".center(127))
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

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


    except Error as e:
        print(f"Error inserting the game: {e}".center(127))

    finally:
        if connection.is_connected():
            connection.close()

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
            cursor.close()

    except Error as e:
        # Manejo de errores
        if "duplicate" in str(e).lower():
            print(f"Error: The player {dni} is already registered in the game {game_id}.".center(127))
        else:
            print(f"Error inserting player in game: {e}".center(127))

    finally:
        # Cierra la conexión con la base de datos
        if connection.is_connected():
            connection.close()

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

    except Error as e:
        print(f"Error inserting or updating round data: {e}".center(127))

    finally:
        if connection.is_connected():
            connection.close()

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

    except Error as e:
        print(f"Error updating the game: {e}".c)

    finally:
        if connection.is_connected():
            connection.close()
