import random

def newRandomDNI():
    num = random.randint(10000000, 99999999)
    letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
    letra = letras[num % 23]
    dni = f"{num}{letra}"
    return dni

def logToFile(text):
    f = open("logfileSevenAndHalf.txt", "a")
    f.write(text)
    f.close()

def setCardsDeck():
    # Elegimos una baraja, y a partir de esa baraja, establecemos el diccionario de cartas
    # contextGame["cards_deck"]
    pass

def chanceExceedingSevenAndHalf(id, mazo):
    # Función que calcula la probabilidad de pasarse de siete y medio
    pass

def orderPlayersByPoints(listaJugadores):
    # Función que ordena los jugadores según sus puntos.
    pass

def orderPlayersByPriority(listaJugadores):
    # Ordenamos la lista de jugadores de la partida (contextGame[“game”]) según
    # prioridad.
    pass