import random
import SC.Datos as Dt
import SC.Utilidad as Ut
import SC.Cabeceras as Cb
import time
import random


def playGame():
    Ut.clear_terminal()
    print(Cb.cabecera06)
    if len(Dt.context_game["game"])<2:
        print("You need 2 players to start".center(127))
        input("Press Enter to return...".center(127))
        return
    
    ID_partida =  random.randrange(100000000,999999999)
    Dt.context_game["round"] = 0  # Inicializar el contador de rondas
    resetPoints()
    
    # Repartir una carta inicial a cada jugador para establecer prioridades
    setInitialPriorities(Dt.context_game["mazo"])
    
    # Devolver las cartas iniciales al mazo (conservando el ID en "initialCard")
    returnInitialCardsToDeck()
    
    # Comenzar las rondas
    while Dt.context_game["round"] < Dt.context_game["maxRounds"] and checkMinimun2PlayerWithPoints():
        Dt.context_game["round"] += 1
        print(f" Round {Dt.context_game['round']} ".center(127,"="))
        
        # Reiniciar el historial de la ronda
        Dt.context_game["round_history"] = []
        
        # Establecer las apuestas de los jugadores al inicio de cada ronda
        setBets()
        
        # Repartir una carta a cada jugador para comenzar la ronda
        dealInitialCardToPlayers(Dt.context_game["mazo"])
        
        # Cada jugador juega su turno (excepto la banca)
        for player_id in Dt.context_game["game"]:
            if not Dt.context_game["players"][player_id]["bank"]:  # Ignorar a la banca por ahora
                if Dt.context_game["players"][player_id]["human"]:
                    humanRound(player_id, Dt.context_game["mazo"])
                else:
                    standarRound(player_id, Dt.context_game["mazo"])
        
        # La banca juega al final
        for player_id in Dt.context_game["game"]:
            if Dt.context_game["players"][player_id]["bank"]:
                if Dt.context_game["players"][player_id]["human"]:
                    humanRound(player_id, Dt.context_game["mazo"])
                else:
                    standarRound(player_id, Dt.context_game["mazo"])
                break  # Solo hay una banca, así que salimos del bucle
        
        # Distribuir puntos, eliminar jugadores sin puntos y asignar nueva banca
        distributionPointAndNewBankCandidates()
        
        # Mostrar estadísticas de la ronda
        printStats()
        Ut.clear_terminal()
        print(Cb.cabecera06)
    
    # Mostrar al ganador de la partida
    printWinner()

def setGamePriority(mazo):
    # Mezclar el mazo
    random.shuffle(mazo)
    
    # Repartir una carta a cada jugador y establecer su prioridad
    for player_id in Dt.context_game["game"]:
        # Sacar una carta del mazo
        card = mazo.pop()
        
        # Asegurarse de que `card` sea una cadena (clave válida para el diccionario)
        if isinstance(card, str):
            # Asignar la carta inicial al jugador
            Dt.context_game["players"][player_id]["initialCard"] = card
            Dt.context_game["players"][player_id]["cards"].append(card)
            Dt.context_game["players"][player_id]["roundPoints"] += Dt.context_game["cards_deck"][card]["value"]
            
            # Establecer la prioridad del jugador
            Dt.context_game["players"][player_id]["priority"] = Dt.context_game["cards_deck"][card]["priority"]
        else:
            raise ValueError(f"La carta {card} no es un valor hashable (debe ser una cadena).")
    
    # Ordenar jugadores por prioridad (de mayor a menor)
    orderPlayersByPriority(Dt.context_game["game"])
    
    # Asignar la banca al jugador con la mayor prioridad en la primera ronda
    if Dt.context_game["round"] == 1:
        # El primer jugador en la lista ordenada es el de mayor prioridad
        new_bank_id = Dt.context_game["game"][0]
        Dt.context_game["players"][new_bank_id]["bank"] = True
        print(f"{Dt.context_game['players'][new_bank_id]['name']} es la banca en esta ronda.")
        addToRoundHistory(str(f"{Dt.context_game['players'][new_bank_id]['name']} es la banca en esta ronda."))
        time.sleep(1.2)

def resetPoints():
    for player_id in Dt.context_game["players"]:
        Dt.context_game["players"][player_id]["points"] = 20
        Dt.context_game["players"][player_id]["cards"] = []
        Dt.context_game["players"][player_id]["roundPoints"] = 0

