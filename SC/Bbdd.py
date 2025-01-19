import mysql.connector
import SC.Utilidad as Ut
from mysql.connector import Error
import SC.Datos as Dt
import SC.Cabeceras as Cb
import time



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
            Dt.context_game["players"] = {player[0]: player[1] for player in players}
            return Dt.context_game["players"]
    except Error as e:
        print(f"Error al obtener jugadores: {e}")
        return {}  # Devolver un diccionario vacío en caso de error
    finally:
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
