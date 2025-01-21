cartas_es = {}
cartas_en = {}
cartas_al = {}

context_game = {
    "cards_deck":{}, #Baraja de cartas seleccionada
    "mazo":[],       #Mazo de carta de la partida
    
    "players":{        
        "11115555A":{
            "name":"Mario",
            "human":True,
            "bank":False,
            "initialCard":"",
            "priority":0,
            "type":40,
            "bet":4,
            "points":0,
            "cards":[],
            "roundPoints":0
        },
        "22225555A":{
            "name":"Pepe",
            "human":False,
            "bank":False,
            "initialCard":"",
            "priority":0,
            "type":30,
            "bet":4,
            "points":0,
            "cards":[],
            "roundPoints":0
        },
        "33335555A":{
            "name":"Jose1",
            "human":False,
            "bank":False,
            "initialCard":"",
            "priority":0,
            "type":50,
            "bet":4,
            "points":0,
            "cards":[],
            "roundPoints":0
        },
        "44445555A":{
            "name":"Jose2",
            "human":False,
            "bank":False,
            "initialCard":"",
            "priority":0,
            "type":50,
            "bet":4,
            "points":0,
            "cards":[],
            "roundPoints":0
        },
        "55555555A":{
            "name":"Jose3",
            "human":False,
            "bank":False,
            "initialCard":"",
            "priority":0,
            "type":50,
            "bet":4,
            "points":0,
            "cards":[],
            "roundPoints":0
        },        
        "66665555A":{
            "name":"Jose4",
            "human":False,
            "bank":False,
            "initialCard":"",
            "priority":0,
            "type":50,
            "bet":4,
            "points":0,
            "cards":[],
            "roundPoints":0
        },
        "77775555A":{
            "name":"Jose5",
            "human":False,
            "bank":False,
            "initialCard":"",
            "priority":0,
            "type":50,
            "bet":4,
            "points":0,
            "cards":[],
            "roundPoints":0
        },
    },    #Jugadores extraidos de la base de datos
    "game":[],       #Jugadores en partida

    "round":0,      #Ronda actual
    "maxRounds":5,   #Rondas maximas de la partida
    "round_history":[]
}