def standarRound(id, mazo):
    player = Dt.context_game["players"][id]
    
    while True:
        # Calcular la probabilidad de pasarse si pide otra carta
        probability = chanceExceedingSevenAndHalf(id, mazo)
        
        # Si la probabilidad supera el perfil de riesgo, se planta
        if probability > player["type"]:
            print(f"{player['name']} se planta con {player['roundPoints']} puntos.")
            addToRoundHistory(str(f"{player['name']} se planta con {player['roundPoints']} puntos."))
            time.sleep(1.2)
            break
        
        # Pedir una carta
        card = mazo.pop()
        player["cards"].append(card)
        player["roundPoints"] += Dt.context_game["cards_deck"][card]["value"]
        print(f"{player['name']} ha recibido: {Dt.context_game['cards_deck'][card]['literal']}")
        time.sleep(1.2)
        print(f"Puntos actuales en esta ronda: {player['roundPoints']}")
        addToRoundHistory(str(f"{player['name']} ha recibido: {Dt.context_game['cards_deck'][card]['literal']}"))
        addToRoundHistory(str(f"Puntos actuales de {player["name"]} en esta ronda: {player['roundPoints']}"))
        time.sleep(1.2)
        
        # Verificar si se ha pasado de 7.5
        if player["roundPoints"] > 7.5:
            print(f"{player['name']} se ha pasado de 7.5.")
            addToRoundHistory(str(f"{player['name']} se ha pasado de 7.5."))
            time.sleep(1.2)
            break

def humanRound(id, mazo):
    player = Dt.context_game["players"][id]
    
    while True:
        Ut.clear_terminal()
        print(Cb.cabecera06)
        # Mostrar el menú
        print(" Player Menu ".center(127,"="))
        print("1) View Stats")
        print("2) View Game Stats")
        if not player["bank"]:  # Solo mostrar la opción de apuesta si no es la banca
            print("3) Set Bet")
        print("4) Order Card")
        print("5) Automatic Play")
        print("6) Stand")
        print("7) View Round History")  # Nueva opción para ver el historial de la ronda
        option = input("Option: ")

        if option == "1":
            # Ver las estadísticas del jugador
            printPlayerStats(id)
        elif option == "2":
            # Ver las estadísticas del juego
            printStats()
        elif option == "3" and not player["bank"]:  # Solo permitir apuesta si no es la banca
            # Cambiar la apuesta
            Ut.clear_terminal()
            print(Cb.cabecera06)
            print(f" Set Bet ".center(127,"="))
            while True:
                try:
                    new_bet = int(input(f"Introduce tu nueva apuesta (máximo {player['points']}): "))
                    if new_bet > 0 and new_bet <= player["points"]:
                        player["bet"] = new_bet
                        print(f"Apuesta cambiada a {new_bet}.")
                        addToRoundHistory(str(f"Apuesta de {player["name"]} cambiada a {new_bet}."))
                        break
                    else:
                        print(f"Apuesta no válida. Debe ser un número positivo y no mayor que tus puntos actuales ({player['points']}).")
                except ValueError:
                    print("Entrada no válida. Introduce un número.")
        elif option == "4":
            Ut.clear_terminal()
            print(Cb.cabecera06)
            print(f" Round {Dt.context_game['round']} ".center(127,"="))
            # Pedir una carta
            card = mazo.pop()
            player["cards"].append(card)
            player["roundPoints"] += Dt.context_game["cards_deck"][card]["value"]
            print(f"Has recibido: {Dt.context_game['cards_deck'][card]['literal']}")
            time.sleep(1.2)
            print(f"Puntos actuales en esta ronda: {player['roundPoints']}")
            time.sleep(1.2)
            addToRoundHistory(str(f"{player["name"]} ha recibido: {Dt.context_game['cards_deck'][card]['literal']}."))
            addToRoundHistory(str(f"Puntos actuales de {player["name"]} en esta ronda: {player['roundPoints']}"))
            if player["roundPoints"] > 7.5:
                print("¡Te has pasado de 7.5!")
                time.sleep(1.2)
                addToRoundHistory(str(f"¡{player["name"]} se ha pasado de 7.5!"))
                break
        elif option == "5":
            # Jugar en modo automático (como un bot)
            Ut.clear_terminal()
            print(Cb.cabecera06)
            print(f" Round {Dt.context_game['round']} ".center(127,"="))
            print("Modo automático activado.")
            time.sleep(1.2)
            while True:
                if chanceExceedingSevenAndHalf(id, mazo) > player["type"]:
                    print("Te plantas automáticamente.")
                    addToRoundHistory(str(f"{player["name"]} se ha plantado."))
                    time.sleep(1.2)
                    break
                card = mazo.pop()
                player["cards"].append(card)
                player["roundPoints"] += Dt.context_game["cards_deck"][card]["value"]
                print(f"Has recibido: {Dt.context_game['cards_deck'][card]['literal']}")
                time.sleep(1.2)
                print(f"Puntos actuales en esta ronda: {player['roundPoints']}")
                time.sleep(1.2)
                addToRoundHistory(str(f"{player["name"]} ha recibido: {Dt.context_game['cards_deck'][card]['literal']}."))
                addToRoundHistory(str(f"Puntos actuales de {player["name"]} en esta ronda: {player['roundPoints']}"))
                if player["roundPoints"] > 7.5:
                    print("¡Te has pasado de 7.5!")
                    time.sleep(1.2)
                    addToRoundHistory(str(f"¡{player["name"]} se ha pasado de 7.5!"))
                    break
            break
        elif option == "6":
            # Plantarse
            Ut.clear_terminal()
            print(Cb.cabecera06)
            print(f" Round {Dt.context_game['round']} ".center(127,"="))
            print("Te has plantado.")
            time.sleep(1.2)
            addToRoundHistory(str(f"{player["name"]} se ha plantado."))
            break
        elif option == "7":
            # Ver el historial de la ronda
            printRoundHistory()  # Llamar a la función para mostrar el historial
        else:
            print("Opción no válida. Inténtalo de nuevo.")

