import SC.Utilidad as Ut
import SC.Datos as Dt
import SC.Juego as Jg
import SC.Bbdd as Bd
import SC.Cabeceras as Cb
import time

from ProyectoSieteYMedio_ACD.SC.Bbdd import getBBDDRankingPoints, getBBDDRankingByMinutes, getPlayersByGamesPlayed, \
    getBBDDRankingByMinutes, getBBDDRankingPoints


def main_menu():
    # Muestra el menú principal del juego y gestiona la selección de opciones.

    while True:
        Ut.clear_terminal()
        print(Cb.cabecera00)
        menu = [
            "1) Add/Remove/Show Players",
            "2) Settings",
            "3) Play Game",
            "4) Ranking",
            "5) Reports",
            "6) Exit"
        ]
        Ut.print_centered_menu(menu,127)

        option = Ut.getOpt(
            inputOptText="Select an option: ".rjust(70),
            rangeList=[1, 2, 3, 4, 5, 6]
        )
        
        if option == 1:
            addRemovePlayers()
        elif option == 2:
            settings()
        elif option == 3:
            Jg.addCardsToMaze()
            Jg.playGame()
        elif option == 4:
            ranking()
        elif option == 5:
            reports()
        elif option == 6:
            Ut.clear_terminal()
            break

def addRemovePlayers():
    # Muestra el menú para añadir, eliminar o mostrar jugadores.

    while True:
        Ut.clear_terminal()
        print(Cb.cabecera01)
        menu=[
            "1) New Human Player",
            "2) New Bot",
            "3) Show/Delete Players",
            "4) Return to Main Menu"
        ]
        Ut.print_centered_menu(menu,127)

        option = Ut.getOpt(
            inputOptText="Select an option: ".rjust(70),
            rangeList=[1, 2, 3, 4]
        )
        
        if option == 1:
            setNewPlayer(human=True)
        elif option == 2:
            setNewPlayer(human=False)
        elif option == 3:
            Bd.removeBBDDPlayer()
        elif option == 4:
            break

def settings():
    # Muestra el menú de configuración del juego.
    
    while True:
        Ut.clear_terminal()
        print(Cb.cabecera02)
        menu=[
            "1) Set Game Players",
            "2) Set Deck of Cards",
            "3) Set Maximum Rounds",
            "4) Return to Main Menu"
        ]
        Ut.print_centered_menu(menu,127)

        option = Ut.getOpt(
            inputOptText="Select an option: ".rjust(70),
            rangeList=[1, 2, 3, 4]
        )
        
        if option == 1:
            setPlayersGame()
        elif option == 2:
            setCardsDeck()
        elif option == 3:
            setMaxRounds()
        elif option == 4:
            break

def setMaxRounds():
    # Establece el número máximo de rondas para la partida.
    
    while True:
        Ut.clear_terminal()
        print(Cb.cabecera02)
        print(f"Current: {Dt.context_game['maxRounds']} rounds (Max 30 rounds)".center(127))
        print()
        print("0) Leave this menu".center(127))
        print() 
        max_rounds = input("Enter the maximum number of rounds: ".rjust(82)).strip()
        
        if max_rounds.isdigit() and 0 < int(max_rounds) <= 30:
            Dt.context_game["maxRounds"] = int(max_rounds)
            print(f"Maximum number of rounds set to {max_rounds}.".center(127))
            time.sleep(1)
            break
        elif max_rounds.isdigit() and int(max_rounds) == 0:
            break
        else:
            print("Invalid input. Enter a number greater than 0 and lower than 31.".center(127))
            time.sleep(1)

