import SC.Utilidad as Ut
import SC.Datos as Dt
import SC.Juego as Jg
import SC.Bbdd as Bd
import time


def main_menu():
    # Muestra el menú principal del juego y gestiona la selección de opciones.

    while True:
        Ut.clear_terminal()
        print("=== Menú Principal ===")
        print("1) Add/Remove/Show Players")
        print("2) Settings")
        print("3) Play Game")
        print("4) Ranking")
        print("5) Reports")
        print("6) Exit")
        
        option = Ut.getOpt(
            inputOptText="Seleccione una opción: ",
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
            print("Saliendo del juego...")
            break

def addRemovePlayers():
    # Muestra el menú para añadir, eliminar o mostrar jugadores.

    while True:
        Ut.clear_terminal()
        print("=== Gestión de Jugadores ===")
        print("1) Nuevo Jugador Humano")
        print("2) Nuevo Bot")
        print("3) Mostrar/Eliminar Jugadores")
        print("4) Volver al Menú Principal")
        
        option = Ut.getOpt(
            inputOptText="Seleccione una opción: ",
            rangeList=[1, 2, 3, 4]
        )
        
        if option == 1:
            setNewPlayer(human=True)
        elif option == 2:
            setNewPlayer(human=False)
        elif option == 3:
            print("FUNCIONALIDAD POR CREAR")
        elif option == 4:
            break

def settings():
    # Muestra el menú de configuración del juego.
    
    while True:
        Ut.clear_terminal()
        print("=== Configuración del Juego ===")
        print("1) Establecer Jugadores de la Partida")
        print("2) Establecer Baraja de Cartas")
        print("3) Establecer Máximo de Rondas")
        print("4) Volver al Menú Principal")
        
        option = Ut.getOpt(
            inputOptText="Seleccione una opción: ",
            rangeList=[1, 2, 3, 4]
        )
        
        if option == 1:
            setPlayersGame()
        elif option == 2:
            Bd.setCardsDeck()
        elif option == 3:
            setMaxRounds()
        elif option == 4:
            break

def setMaxRounds():
    # Establece el número máximo de rondas para la partida.
    
    while True:
        Ut.clear_terminal()
        max_rounds = input("Introduzca el número máximo de rondas (por defecto 5): ").strip()
        
        if max_rounds.isdigit() and int(max_rounds) > 0:
            Dt.context_game["maxRounds"] = int(max_rounds)
            Ut.clear_terminal()
            print(f"Número máximo de rondas establecido a {max_rounds}.")
            time.sleep(2)
            break
        else:
            print("Entrada no válida. Introduzca un número mayor que 0.")

def setPlayersGame():
    """
    Permite al usuario seleccionar jugadores de la lista de jugadores guardados
    y añadirlos a la partida actual (context_game["game"]).
    Los jugadores ya seleccionados no aparecerán en la lista de disponibles.
    """
    Ut.clear_terminal()
    showPlayersGame()
    print()
    print("=== Seleccionar Jugadores para la Partida ===")
    
    # Verificar si hay jugadores disponibles
    if not Dt.context_game.get("players"):
        print("No hay jugadores disponibles. Por favor, añada jugadores primero.")
        input("Presione Enter para continuar...")
        return
    
    # Obtener la lista de jugadores ya seleccionados
    selected_players = Dt.context_game.get("game", [])
    
    # Filtrar jugadores disponibles (excluyendo los ya seleccionados)
    available_players = {
        player_id: player_data
        for player_id, player_data in Dt.context_game["players"].items()
        if player_id not in selected_players
    }
    
    # Verificar si hay jugadores disponibles después de filtrar
    if not available_players:
        print("Todos los jugadores ya están seleccionados para la partida.")
        input("Presione Enter para continuar...")
        return
    
    # Mostrar la lista de jugadores disponibles
    print("Jugadores disponibles:")
    for i, (player_id, player_data) in enumerate(available_players.items(), start=1):
        player_name = player_data.get("name", "Desconocido")
        player_type = "Humano" if player_data.get("human", False) else "Bot"
        print(f"{i}) {player_name} ({player_type}) - ID: {player_id}")
    
    # Solicitar al usuario que seleccione jugadores
    while True:
        option = input(
            "Seleccione el número del jugador para añadir a la partida (o 'fin' para terminar): "
        ).strip().lower()
        
        if option == "fin":
            break
        
        if option.isdigit():
            option = int(option)
            if 1 <= option <= len(available_players):
                player_id = list(available_players.keys())[option - 1]
                selected_players.append(player_id)
                print(f"Jugador {available_players[player_id]['name']} añadido a la partida.")
                
                # Actualizar la lista de jugadores disponibles
                available_players = {
                    player_id: player_data
                    for player_id, player_data in Dt.context_game["players"].items()
                    if player_id not in selected_players
                }
                
                # Si no quedan jugadores disponibles, terminar
                if not available_players:
                    print("Todos los jugadores han sido seleccionados.")
                    break
            else:
                print("Número no válido. Inténtelo de nuevo.")
        else:
            print("Entrada no válida. Inténtelo de nuevo.")
    
    # Guardar los jugadores seleccionados en context_game["game"]
    Dt.context_game["game"] = selected_players
    print("Jugadores seleccionados para la partida:")
    for player_id in selected_players:
        print(f"- {Dt.context_game['players'][player_id]['name']} (ID: {player_id})")
    
    input("Presione Enter para continuar...")

def showPlayersGame():
    #Visualizar jugadores seleccionados
    print("=== Jugadores en la Partida ===")
    
    # Verificar si hay jugadores en la partida
    if not Dt.context_game.get("game"):
        print("No hay jugadores en la partida actual.")
    else:
    # Mostrar la lista de jugadores
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

            print(f"{i+1}) " + player_id.ljust(18) + player_name.ljust(18) + player_human.ljust(18) + player_type.ljust(18))

def reports():
    """
    Muestra el menú de informes y gestiona la selección de opciones.
    """
    while True:
        Ut.clear_terminal()
        print("=== Informes ===")
        print("1) Carta Inicial Más Repetida")
        print("2) Apuesta Más Alta por Partida")
        print("3) Apuesta Más Baja por Partida")
        print("4) Porcentaje de Rondas Ganadas")
        print("5) Partidas Ganadas por Bots")
        print("6) Rondas Ganadas por la Banca")
        print("7) Usuarios que han sido Banca")
        print("8) Volver al Menú Principal")
        
        option = Ut.getOpt(
            inputOptText="Seleccione una opción: ",
            rangeList=[1, 2, 3, 4, 5, 6, 7, 8]
        )
        
        if option == 8:
            break
        else:
            print(f"Informe {option} seleccionado. Funcionalidad en desarrollo...")

def ranking():
    """
    Muestra el menú de ranking y gestiona la selección de opciones.
    """
    while True:
        Ut.clear_terminal()
        print("=== Ranking ===")
        print("1) Jugadores con Más Ganancias")
        print("2) Jugadores con Más Partidas Jugadas")
        print("3) Jugadores con Más Minutos Jugados")
        print("4) Volver al Menú Principal")
        
        option = Ut.getOpt(
            inputOptText="Seleccione una opción: ",
            rangeList=[1, 2, 3, 4]
        )
        
        if option == 4:
            break
        else:
            print(f"Ranking {option} seleccionado. Funcionalidad en desarrollo...")

def setNewPlayer(human=True):
    """
    Crea un nuevo jugador (humano o bot) y lo añade a la base de datos.
    
    Parámetros:
    - human: Booleano que indica si el jugador es humano (True) o un bot (False).
    """
    Ut.clear_terminal()
    print("=== Crear Nuevo Jugador ===")
    
    # Solicitar nombre del jugador
    name = input("Introduzca el nombre del jugador: ").strip()
    if not name:
        print("El nombre no puede estar vacío.")
        return
    
    # Solicitar perfil de riesgo (solo para bots)
    if not human:
        print("Seleccione el perfil de riesgo del bot:")
        print("1) Atrevido (50)")
        print("2) Normal (40)")
        print("3) Prudente (30)")
        
        profile_option = Ut.getOpt(
            inputOptText="Seleccione una opción: ",
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
    
    print(f"Jugador '{name}' creado con éxito. DNI: {dni}")
    input("Presione Enter para continuar...")