import SC.Utilidad as Ut
import SC.Datos as Dt
import SC.Juego as Jg
import SC.Bbdd as Bd
import time


def main_menu():
    # Muestra el menú principal del juego y gestiona la selección de opciones.

    while True:
        Ut.clear_terminal()
        print("=== Main Menu ===")
        print("1) Add/Remove/Show Players")
        print("2) Settings")
        print("3) Play Game")
        print("4) Ranking")
        print("5) Reports")
        print("6) Exit")
        
        option = Ut.getOpt(
            inputOptText="Select an option: ",
            rangeList=[1, 2, 3, 4, 5, 6]
        )
        
        if option == 1:
            addRemovePlayers()
        elif option == 2:
            settings()
        elif option == 3:
            Jg.playGame()
        elif option == 4:
            ranking()
        elif option == 5:
            reports()
        elif option == 6:
            print("Leaving the game...")
            break

def addRemovePlayers():
    # Muestra el menú para añadir, eliminar o mostrar jugadores.

    while True:
        Ut.clear_terminal()
        print("=== Player Management ===")
        print("1) New Human Player")
        print("2) New Bot")
        print("3) Show/Delete Players")
        print("4) Return to Main Menu")

        
        option = Ut.getOpt(
            inputOptText="Select an option: ",
            rangeList=[1, 2, 3, 4]
        )
        
        if option == 1:
            setNewPlayer(human=True)
        elif option == 2:
            setNewPlayer(human=False)
        elif option == 3:
            print("FUNCTIONALITY TO BE CREATED")
        elif option == 4:
            break