def setPlayersGame():
    # Permite al usuario seleccionar jugadores de la lista de jugadores guardados
    # y añadirlos a la partida actual.
    # También permite eliminar jugadores ya seleccionados.    
    # Verificar si hay jugadores disponibles
    
    if not Dt.context_game.get("players"):
        print("No players available. Please add players first.".center(127))
        input("Press Enter to continue...".center(127))
        return
    
    # Obtener la lista de jugadores ya seleccionados
    selected_players = Dt.context_game.get("game", [])
    
    # Mostrar menú principal de selección/eliminación
    while True:
        Ut.clear_terminal()
        print(Cb.cabecera02)
        showPlayersGame()
        print()
        print(" Select/Remove Players ".center(127,"="))
        menu=[
            "1) Add Players to Game",
            "2) Remove Players from Game",
            "3) Return to Previous Menu",
        ]
        Ut.print_centered_menu(menu,127)
        
        option = Ut.getOpt(
            inputOptText="Select an option: ".rjust(70),
            rangeList=[1, 2, 3]
        )
        
        if option == 1:
            # Añadir jugadores a la partida
            addPlayersToGame(selected_players)
        elif option == 2:
            # Eliminar jugadores de la partida
            removePlayersFromGame(selected_players)
        elif option == 3:
            # Guardar los jugadores seleccionados y salir
            Dt.context_game["game"] = selected_players
            break

def addPlayersToGame(selected_players):
    # Muestra la lista de jugadores disponibles y permite añadirlos a la partida.
    # El usuario debe introducir el DNI del jugador que desea añadir.
    # No se pueden añadir más de 6 jugadores.
    
    # Verificar si ya se han seleccionado 6 jugadores
    if len(selected_players) >= 6:
        print("6 players have already been selected. No more can be added.".center(127))
        input("Press Enter to continue...".center(127))
        return
    
    # Filtrar jugadores disponibles (excluyendo los ya seleccionados)
    available_players = {
        player_id: player_data
        for player_id, player_data in Dt.context_game["players"].items()
        if player_id not in selected_players
    }
    
    # Verificar si hay jugadores disponibles después de filtrar
    if not available_players:
        print("All players have already been selected for the game.".center(127))
        input("Press Enter to continue...".center(127))
        return

    # Solicitar al usuario que introduzca el DNI del jugador
    while True:
        # Verificar si ya se han seleccionado 6 jugadores
        if len(selected_players) >= 6:
            print("6 players have already been selected. No more can be added.".center(127))
            time.sleep(1)
            break
        
        Ut.clear_terminal()
        print(Cb.cabecera02)
        showPlayersGame()
        print()
        print(" Add players to the game ".center(127,"="))
        for player_id, player_data in available_players.items():
            player_name = player_data.get("name", "Unknown")
            player_type = "Human" if player_data.get("human", False) else "Bot"
            player_risk = player_data.get("type", "N/A")
            # Convertir el perfil de riesgo a texto
            if player_risk == 50:
                risk_profile = "Daring"
            elif player_risk == 40:
                risk_profile = "Normal"
            elif player_risk == 30:
                risk_profile = "Cautious"
            else:
                risk_profile = "N/A"
            print(str(player_id.rjust(32) + player_name.rjust(21) +" "*20+ player_type.ljust(21) + risk_profile.ljust(32)))
        print()

        print("0) Exit".center(127))
        print()

        dni = input(
            "Enter the ID of the player you wish to add to the game: ".rjust(90)
        ).strip().upper()
        
        if dni == "0":
            break
        
        if dni in available_players:
            selected_players.append(dni)
            print(f"Player {available_players[dni]['name']} added to the game.".center(127))
            time.sleep(1)
            # Actualizar la lista de jugadores disponibles
            available_players = {
                player_id: player_data
                for player_id, player_data in Dt.context_game["players"].items()
                if player_id not in selected_players
            }
            
            # Si no quedan jugadores disponibles, terminar
            if not available_players:
                print("All players have been selected.".center(127))
                time.sleep(1)
                break
        else:
            print("Invalid ID. Please try again.".center(127))
            time.sleep(1)


