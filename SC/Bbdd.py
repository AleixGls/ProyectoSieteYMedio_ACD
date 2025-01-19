import mysql.connector
import SC.Utilidad as Ut
from mysql.connector import Error
import SC.Cabeceras as Cb
import time



def insertBBDDCardgame(cardgame):
    # Función que guarda un nuevo registro en la tabla cardgame.
    # Esta función debería llamarse justo después de acabar una partida.
    pass

def insertBBDD_player_game(player_game,cardgame_id):
     #Función que guarda en la tabla player_game de la BBDD el diccionario
     #player_game.
     #Esta función debería llamarse justo después de acabar una partida
    pass

def savePlayer(dni, nombre, risk, human):
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
            print(f"Player {nombre} con ID {dni} inserted correctly.".center(127))
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

def getBBDDRanking():
    # Función que crea la vista player_earnings, y retorna un diccionario con los datos de
    # ésta,
    # player_id | earnings | games_played | minutes_played.
    pass

def getPlayers():
    # Función que extrae los jugadores definidos en la BBDD y los almacena en el diccionario
    # contextGame[“players”]
    pass

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
            query_humanos = "SELECT id_jugador, nombre, nivel_riesgo FROM jugadores WHERE es_humano = TRUE;"
            cursor.execute(query_humanos)
            humanos = cursor.fetchall()
            
            # Consultar jugadores bots
            query_bots = "SELECT id_jugador, nombre, nivel_riesgo FROM jugadores WHERE es_humano = FALSE;"
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
        query = "DELETE FROM jugadores WHERE id_jugador = %s;"
        cursor.execute(query, (id_jugador,))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Player with ID {id_jugador} successfully removed.".center(127))
            time.sleep(1)
        else:
            print(f"No player found with ID {id_jugador}.".center(127))
            time.sleep(1)
    except Error as e:
        print(f"Error when deleting player: {e}".center(127))
        time.sleep(1)
