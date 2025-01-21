import mysql.connector
import SC.Utilidad as Ut
from mysql.connector import Error
import SC.Datos as Dt
import SC.Cabeceras as Cb
import time



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
            
    except Error as e:
        print(f"Error while importing players: {e}".center(127))
        return None  # Retornar None en caso de error