def removePlayersFromGame(selected_players):
    # Muestra la lista de jugadores seleccionados y permite eliminarlos de la partida.
    # El usuario debe introducir el DNI del jugador que desea eliminar.
    
    # Verificar si hay jugadores seleccionados
    if not selected_players:
        print("No players available. Please add players first.".center(127))
        input("Press Enter to continue...".center(127))
        return
    
    # Solicitar al usuario que introduzca el DNI del jugador
    while True:
        if not selected_players:
            print("No players available. Please add players first.".center(127))
            time.sleep(1)
            break

        Ut.clear_terminal()
        print(Cb.cabecera02)
        print(" Remove players from the game ".center(127,"="))
        for player_id in selected_players:
            player_data = Dt.context_game["players"].get(player_id, {})
            player_name = player_data.get("name", "Unknown")
            player_type = "Human" if player_data.get("human", False) else "Bot"
            player_risk = player_data.get("type", "N/A")
            # Convertir el perfil de riesgo a texto
            if player_risk == 50:
                risk_profile = "Daring"
            elif player_risk == 40:
                risk_profile = "Normal"
            elif player_risk == 30:
                risk_profile = "Cautious"
            else:
                risk_profile = "N/A"
            print(str(player_id.rjust(32) + player_name.rjust(21) +" "*20+ player_type.ljust(21) + risk_profile.ljust(32)))
        print()
        print("0) Exit".center(127))
        print()
        dni = input(
            "Enter the ID of the player you wish to remove: ".rjust(85)
        ).strip().upper()
        
        if dni == "0":
            break
        
        if dni in selected_players:
            player_name = Dt.context_game["players"].get(dni, {}).get("name", "Unknown")
            
            confirm = input(f"Are you sure you want to remove {player_name}? (y/n): ".rjust(83)).strip().lower()
            if confirm == "y":
                selected_players.remove(dni)
                print(f"Player {player_name} removed from the game.".center(127))
                time.sleep(1)
            else:
                print("Removal canceled.".center(127))
                time.sleep(1)
        else:
            print("Invalid ID. Please try again.".center(127))
            time.sleep(1)

def showPlayersGame():
    #Visualizar jugadores seleccionados
    print(" Players in the Game ".center(127,"="))
    
    # Verificar si hay jugadores en la partida
    if not Dt.context_game.get("game"):
        print("There are no players in the current game.".center(127))
    else:
        # Mostrar la lista de jugadores
        for i in range(0, len(Dt.context_game["game"])):
            player_id = Dt.context_game["game"][i]
            player_name = Dt.context_game["players"][Dt.context_game["game"][i]]["name"]
            if Dt.context_game["players"][Dt.context_game["game"][i]]["human"]:
                player_human = "Human"
            else:
                player_human = "Bot"
            if Dt.context_game["players"][Dt.context_game["game"][i]]["type"] == 30:
                player_type = "Cautious"
            elif Dt.context_game["players"][Dt.context_game["game"][i]]["type"] == 40:
                player_type = "Moderate"
            elif Dt.context_game["players"][Dt.context_game["game"][i]]["type"] == 50:
                player_type = "Daring"
            else:
                player_type = "ERROR"

            print(str(player_id.rjust(32) + player_name.rjust(21) +" "*20+ player_human.ljust(21)) + player_type.ljust(32))

def setCardsDeck():
    # Permite al usuario seleccionar una baraja de cartas para la partida.
    # Muestra la baraja seleccionada actualmente.

    while True:
        Ut.clear_terminal()
        print(Cb.cabecera02)

        # Mostrar la baraja seleccionada actualmente
        if "cards_deck" in Dt.context_game and Dt.context_game["cards_deck"]:
            if Dt.context_game["cards_deck"] == Dt.cartas_es:
                print("Currently selected deck: Spanish Deck (40 cards)".center(127))
            elif Dt.context_game["cards_deck"] == Dt.cartas_en:
                print("Currently selected deck: English Deck (52 cards)".center(127))
            elif Dt.context_game["cards_deck"] == Dt.cartas_al:
                print("Currently selected deck: German Deck (60 cards)".center(127))
        print()
        # Mostrar las opciones de barajas disponibles
        print("Select the card deck for the game:".center(127))
        menu=[
            "1) Spanish Deck (40 cards)",
            "2) English Deck (52 cards)",
            "3) German Deck (60 cards)",
            "4) Return to Previous Menu"
        ]
        Ut.print_centered_menu(menu,127)

        # Solicitar al usuario que seleccione una opción
        option = Ut.getOpt(
            inputOptText="Select an option: ".rjust(70),
            rangeList=[1, 2, 3, 4]
        )

        # Asignar la baraja seleccionada a context_game["cards_deck"]
        if option == 1:
            Dt.context_game["cards_deck"] = Dt.cartas_es
            print("Spanish Deck selected.".center(127))
        elif option == 2:
            Dt.context_game["cards_deck"] = Dt.cartas_en
            print("English Deck selected.".center(127))
        elif option == 3:
            Dt.context_game["cards_deck"] = Dt.cartas_al
            print("German Deck selected.".center(127))
        elif option == 4:
            return
        input("Press Enter to continue...".center(127))

