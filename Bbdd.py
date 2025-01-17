


def insertBBDDCardgame(cardgame):
    # Función que guarda un nuevo registro en la tabla cardgame.
    # Esta función debería llamarse justo después de acabar una partida.
    pass

def insertBBDD_player_game(player_game,cardgame_id):
    # Función que guarda en la tabla player_game de la BBDD el diccionario
    # player_game.
    # Esta función debería llamarse justo después de acabar una partida
    pass
# #def insert_player_game(dni, nombre, nivel_riesgo, es_humano):
#     try:
#         # Conecta a la base de datos
#         connection = connect_to_database()
#         if connection:
#             cursor = connection.cursor()
#             query = """
#                 INSERT INTO jugadores (dni, nombre, nivel_riesgo, es_humano)
#                 VALUES (%s, %s, %s, %s);
#                 """
#             # consulta si el dni existe
#             cursor.execute(query, (dni, nombre, nivel_riesgo, es_humano))
#             connection.commit()
#             print(f"Jugador {nombre} con DNI {dni} insertado correctamente.")
#             cursor.close()
#
#     except Error as e:
#         # dni ya registrado
#         if "duplicate" in str(e).lower():
#             print(f"Error: El DNI {dni} ya está registrado en la base de datos.")
#         else:
#             print(f"Error al insertar jugador: {e}")
#
#     finally:
#         # cierra la conexion con la base de datos
#         if connection and connection.is_connected():
#             connection.close()














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