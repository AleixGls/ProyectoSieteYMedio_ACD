def playGame():
    # Esta es la función principal del proyecto. Una vez establecido el número de rondas, la
    # baraja con la que se va a jugar, y los jugadores que participan en la partida, ésta será
    # la función que gestione toda la partida. Para ello, hará uso de otras funciones
    # auxiliares como:
    pass

def setGamePriority(mazo):
    # Esta función establece las prioridades de los jugadores.
    # Se recibe una lista con los id’s de la baraja (mazo), se mezclan, se reparte una
    # carta a cada jugador, se ordenan la lista de jugadores de la partida
    # (contextGame[“game”]) según la carta que han recibido, y se establecen las
    # prioridades
    pass

def resetPoints():
    # Función que establece los 20 puntos iniciales en todos los jugadores.
    pass

def fill_player_game(player_game,gameID,*fields):
    # Función para insertar datos en el diccionario player_game
    pass

def fill_player_game_round(player_game_round,round,*fields):
    # Función para insertar datos en el diccionario player_game_round
    pass

def checkMinimun2PlayerWithPoints():
    # Función que verifica que al menos haya dos jugadores con puntos
    pass

def orderAllPlayers():
    # Función que ordena los jugadores de la partida (contextGame[“game”]) de forma
    # que pone la banca al principio y el resto de jugadores después, ordenados según
    # prioridad
    pass

def setBets():
    # Función que establece las apuestas de cada jugador en función del tipo de
    # jugador.
    pass

def standarRound(id, mazo):
    # Función que realiza la tirada de cartas de un jugador en función del tipo de
    # jugador que es y teniendo en cuenta si el jugador es banca o no.
    pass

def humanRound(id, mazo):
    # Función que gestiona la tirada de un jugador humano. Nos muestra el menú de
    # opciones:
    #   1)View Stats
    #   2)View Game Stats
    #   3)Set Bet
    #   4)Order Card
    #   5)Automatic Play
    #   6)Stand
    #   Option:
    # Y ejecuta la acción que elijamos
    pass

def distributionPointAndNewBankCandidates():
    # Función que realiza el reparto de puntos una vez finalizada una ronda y devuelve
    # una lista con los candidatos a la banca ( los que tienen 7,5)
    pass

def printStats(idPlayer="", titulo=""):
    # Esta función nos imprime los stats de todos los jugadores de la partida.
    pass

def orderPlayersByPriority(listaJugadores):
    # Ordenamos la lista de jugadores de la partida (contextGame[“game”]) según
    # prioridad.
    pass

def printWinner():
    # Función que muestra el ganador de la partida.
    pass

def insertBBDDCardgame(cardgame):
    # Función que guarda un nuevo registro en la tabla cardgame.
    # Esta función debería llamarse justo después de acabar una partida.
    pass

def insertBBDD_player_game(player_game,cardgame_id):
    # Función que guarda en la tabla player_game de la BBDD el diccionario
    # player_game.
    # Esta función debería llamarse justo después de acabar una partida
    pass

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

def getOpt(textOpts="", inputOptText="", rangeList=[], exceptions=[]):
    # Función para la gestión de menús. Le pasamos un texto, que nos mostrará un menú,
    # un rango de opciones válidas, y una lista de excepciones, y nos devuelve la opción
    # elegida por el usuario.
    pass

def orderPlayersByPoints(listaJugadores):
    # Función que ordena los jugadores según sus puntos.
    pass

def chanceExceedingSevenAndHalf(id, mazo):
    # Función que calcula la probabilidad de pasarse de siete y medio
    pass

def printPlayerStats(id):
    # Esta función nos muestra los stats de un jugador humano.
    #   name Mario
    #   type 40
    #   human True
    #   bank True
    #   initialCard E11
    #   priority 3
    #   bet 8
    #   points 20
    #   cards C07
    #   roundPoints 0
    pass

def logToFile(text):
    # f = open("logfileSevenAndHalf.txt", "a")
    # f.write(text)
    # f.close()
    # Esta función nos puede servir para enviar mensajes de texto al archivo
    # “logFileSevenAndHalf”, que puede sernos útil a modo de debug.
    pass

def baknOrderNewCard(id, mazo):
    # Función que evalúa si la banca pedirá una nueva carta.
    pass

def newPlayer(dni, name, profile, human):
    # Función que devuelve una tupla con dos elementos, el primero es el dni del nuevo
    # jugador, el segundo, un diccionario con las claves: name, human, bank, initialCard,
    # priority, type, bet, points, ards, roundPoints
    pass

def addRemovePlayers():
    # Función que nos muestra el menú despues de escoger la opción 1 del menu principal:
    #   1)New Human Player
    #   2)New Boot
    #   3)Show/Remove Players
    #   4)Go back
    #   Option:
    pass

def settings():
    # Función que gestiona el menú settings, donde podemos establecer los jugadores que
    # participarán en una partida, la baraja con la que se va a jugar y el número máximo de
    # rondas
    pass

def setMaxRounds():
    # Función que pide al usuario el número de rondas de la siguiente partida y lo establece
    # en el diccionario contextGame, contextGame[“maxRounds”]
    pass

def newRandomDNI():
    # Función que devuelve un dni válido con números aleatorios
    pass

def setNewPlayer(human=True):
    # Función que gestiona la creación de un nuevo jugador que insertaremos en la BBDD
    pass

def showhPlayersGame():
    # Función que muestra los jugadores seleccionados cuando estamos añadiendo
    # jugadores a la partida:
    pass

def setPlayersGame():
    # Función para establecer los jugadores que conformarán la partida siguiente
    pass

def removeBBDDPlayer():
    # Función que nos muestra los jugadores disponibles en BBDD, y elimina el que
    # seleccionemos
    pass

def printStats(idPlayer="", titulo=""):
    # Esta función nos imprime los stats de todos los jugadores de la partida.
    pass

def reports():
    # Función que nos muestra el menú de reportes, y una vez elegida una opción, el reporte
    # correspondiente
    pass

def getPlayers():
    # Función que extrae los jugadores definidos en la BBDD y los almacena en el diccionario
    # contextGame[“players”]
    pass

def setCardsDeck():
    # Elegimos una baraja, y a partir de esa baraja, establecemos el diccionario de cartas
    # contextGame["cards_deck"]
    pass

def savePlayer(nif,name,risk,human):
    # Función que guarda en BBDD un nuevo jugador.
    pass

def delBBDDPlayer(nif):
    # Función que elimina un jugador de la BBDD
    pass

def getGameId():
    # Función que devuelve un id no existente en la tabla cardgame.
    pass

def getBBDDRanking():
    # Función que crea la vista player_earnings, y retorna un diccionario con los datos de
    # ésta,
    # player_id | earnings | games_played | minutes_played.
    pass

def ranking():
    # Función queMuestra el menú del ranking y el ranking según la opción elegida
    pass

def returnListRanking(field="earnings"):
    # Función que retorna una lista con los id de jugadores del diccionario que retorna la
    # función getBBDDRanking(), ordenados según la opción del ranking elegida
    pass

print("a")