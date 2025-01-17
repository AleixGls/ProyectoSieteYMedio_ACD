import Datos as Dt


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

def printStats(idPlayer="", titulo=""):
    # Esta función nos imprime los stats de todos los jugadores de la partida.
    pass

def printWinner():
    # Función que muestra el ganador de la partida.
    pass

def printPlayerStats(id):
    print(
    f"""
    Name:         {Dt.players[id]["name"]}
    Type:         {Dt.players[id]["type"]}
    Human:        {Dt.players[id]["human"]}
    Bank:         {Dt.players[id]["bank"]}
    Initial Card: {Dt.players[id]["initialCard"]}
    Priority:     {Dt.players[id]["priority"]}
    Bet:          {Dt.players[id]["bet"]}
    Points:       {Dt.players[id]["points"]}
    Cards:        {", ".join(Dt.players[id]["cards"])}
    Round Points: {Dt.players[id]["roundPoints"]}
    """
    )

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

def showhPlayersGame():
    print("Actual Players In Game".center(72,"*"))
    for i in range(0,len(Dt.context_game["game"])):
        player_id    = Dt.context_game["game"][i]
        player_name  = Dt.context_game["players"][Dt.context_game["game"][i]]["name"]
        if Dt.context_game["players"][Dt.context_game["game"][i]]["human"] == True:
            player_human = "Human"
        else:
            player_human = "Bot"

        if   Dt.context_game["players"][Dt.context_game["game"][i]]["type"] == 30:
            player_type = "Cautious"
        elif Dt.context_game["players"][Dt.context_game["game"][i]]["type"] == 40:
            player_type = "Moderated"
        elif Dt.context_game["players"][Dt.context_game["game"][i]]["type"] == 50:
            player_type = "Bold"
        else:
            player_type = "ERROR"

        print(player_id.ljust(18) + player_name.ljust(18) + player_human.ljust(18) + player_type.ljust(18))

def setMaxRounds():
    # Función que pide al usuario el número de rondas de la siguiente partida y lo establece
    # en el diccionario contextGame, contextGame[“maxRounds”]
    pass

def printStats(idPlayer="", titulo=""):
    # Esta función nos imprime los stats de todos los jugadores de la partida.
    pass

def setNewPlayer(human=True):
    # Función que gestiona la creación de un nuevo jugador que insertaremos en la BBDD
    pass

def setPlayersGame():
    # Función para establecer los jugadores que conformarán la partida siguiente
    pass

def ranking():
    # Función queMuestra el menú del ranking y el ranking según la opción elegida
    pass

def reports():
    # Función que nos muestra el menú de reportes, y una vez elegida una opción, el reporte
    # correspondiente
    pass