def reports():
    # Muestra el menú de informes y gestiona la selección de opciones.
    
    while True:
        Ut.clear_terminal()
        print(Cb.cabecera04)
        menu=[
            "1) Most Repeated Initial Card",
            "2) Highest Bet per Game",
            "3) Lowest Bet per Game",
            "4) Win Percentage per Round",
            "5) Games Won by Bots",
            "6) Rounds Won by the Bank",
            "7) Users Who Have Been Bank",
            "8) Return to Main Menu",
        ]
        Ut.print_centered_menu(menu,127)

        option = Ut.getOpt(
            inputOptText="Select an option: ".rjust(70),
            rangeList=[1, 2, 3, 4, 5, 6, 7, 8]
        )
        
        if option == 8:
            break
        else:
            print(f"Report {option} selected. Functionality under development...".center(127))
            time.sleep(1)

def ranking():
    # Muestra el menú de ranking y gestiona la selección de opciones.

    while True:
        Ut.clear_terminal()
        print(Cb.cabecera03)
        menu=[
            "1) Players with Most Earnings",
            "2) Players with Most Games Played",
            "3) Players with Most Minutes Played",
            "4) Return to Main Menu",
        ]
        Ut.print_centered_menu(menu,127)
        
        option = Ut.getOpt(
            inputOptText="Select an option: ".rjust(70),
            rangeList=[1, 2, 3, 4]
        )
        if option == 1:
            getBBDDRankingPoints()
        elif option == 2:
            getPlayersByGamesPlayed()
        elif option == 3:
            getBBDDRankingByMinutes()
        if option == 4:
            break
        else:
            print(f"Ranking {option} selected. Functionality under development...".center(127))
            time.sleep(1)

def setNewPlayer(human=True):
    #Crea un nuevo jugador (humano o bot) y lo añade a la base de datos.
    #Parámetros:
    #- human: Booleano que indica si el jugador es humano (True) o un bot (False).
    
    Ut.clear_terminal()
    print(Cb.cabecera01)
    
    # Solicitar nombre del jugador
    name = input("Enter the player's name: ".rjust(75)).strip()
    if name == "":
        print("The name cannot be empty.".center(127))
        time.sleep(1)
        return
    
    # Solicitar perfil de riesgo (solo para bots)
    if not human:
        print("Select the bot's risk profile:".center(127))
        menu=[
            "1) Daring (50)",
            "2) Normal (40)",
            "3) Cautious (30)",
        ]
        Ut.print_centered_menu(menu,127)
        
        profile_option = Ut.getOpt(
            inputOptText="Select an option: ".rjust(70),
            rangeList=[1, 2, 3]
        )
        
        if profile_option == 1:
            risk = str(50)
        elif profile_option == 2:
            risk = str(40)
        elif profile_option == 3:
            risk = str(30)
    else:
        print("Select the player's risk profile:".center(127))
        menu=[
            "1) Daring (50)",
            "2) Normal (40)",
            "3) Cautious (30)",
        ]
        Ut.print_centered_menu(menu,127)
        
        profile_option = Ut.getOpt(
            inputOptText="Select an option: ".rjust(70),
            rangeList=[1, 2, 3]
        )
        
        if profile_option == 1:
            risk = str(50)
        elif profile_option == 2:
            risk = str(40)
        elif profile_option == 3:
            risk = str(30)
    
    # Generar un DNI aleatorio para el jugador
    dni = Ut.newRandomDNI()
    
    # Guardar el jugador en la base de datos
    Bd.savePlayer(dni, name, risk, human)
    
    input("Press Enter to continue...".center(127))