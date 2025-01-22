import random
import SC.Datos as Dt
import SC.Utilidad as Ut
import SC.Cabeceras as Cb
import SC.Bbdd as Bd
import time



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
    Bd.player_database()

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
            raise ValueError(f"The card {card} is not a hashable value (it must be a string).".center(127))
    
    # Ordenar jugadores por prioridad (de mayor a menor)
    orderPlayersByPriority(Dt.context_game["game"])
    
    # Asignar la banca al jugador con la mayor prioridad en la primera ronda
    if Dt.context_game["round"] == 1:
        # El primer jugador en la lista ordenada es el de mayor prioridad
        new_bank_id = Dt.context_game["game"][0]
        Dt.context_game["players"][new_bank_id]["bank"] = True
        print(f"{Dt.context_game['players'][new_bank_id]['name']} is the bank in this round.".center(127))
        addToRoundHistory(str(f"{Dt.context_game['players'][new_bank_id]['name']} is the bank in this round."))
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
            print(f"{player['name']} stands with {player['roundPoints']} points.".center(127))
            addToRoundHistory(str(f"{player['name']} stands with {player['roundPoints']} points."))
            time.sleep(1.2)
            break
        
        # Pedir una carta
        card = mazo.pop()
        player["cards"].append(card)
        player["roundPoints"] += Dt.context_game["cards_deck"][card]["value"]
        print(f"{player['name']} has received: {Dt.context_game['cards_deck'][card]['literal']}".center(127))
        time.sleep(1.2)
        print(f"Current points in this round: {player['roundPoints']}".center(127))
        addToRoundHistory(str(f"{player['name']} has received: {Dt.context_game['cards_deck'][card]['literal']}"))
        addToRoundHistory(str(f"Current points of {player["name"]} in this round: {player['roundPoints']}"))
        time.sleep(1.2)
        
        # Verificar si se ha pasado de 7.5
        if player["roundPoints"] > 7.5:
            print(f"{player['name']} has passed above 7.5.".center(127))
            addToRoundHistory(str(f"{player['name']} has passed above 7.5."))
            time.sleep(1.2)
            break