def distributionPointAndNewBankCandidates():
    bank_id = None
    candidates = []
    
    # Determinar la banca actual
    for player_id in Dt.context_game["game"]:
        if Dt.context_game["players"][player_id]["bank"]:
            bank_id = player_id
            break
    
    # Si no hay banca, salir (esto no debería ocurrir)
    if not bank_id:
        print("Error: No hay banca en esta ronda.")
        return
    
    bank = Dt.context_game["players"][bank_id]
    
    # Verificar si la banca se ha pasado de 7.5
    bank_busted = bank["roundPoints"] > 7.5
    
    # Comparar la puntuación de la banca con la de cada jugador
    for player_id in Dt.context_game["game"]:
        if player_id == bank_id:
            continue  # La banca no juega contra sí misma
        
        player = Dt.context_game["players"][player_id]
        
        if player["roundPoints"] > 7.5:
            # El jugador se ha pasado
            player["points"] -= player["bet"]
            bank["points"] += player["bet"]
            print(f"{player['name']} se ha pasado y pierde {player['bet']} puntos.")
            addToRoundHistory(str(f"{player['name']} se ha pasado y pierde {player['bet']} puntos."))
            time.sleep(1.2)
        elif bank_busted:
            # La banca se ha pasado, paga a los jugadores que no se hayan pasado
            if player["roundPoints"] <= 7.5:
                player["points"] += player["bet"]
                bank["points"] -= player["bet"]
                print(f"{player['name']} gana {player['bet']} puntos porque la banca se ha pasado.")
                addToRoundHistory(f"{player['name']} gana {player['bet']} puntos porque la banca se ha pasado.")
                time.sleep(1.2)
        else:
            # La banca no se ha pasado, comparar puntuaciones
            if player["roundPoints"] == 7.5 and bank["roundPoints"] != 7.5:
                # El jugador tiene 7.5 y la banca no
                player["points"] += 2 * player["bet"]
                bank["points"] -= 2 * player["bet"]
                candidates.append(player_id)  # Añadir a candidatos a banca
                print(f"{player['name']} tiene 7.5 y gana el doble: {2 * player['bet']} puntos.")
                addToRoundHistory(str(f"{player['name']} tiene 7.5 y gana el doble: {2 * player['bet']} puntos."))
                time.sleep(1.2)
            elif player["roundPoints"] > bank["roundPoints"]:
                # El jugador tiene más puntos que la banca
                player["points"] += player["bet"]
                bank["points"] -= player["bet"]
                print(f"{player['name']} gana {player['bet']} puntos contra la banca.")
                addToRoundHistory(str(f"{player['name']} gana {player['bet']} puntos contra la banca."))
                time.sleep(1.2)
            else:
                # El jugador tiene igual o menos puntos que la banca
                player["points"] -= player["bet"]
                bank["points"] += player["bet"]
                print(f"{player['name']} pierde {player['bet']} puntos contra la banca.")
                addToRoundHistory(str(f"{player['name']} pierde {player['bet']} puntos contra la banca."))
                time.sleep(1.2)
    
    # Eliminar jugadores sin puntos
    players_to_remove = []
    for player_id in Dt.context_game["game"]:
        player = Dt.context_game["players"][player_id]
        if player["points"] <= 0:
            players_to_remove.append(player_id)
            print(f"{player['name']} se ha quedado sin puntos y ha sido eliminado.")
            addToRoundHistory(str(f"{player['name']} se ha quedado sin puntos y ha sido eliminado."))
            time.sleep(1.2)
    
    for player_id in players_to_remove:
        Dt.context_game["game"].remove(player_id)
    
    # Determinar la nueva banca si es necesario
    if candidates:
        # Elegir al candidato con mayor prioridad
        new_bank_id = max(candidates, key=lambda x: Dt.context_game["players"][x]["priority"])
        Dt.context_game["players"][new_bank_id]["bank"] = True
        if bank_id:
            Dt.context_game["players"][bank_id]["bank"] = False
        print(f"{Dt.context_game['players'][new_bank_id]['name']} es la nueva banca.")
        addToRoundHistory(str(f"{Dt.context_game['players'][new_bank_id]['name']} es la nueva banca."))
        time.sleep(1.2)
    elif bank["points"] <= 0:
        # La banca ha sido eliminada, elegir al jugador con mayor prioridad
        if Dt.context_game["game"]:
            new_bank_id = max(Dt.context_game["game"], key=lambda x: Dt.context_game["players"][x]["priority"])
            Dt.context_game["players"][new_bank_id]["bank"] = True
            print(f"{Dt.context_game['players'][new_bank_id]['name']} es la nueva banca porque la anterior fue eliminada.")
            addToRoundHistory(str(f"{Dt.context_game['players'][new_bank_id]['name']} es la nueva banca porque la anterior fue eliminada."))
            time.sleep(1.2)
    
    # Devolver las cartas de los jugadores al mazo
    for player_id in Dt.context_game["game"]:
        player = Dt.context_game["players"][player_id]
        Dt.context_game["mazo"].extend(player["cards"])  # Devolver las cartas al mazo
        player["cards"] = []  # Reiniciar las cartas del jugador
        player["roundPoints"] = 0  # Reiniciar los puntos de la ronda
    
    # Barajar el mazo para la siguiente ronda
    random.shuffle(Dt.context_game["mazo"])

