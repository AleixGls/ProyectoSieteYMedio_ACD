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

def distributionPointAndNewBankCandidates():
    # Función que realiza el reparto de puntos una vez finalizada una ronda y devuelve
    # una lista con los candidatos a la banca ( los que tienen 7,5)
    pass

def orderPlayersByPriority(listaJugadores):
    # Ordenamos la lista de jugadores de la partida (contextGame[“game”]) según
    # prioridad.
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

def newRandomDNI():
    # Función que devuelve un dni válido con números aleatorios
    pass

def setCardsDeck():
    # Elegimos una baraja, y a partir de esa baraja, establecemos el diccionario de cartas
    # contextGame["cards_deck"]
    pass

def getGameId():
    # Función que devuelve un id no existente en la tabla cardgame.
    pass

def returnListRanking(field="earnings"):
    # Función que retorna una lista con los id de jugadores del diccionario que retorna la
    # función getBBDDRanking(), ordenados según la opción del ranking elegida
    pass

print("a")