def humanRound(id, mazo):
    player = Dt.context_game["players"][id]
    
    while True:
        Ut.clear_terminal()
        print(Cb.cabecera06)
        # Mostrar el menú
        print(" Player Menu ".center(127,"="))
        print(" " * 53 + "1) View Stats".ljust(127))
        print(" " * 53 + "2) View Game Stats".ljust(127))
        if not player["bank"]:  # Solo mostrar la opción de apuesta si no es la banca
            print(" " * 53 + "3) Set Bet".ljust(127))
        print(" " * 53 + "4) Order Card".ljust(127))
        print(" " * 53 + "5) Automatic Play".ljust(127))
        print(" " * 53 + "6) Stand".ljust(127))
        print(" " * 53 + "7) View Round History".ljust(127))  # Nueva opción para ver el historial de la ronda
        print()
        option = input(" " * 57 + "Option: ")

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
                    new_bet = int(input(f"Enter your new bet (Max {player['points']}): ".rjust(77)))
                    if new_bet > 0 and new_bet <= player["points"]:
                        player["bet"] = new_bet
                        print(f"Bet changed to {new_bet}.".center(127))
                        addToRoundHistory(str(f"Bet of {player["name"]} changed to {new_bet}."))
                        break
                    else:
                        print(f"Invalid bet. Must be a positive number and not greater than your current points ({player['points']}).".center(127))
                        time.sleep(1.2)
                except ValueError:
                    print("Invalid entry. Enter a number.".center(127))
                    time.sleep(1.2)
        elif option == "4":
            Ut.clear_terminal()
            print(Cb.cabecera06)
            print(f" Round {Dt.context_game['round']} ".center(127,"="))
            # Pedir una carta
            card = mazo.pop()
            player["cards"].append(card)
            player["roundPoints"] += Dt.context_game["cards_deck"][card]["value"]
            print(f"You have received: {Dt.context_game['cards_deck'][card]['literal']}".center(127))
            time.sleep(1.2)
            print(f"Current points in this round: {player['roundPoints']}".center(127))
            time.sleep(1.2)
            addToRoundHistory(str(f"{player["name"]} has received: {Dt.context_game['cards_deck'][card]['literal']}."))
            addToRoundHistory(str(f"Current points of {player["name"]} in this round: {player['roundPoints']}"))
            if player["roundPoints"] > 7.5:
                print("You went over 7.5!".center(127))
                time.sleep(1.2)
                addToRoundHistory(str(f"{player["name"]} has exceeded 7.5!"))
                break
        elif option == "5":
            # Jugar en modo automático (como un bot)
            Ut.clear_terminal()
            print(Cb.cabecera06)
            print(f" Round {Dt.context_game['round']} ".center(127,"="))
            print("Automatic mode enabled.".center(127))
            time.sleep(1.2)
            while True:
                if chanceExceedingSevenAndHalf(id, mazo) > player["type"]:
                    print("You stand automatically.".center(127))
                    addToRoundHistory(str(f"{player["name"]} has standed."))
                    time.sleep(1.2)
                    break
                card = mazo.pop()
                player["cards"].append(card)
                player["roundPoints"] += Dt.context_game["cards_deck"][card]["value"]
                print(f"You have received: {Dt.context_game['cards_deck'][card]['literal']}".center(127))
                time.sleep(1.2)
                print(f"Current points in this round: {player['roundPoints']}".center(127))
                time.sleep(1.2)
                addToRoundHistory(str(f"{player["name"]} has received: {Dt.context_game['cards_deck'][card]['literal']}."))
                addToRoundHistory(str(f"Current points of {player["name"]} in this round: {player['roundPoints']}"))
                if player["roundPoints"] > 7.5:
                    print("You exceeded 7.5!".center(127))
                    time.sleep(1.2)
                    addToRoundHistory(str(f"{player["name"]} has exceeded 7.5!"))
                    break
            break
        elif option == "6":
            # Plantarse
            Ut.clear_terminal()
            print(Cb.cabecera06)
            print(f" Round {Dt.context_game['round']} ".center(127,"="))
            print("You standed.".center(127))
            time.sleep(1.2)
            addToRoundHistory(str(f"{player["name"]} has standed."))
            break
        elif option == "7":
            # Ver el historial de la ronda
            printRoundHistory()  # Llamar a la función para mostrar el historial
        else:
            print("Invalid option. Please try again.".center(127))
            time.sleep(1.2)

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
        print("Error: There is no bank in this round.".center(127))
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
            print(f"{player['name']} has exceded and losses {player['bet']} points.".center(127))
            addToRoundHistory(str(f"{player['name']} has exceded and losses {player['bet']} points."))
            time.sleep(1.2)
        elif bank_busted:
            # La banca se ha pasado, paga a los jugadores que no se hayan pasado
            if player["roundPoints"] <= 7.5:
                player["points"] += player["bet"]
                bank["points"] -= player["bet"]
                print(f"{player['name']} wins {player['bet']} points because the bank has exceded.".center(127))
                addToRoundHistory(f"{player['name']} wins {player['bet']} points because the bank has exceded.")
                time.sleep(1.2)
        else:
            # La banca no se ha pasado, comparar puntuaciones
            if player["roundPoints"] == 7.5 and bank["roundPoints"] != 7.5:
                # El jugador tiene 7.5 y la banca no
                player["points"] += 2 * player["bet"]
                bank["points"] -= 2 * player["bet"]
                candidates.append(player_id)  # Añadir a candidatos a banca
                print(f"{player['name']} has 7.5 and earns double: {2 * player['bet']} points.".center(127))
                addToRoundHistory(str(f"{player['name']} has 7.5 and earns double: {2 * player['bet']} points."))
                time.sleep(1.2)
            elif player["roundPoints"] > bank["roundPoints"]:
                # El jugador tiene más puntos que la banca
                player["points"] += player["bet"]
                bank["points"] -= player["bet"]
                print(f"{player['name']} wins {player['bet']} points against the bank.".center(127))
                addToRoundHistory(str(f"{player['name']} wins {player['bet']} points against the bank."))
                time.sleep(1.2)
            else:
                # El jugador tiene igual o menos puntos que la banca
                player["points"] -= player["bet"]
                bank["points"] += player["bet"]
                print(f"{player['name']} losses {player['bet']} points against the bank.".center(127))
                addToRoundHistory(str(f"{player['name']} losses {player['bet']} points against the bank."))
                time.sleep(1.2)
    
    # Eliminar jugadores sin puntos
    players_to_remove = []
    for player_id in Dt.context_game["game"]:
        player = Dt.context_game["players"][player_id]
        if player["points"] <= 0:
            players_to_remove.append(player_id)
            print(f"{player['name']} has run out of points and has been eliminated.".center(127))
            addToRoundHistory(str(f"{player['name']} has run out of points and has been eliminated."))
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
        print(f"{Dt.context_game['players'][new_bank_id]['name']} is the new bank.".center(127))
        addToRoundHistory(str(f"{Dt.context_game['players'][new_bank_id]['name']} is the new bank."))
        time.sleep(1.2)
    elif bank["points"] <= 0:
        # La banca ha sido eliminada, elegir al jugador con mayor prioridad
        if Dt.context_game["game"]:
            new_bank_id = max(Dt.context_game["game"], key=lambda x: Dt.context_game["players"][x]["priority"])
            Dt.context_game["players"][new_bank_id]["bank"] = True
            print(f"{Dt.context_game['players'][new_bank_id]['name']} is the new bank because the previous one was eliminated.".center(127))
            addToRoundHistory(str(f"{Dt.context_game['players'][new_bank_id]['name']} is the new bank because the previous one was eliminated."))
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

        # Mostrar el encabezado
        print("Name".center(16) + "Human".center(16) +  "Priority".center(15) +  "Type".center(16) + "Bank".center(16) + "Bet".center(16) + "Points".center(16) + "Round Points".center(16))
        print("-"*127)
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
            print(player["name"].center(16) + str(player["human"]).center(16) + str(player["priority"]).center(15) + str(player["type"]).center(16) + str(player["bank"]).center(16) + str(player["bet"]).center(16) + str(player["points"]).center(16) +  str(player["roundPoints"]).center(16))
        print()
        input("Press Enter to return...".center(127))
        break