def bankOrderNewCard(id, mazo):
    player = Dt.context_game["players"][id]
    
    # Si ya tiene 7.5, no pide más cartas
    if player["roundPoints"] == 7.5:
        return False
    
    # Si ya se ha pasado, no pide más cartas
    if player["roundPoints"] > 7.5:
        return False
    
    # Si no tiene 7.5, pero después de repartir puntos se quedaría sin puntos, pide carta
    if player["points"] - player["bet"] <= 0:
        return True
    
    # Si ya gana a todos los jugadores, no pide carta
    if all(player["roundPoints"] >= Dt.context_game["players"][other_id]["roundPoints"] for other_id in Dt.context_game["game"] if other_id != id):
        return False
    
    # Si no supera a ningún jugador, pide carta
    if all(player["roundPoints"] < Dt.context_game["players"][other_id]["roundPoints"] for other_id in Dt.context_game["game"] if other_id != id):
        return True
    
    # Si ya supera a algún jugador y no se queda sin puntos, pide carta según su perfil de riesgo
    probability = chanceExceedingSevenAndHalf(id, mazo)
    return probability <= player["type"]

def chanceExceedingSevenAndHalf(id, mazo):
    player = Dt.context_game["players"][id]
    remaining_cards = len(mazo)
    exceeding_cards = 0
    
    for card in mazo:
        if player["roundPoints"] + Dt.context_game["cards_deck"][card]["value"] > 7.5:
            exceeding_cards += 1
    
    if remaining_cards == 0:
        return 0  # No hay cartas restantes
    
    return (exceeding_cards / remaining_cards) * 100

