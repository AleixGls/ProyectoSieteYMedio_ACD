cartas_es = {}
cartas_en = {}
cartas_al = {}

context_game = {
    "cards_deck":{},    #Baraja de cartas seleccionada
    "mazo":[],          #Mazo de carta de la partida

    "players":{},       #Jugadores extraidos de la base de datos
    "game":[],          #Jugadores en partida

    "round":0,          #Ronda actual
    "maxRounds":5,      #Rondas maximas de la partida
    "round_history":[]  #Historial de la ronda
}