def printPlayerStats(id):
    Ut.clear_terminal()
    print(Cb.cabecera06)
    player = Dt.context_game["players"][id]
    while True:
        print(" Player Stats ".center(127,"="))
        print(str(f"Name: {player['name']}").center(127))
        print(str(f"Type: {player['type']}").center(127))
        print(str(f"Human: {player['human']}").center(127))
        print(str(f"bank: {player['bank']}").center(127))
        print(str(f"Initial Card: {player['initialCard']}").center(127))
        print(str(f"Priority: {player['priority']}").center(127))
        print(str(f"Bet: {player['bet']}").center(127))
        print(str(f"Points: {player['points']}").center(127))
        print(str(f"Cards: {' '.join(player['cards'])}").center(127))
        print(str(f"Round Points: {player['roundPoints']}").center(127))
        print()
        input("Press Enter to return...".center(127))
        break

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
            print(f"{player['name']} is the bank and does not bet.".center(127))
            addToRoundHistory(str(f"{player['name']} is the bank and does not bet."))
            time.sleep(1.2)
            continue
        
        if player["human"]:
            # Jugador humano: pedir la apuesta manualmente
            while True:
                try:
                    new_bet = int(input(f"{player['name']}, enter your bet (Max {player['points']}): ".rjust(80)))
                    if new_bet > 0 and new_bet <= player["points"]:
                        player["bet"] = new_bet
                        addToRoundHistory(str(f"{player['name']} bets {new_bet} points."))
                        break
                    else:
                        print(f"Invalid bet. Must be a positive number and not greater than your current points ({player['points']}).".center(127))
                except ValueError:
                    print("Invalid entry. Enter a number.".center(127))
        else:
            # Jugador bot: apostar un porcentaje de sus puntos según su perfil de riesgo
            percentage = player["type"]  # El tipo del jugador (30, 40 o 50)
            bet_amount = int(player["points"] * (percentage / 100))  # Calcular el porcentaje y truncar
            
            # Asegurarse de que la apuesta no sea 0
            if bet_amount == 0:
                bet_amount = 1  # Apostar al menos 1 punto
            
            player["bet"] = bet_amount
            print(f"{player['name']} (bot) bets {bet_amount} points.".center(127))
            addToRoundHistory(str(f"{player['name']} (bot) bets {bet_amount} points."))
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
        print(f"{Dt.context_game['players'][player_id]['name']} has recived: {Dt.context_game['cards_deck'][card]['literal']}".center(127))
        addToRoundHistory(str(f"{Dt.context_game['players'][player_id]['name']} has recived: {Dt.context_game['cards_deck'][card]['literal']}"))
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
            print("The round history is empty.".center(127))
            print()
            input("Press Enter to return...".center(127))
            break

        for entry in range(0,len(Dt.context_game["round_history"])):
            print(Dt.context_game["round_history"][entry].center(127))
        print()
        input("Press Enter to return...".center(127))
        break