def settings():
    # Muestra el menú de configuración del juego.
    
    while True:
        Ut.clear_terminal()
        print("=== Game Settings ===")
        print("1) Set Game Players")
        print("2) Set Deck of Cards")
        print("3) Set Maximum Rounds")
        print("4) Return to Main Menu")
        
        option = Ut.getOpt(
            inputOptText="Select an option: ",
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
        print("=== Select Maximum Rounds ===")
        print(f"Current: {Dt.context_game['maxRounds']} rounds")
        print() 
        max_rounds = input("Enter the maximum number of rounds: ").strip()
        
        if max_rounds.isdigit() and int(max_rounds) > 0:
            Dt.context_game["maxRounds"] = int(max_rounds)
            print(f"Maximum number of rounds set to {max_rounds}.")
            time.sleep(1)
            break
        else:
            print("Invalid input. Enter a number greater than 0.")
            time.sleep(1)

def setPlayersGame():
    # Permite al usuario seleccionar jugadores de la lista de jugadores guardados
    # y añadirlos a la partida actual.
    # También permite eliminar jugadores ya seleccionados.    
    # Verificar si hay jugadores disponibles
    
    if not Dt.context_game.get("players"):
        print("No players available. Please add players first.")
        input("Press Enter to continue...")
        return
    
    # Obtener la lista de jugadores ya seleccionados
    selected_players = Dt.context_game.get("game", [])
    
    # Mostrar menú principal de selección/eliminación
    while True:
        Ut.clear_terminal()
        showPlayersGame()
        print()
        print("=== Select/Remove Players ===")
        print("1) Add Players to Game")
        print("2) Remove Players from Game")
        print("3) Return to Previous Menu")
        
        option = Ut.getOpt(
            inputOptText="Select an option: ",
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
        print("6 players have already been selected. No more can be added.")
        input("Press Enter to continue...")
        return
    
    # Filtrar jugadores disponibles (excluyendo los ya seleccionados)
    available_players = {
        player_id: player_data
        for player_id, player_data in Dt.context_game["players"].items()
        if player_id not in selected_players
    }
    
    # Verificar si hay jugadores disponibles después de filtrar
    if not available_players:
        print("All players have already been selected for the game.")
        input("Press Enter to continue...")
        return

    # Solicitar al usuario que introduzca el DNI del jugador
    while True:
        # Verificar si ya se han seleccionado 6 jugadores
        if len(selected_players) >= 6:
            print("6 players have already been selected. No more can be added.")
            time.sleep(1)
            break
        
        Ut.clear_terminal()
        showPlayersGame()
        print()
        print("=== Add Players to the Game ===")
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
            print(player_id.ljust(18) + player_name.ljust(18) + player_type.ljust(18) + risk_profile.ljust(18))
        print()

        print("0) Exit")
        print()

        dni = input(
            "Enter the ID of the player you wish to add to the game: "
        ).strip().upper()
        
        if dni == "0":
            break
        
        if dni in available_players:
            selected_players.append(dni)
            print(f"Player {available_players[dni]['name']} added to the game.")
            time.sleep(1)
            # Actualizar la lista de jugadores disponibles
            available_players = {
                player_id: player_data
                for player_id, player_data in Dt.context_game["players"].items()
                if player_id not in selected_players
            }
            
            # Si no quedan jugadores disponibles, terminar
            if not available_players:
                print("All players have been selected.")
                time.sleep(1)
                break
        else:
            print("Invalid ID. Please try again.")
            time.sleep(1)


def removePlayersFromGame(selected_players):
    # Muestra la lista de jugadores seleccionados y permite eliminarlos de la partida.
    # El usuario debe introducir el DNI del jugador que desea eliminar.
    
    # Verificar si hay jugadores seleccionados
    if not selected_players:
        print("No players available. Please add players first.")
        input("Press Enter to continue...")
        return
    
    # Solicitar al usuario que introduzca el DNI del jugador
    while True:
        if not selected_players:
            print("No players available. Please add players first.")
            time.sleep(1)
            break

        Ut.clear_terminal()
        print("=== Remove Players from the Game ===")
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
            print(player_id.ljust(18) + player_name.ljust(18) + player_type.ljust(18) + risk_profile.ljust(18))
        print()
        print("0) Exit")
        print()
        dni = input(
            "Enter the ID of the player you wish to remove: "
        ).strip().upper()
        
        if dni == "0":
            break
        
        if dni in selected_players:
            player_name = Dt.context_game["players"].get(dni, {}).get("name", "Unknown")
            
            confirm = input(f"Are you sure you want to remove {player_name}? (y/n): ").strip().lower()
            if confirm == "y":
                selected_players.remove(dni)
                print(f"Player {player_name} removed from the game.")
                time.sleep(1)
            else:
                print("Removal canceled.")
                time.sleep(1)
        else:
            print("Invalid ID. Please try again.")
            time.sleep(1)

def showPlayersGame():
    #Visualizar jugadores seleccionados
    print("=== Players in the Game ===")
    
    # Verificar si hay jugadores en la partida
    if not Dt.context_game.get("game"):
        print("There are no players in the current game.")
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

            print(player_id.ljust(18) + player_name.ljust(18) + player_human.ljust(18) + player_type.ljust(18))

def setCardsDeck():
    """
    Permite al usuario seleccionar una baraja de cartas para la partida.
    Muestra la baraja seleccionada actualmente y establece la Baraja Española como predeterminada.
    """
    while True:
        Ut.clear_terminal()
        print("=== Select Card Deck ===")

        # Mostrar la baraja seleccionada actualmente
        if "cards_deck" in Dt.context_game and Dt.context_game["cards_deck"]:
            if Dt.context_game["cards_deck"] == Dt.cartas_es:
                print("Currently selected deck: Spanish Deck (40 cards)")
            elif Dt.context_game["cards_deck"] == Dt.cartas_en:
                print("Currently selected deck: English Deck (52 cards)")
            elif Dt.context_game["cards_deck"] == Dt.cartas_al:
                print("Currently selected deck: German Deck (60 cards)")
        print()
        # Mostrar las opciones de barajas disponibles
        print("Select the card deck for the game:")
        print("1) Spanish Deck (40 cards)")
        print("2) English Deck (52 cards)")
        print("3) German Deck (60 cards)")
        print("4) Return to Previous Menu")

        # Solicitar al usuario que seleccione una opción
        option = Ut.getOpt(
            inputOptText="Select an option (1-4): ",
            rangeList=[1, 2, 3, 4]
        )

        # Asignar la baraja seleccionada a context_game["cards_deck"]
        if option == 1:
            Dt.context_game["cards_deck"] = Dt.cartas_es
            print("Spanish Deck selected.")
        elif option == 2:
            Dt.context_game["cards_deck"] = Dt.cartas_en
            print("English Deck selected.")
        elif option == 3:
            Dt.context_game["cards_deck"] = Dt.cartas_al
            print("German Deck selected.")
        elif option == 4:
            return
        input("Press Enter to continue...")

def reports():
    """
    Muestra el menú de informes y gestiona la selección de opciones.
    """
    while True:
        Ut.clear_terminal()
        print("=== Reports ===")
        print("1) Most Repeated Initial Card")
        print("2) Highest Bet per Game")
        print("3) Lowest Bet per Game")
        print("4) Win Percentage per Round")
        print("5) Games Won by Bots")
        print("6) Rounds Won by the Bank")
        print("7) Users Who Have Been Bank")
        print("8) Return to Main Menu")
        
        option = Ut.getOpt(
            inputOptText="Select an option: ",
            rangeList=[1, 2, 3, 4, 5, 6, 7, 8]
        )
        
        if option == 8:
            break
        else:
            print(f"Report {option} selected. Functionality under development...")

def ranking():
    """
    Muestra el menú de ranking y gestiona la selección de opciones.
    """
    while True:
        Ut.clear_terminal()
        print("=== Ranking ===")
        print("1) Players with Most Earnings")
        print("2) Players with Most Games Played")
        print("3) Players with Most Minutes Played")
        print("4) Return to Main Menu")
        
        option = Ut.getOpt(
            inputOptText="Select an option: ",
            rangeList=[1, 2, 3, 4]
        )
        
        if option == 4:
            break
        else:
            print(f"Ranking {option} selected. Functionality under development...")

def setNewPlayer(human=True):
    """
    Crea un nuevo jugador (humano o bot) y lo añade a la base de datos.
    
    Parámetros:
    - human: Booleano que indica si el jugador es humano (True) o un bot (False).
    """
    Ut.clear_terminal()
    print("=== Create New Player ===")
    
    # Solicitar nombre del jugador
    name = input("Enter the player's name: ").strip()
    if not name:
        print("The name cannot be empty.")
        return
    
    # Solicitar perfil de riesgo (solo para bots)
    if not human:
        print("Select the bot's risk profile:")
        print("1) Daring (50)")
        print("2) Normal (40)")
        print("3) Cautious (30)")
        
        profile_option = Ut.getOpt(
            inputOptText="Select an option: ",
            rangeList=[1, 2, 3]
        )
        
        if profile_option == 1:
            risk = 50
        elif profile_option == 2:
            risk = 40
        elif profile_option == 3:
            risk = 30
    else:
        risk = 40  # Por defecto, los humanos tienen un perfil "normal"
    
    # Generar un DNI aleatorio para el jugador
    dni = Ut.newRandomDNI()
    
    # Guardar el jugador en la base de datos
    Bd.savePlayer(dni, name, risk, human)
    
    print(f"Player '{name}' successfully created. ID: {dni}")
    input("Press Enter to continue...")