def orderPlayersByPriority(listaJugadores):
    listaJugadores.sort(key=lambda x: Dt.context_game["players"][x]["priority"])

def orderPlayersByPoints(listaJugadores):
    listaJugadores.sort(key=lambda x: Dt.context_game["players"][x]["points"], reverse=True)

def printWinner():
    orderPlayersByPoints(Dt.context_game["game"])
    winner_id = Dt.context_game["game"][0]
    winner = Dt.context_game["players"][winner_id]
    Ut.clear_terminal()
    print(Cb.cabecera05)
    print(f"The winner is {winner['name']} with {winner['points']} points!".center(127))
    input("Press Enter to continue...".center(127))

def printStats(idPlayer="", titulo=""):
    Ut.clear_terminal()
    print(Cb.cabecera06)
    while True:
        print(" Game Stats ".center(127,"="))
        if titulo:
            print(titulo)

        # Definir el formato de las columnas
        header_format = "{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}"
        row_format = "{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}"

        # Mostrar el encabezado
        print(header_format.format(
            "Name", "Human", "Priority", "Type", "Bank", "Bet", "Points"
        ))

        # Determinar los jugadores a mostrar
        if idPlayer:
            # Mostrar solo un jugador específico
            players_to_show = [idPlayer]
        else:
            # Mostrar todos los jugadores en la partida (hasta un máximo de 6)
            players_to_show = Dt.context_game["game"][:6]

        # Mostrar las estadísticas de los jugadores
        for player_id in players_to_show:
            player = Dt.context_game["players"][player_id]
            print(row_format.format(
                player["name"],
                str(player["human"]),
                str(player["priority"]),
                str(player["type"]),
                str(player["bank"]),
                str(player["bet"]),
                str(player["points"])
            ))
        print()
        input("Press Enter to return...")
        break

def printPlayerStats(id):
    Ut.clear_terminal()
    print(Cb.cabecera06)
    player = Dt.context_game["players"][id]
    while True:
        print(" Player Stats ".center(127,"="))
        print(f"Name "         .ljust(14)+f"{player['name']}")
        print(f"Type: "        .ljust(14)+f"{player['type']}")
        print(f"Human: "       .ljust(14)+f"{player['human']}")
        print(f"bank: "        .ljust(14)+f"{player['bank']}")
        print(f"Initial Card: ".ljust(14)+f"{player['initialCard']}")
        print(f"Priority: "    .ljust(14)+f"{player['priority']}")
        print(f"Bet: "         .ljust(14)+f"{player['bet']}")
        print(f"Points: "      .ljust(14)+f"{player['points']}")
        print(f"Cards: "       .ljust(14)+f"{' '.join(player['cards'])}")
        print(f"Round Points: ".ljust(14)+f"{player['roundPoints']}")
        print()
        input("Press Enter to return...")
        break

def newPlayer(dni, name, profile, human):
    Dt.context_game["players"][dni] = {
        "name": name,
        "human": human,
        "bank": False,
        "initialCard": "",
        "priority": 0,
        "type": profile,
        "bet": 4,
        "points": 20,
        "cards": [],
        "roundPoints": 0
    }

def checkMinimun2PlayerWithPoints():
    players_with_points = [player_id for player_id in Dt.context_game["game"] if Dt.context_game["players"][player_id]["points"] > 0]
    return len(players_with_points) >= 2

def orderAllPlayers():
    orderPlayersByPriority(Dt.context_game["game"])
    bank_id = None
    for player_id in Dt.context_game["game"]:
        if Dt.context_game["players"][player_id]["bank"]:
            bank_id = player_id
            break
    if bank_id:
        Dt.context_game["game"].remove(bank_id)
        Dt.context_game["game"].append(bank_id)

def setBets():
    for player_id in Dt.context_game["game"]:
        player = Dt.context_game["players"][player_id]
        
        # La banca no apuesta
        if player["bank"]:
            player["bet"] = 0  # La banca no tiene apuesta
            print(f"{player['name']} es la banca y no apuesta.")
            addToRoundHistory(str(f"{player['name']} es la banca y no apuesta."))
            time.sleep(1.2)
            continue
        
        if player["human"]:
            # Jugador humano: pedir la apuesta manualmente
            while True:
                try:
                    new_bet = int(input(f"{player['name']}, introduce tu apuesta (máximo {player['points']}): "))
                    if new_bet > 0 and new_bet <= player["points"]:
                        player["bet"] = new_bet
                        addToRoundHistory(str(f"{player['name']} apuesta {new_bet} puntos."))
                        break
                    else:
                        print(f"Apuesta no válida. Debe ser un número positivo y no mayor que tus puntos actuales ({player['points']}).")
                except ValueError:
                    print("Entrada no válida. Introduce un número.")
        else:
            # Jugador bot: apostar un porcentaje de sus puntos según su perfil de riesgo
            percentage = player["type"]  # El tipo del jugador (30, 40 o 50)
            bet_amount = int(player["points"] * (percentage / 100))  # Calcular el porcentaje y truncar
            
            # Asegurarse de que la apuesta no sea 0
            if bet_amount == 0:
                bet_amount = 1  # Apostar al menos 1 punto
            
            player["bet"] = bet_amount
            print(f"{player['name']} (bot) apuesta {bet_amount} puntos.")
            addToRoundHistory(str(f"{player['name']} (bot) apuesta {bet_amount} puntos."))
            time.sleep(1.2)

def addCardsToMaze():
    for card_key in Dt.context_game["cards_deck"]:
        Dt.context_game["mazo"].append(card_key)

def setInitialPriorities(mazo):
    # Mezclar el mazo
    random.shuffle(mazo)
    
    # Repartir una carta a cada jugador y establecer su prioridad
    for player_id in Dt.context_game["game"]:
        card = mazo.pop()
        Dt.context_game["players"][player_id]["initialCard"] = card  # Guardar el ID de la carta inicial
        Dt.context_game["players"][player_id]["priority"] = Dt.context_game["cards_deck"][card]["priority"]
        Dt.context_game["players"][player_id]["realValue"] = Dt.context_game["cards_deck"][card]["realValue"]  # Guardar el valor real de la carta
    
    # Ordenar jugadores por prioridad (de menor a mayor) y, en caso de empate, por realValue (de mayor a menor)
    Dt.context_game["game"].sort(key=lambda x: (
        Dt.context_game["players"][x]["priority"],  # Prioridad ascendente (menor valor primero)
        -Dt.context_game["players"][x]["realValue"]  # realValue descendente en caso de empate
    ))
    
    # Asignar la banca al jugador con la menor prioridad (primero en la lista ordenada)
    new_bank_id = Dt.context_game["game"][0]  # El primer jugador en la lista ordenada
    Dt.context_game["players"][new_bank_id]["bank"] = True

def returnInitialCardsToDeck():
    for player_id in Dt.context_game["game"]:
        card = Dt.context_game["players"][player_id]["initialCard"]
        Dt.context_game["mazo"].append(card)  # Devolver la carta al mazo
        # No reiniciamos "initialCard", ya que queremos conservar el ID de la carta inicial

def dealInitialCardToPlayers(mazo):
    # Mezclar el mazo
    random.shuffle(mazo)
    
    # Repartir una carta a cada jugador
    for player_id in Dt.context_game["game"]:
        card = mazo.pop()
        Dt.context_game["players"][player_id]["cards"].append(card)
        Dt.context_game["players"][player_id]["roundPoints"] += Dt.context_game["cards_deck"][card]["value"]
        print(f"{Dt.context_game['players'][player_id]['name']} ha recibido: {Dt.context_game['cards_deck'][card]['literal']}")
        addToRoundHistory(str(f"{Dt.context_game['players'][player_id]['name']} ha recibido: {Dt.context_game['cards_deck'][card]['literal']}"))
        time.sleep(1.2)

def addToRoundHistory(text):
    Dt.context_game["round_history"].append(text)

def printRoundHistory():
    # Muestra el historial de la ronda con todos los detalles.
    Ut.clear_terminal()
    print(Cb.cabecera06)
    while True:
        print(f" Round {Dt.context_game["round"]} History ".center(127,"="))
        if not Dt.context_game["round_history"]:
            print("The round history is empty.")
            print()
            input("Press Enter to return...")
            break

        for entry in range(0,len(Dt.context_game["round_history"])):
            print(Dt.context_game["round_history"][entry])
        print()
        input("Press Enter to return...")
        break