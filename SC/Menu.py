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
            setCardsDeck()
        elif option == 3:
            setMaxRounds()
        elif option == 4:
            break

def setMaxRounds():
    # Establece el número máximo de rondas para la partida.
    
    while True:
        Ut.clear_terminal()
        print("=== Seleccionar rondas maximas ===")
        print(f"Actual: {Dt.context_game["maxRounds"]} rondas")
        print() 
        max_rounds = input("Introduzca el número máximo de rondas: ").strip()
        
        if max_rounds.isdigit() and int(max_rounds) > 0:
            Dt.context_game["maxRounds"] = int(max_rounds)
            print(f"Número máximo de rondas establecido a {max_rounds}.")
            time.sleep(1)
            break
        else:
            print("Entrada no válida. Introduzca un número mayor que 0.")
            time.sleep(1)

def setPlayersGame():
    # Permite al usuario seleccionar jugadores de la lista de jugadores guardados
    # y añadirlos a la partida actual.
    # También permite eliminar jugadores ya seleccionados.    
    # Verificar si hay jugadores disponibles
    
    if not Dt.context_game.get("players"):
        print("No hay jugadores disponibles. Por favor, añada jugadores primero.")
        input("Presione Enter para continuar...")
        return
    
    # Obtener la lista de jugadores ya seleccionados
    selected_players = Dt.context_game.get("game", [])
    
    # Mostrar menú principal de selección/eliminación
    while True:
        Ut.clear_terminal()
        showPlayersGame()
        print()
        print("=== Seleccionar/Eliminar Jugadores ===")
        print("1) Añadir Jugadores a la Partida")
        print("2) Eliminar Jugadores de la Partida")
        print("3) Volver al Menú Anterior")
        
        option = Ut.getOpt(
            inputOptText="Seleccione una opción: ",
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
        print("Ya se han seleccionado 6 jugadores. No se pueden añadir más.")
        input("Presione Enter para continuar...")
        return
    
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

    # Solicitar al usuario que introduzca el DNI del jugador
    while True:
        # Verificar si ya se han seleccionado 6 jugadores
        if len(selected_players) >= 6:
            print("Ya se han seleccionado 6 jugadores. No se pueden añadir más.")
            time.sleep(1)
            break
        
        Ut.clear_terminal()
        showPlayersGame()
        print()
        print("=== Añadir Jugadores a la Partida ===")
        for player_id, player_data in available_players.items():
            player_name = player_data.get("name", "Desconocido")
            player_type = "Humano" if player_data.get("human", False) else "Bot"
            player_risk = player_data.get("type", "N/A")
            # Convertir el perfil de riesgo a texto
            if player_risk == 50:
                risk_profile = "Atrevido"
            elif player_risk == 40:
                risk_profile = "Normal"
            elif player_risk == 30:
                risk_profile = "Prudente"
            else:
                risk_profile = "N/A"
            print(player_id.ljust(18) + player_name.ljust(18) + player_type.ljust(18) + risk_profile.ljust(18))
        print()

        print("0) Salir")
        print()

        dni = input(
            "Introduzca el DNI del jugador que desea añadir a la partida: "
        ).strip().upper()
        
        if dni == "0":
            break
        
        if dni in available_players:
            selected_players.append(dni)
            print(f"Jugador {available_players[dni]['name']} añadido a la partida.")
            time.sleep(1)
            # Actualizar la lista de jugadores disponibles
            available_players = {
                player_id: player_data
                for player_id, player_data in Dt.context_game["players"].items()
                if player_id not in selected_players
            }
            
            # Si no quedan jugadores disponibles, terminar
            if not available_players:
                print("Todos los jugadores han sido seleccionados.")
                time.sleep(1)
                break
        else:
            print("DNI no válido. Inténtelo de nuevo.")
            time.sleep(1)


def removePlayersFromGame(selected_players):
    # Muestra la lista de jugadores seleccionados y permite eliminarlos de la partida.
    # El usuario debe introducir el DNI del jugador que desea eliminar.
    
    # Verificar si hay jugadores seleccionados
    if not selected_players:
        print("No hay jugadores disponibles. Por favor, añada jugadores primero.")
        input("Presione Enter para continuar...")
        return
    
    # Solicitar al usuario que introduzca el DNI del jugador
    while True:
        if not selected_players:
            print("No hay jugadores disponibles. Por favor, añada jugadores primero.")
            time.sleep(1)
            break

        Ut.clear_terminal()
        print("=== Eliminar Jugadores de la Partida ===")
        for player_id in selected_players:
            player_data = Dt.context_game["players"].get(player_id, {})
            player_name = player_data.get("name", "Desconocido")
            player_type = "Humano" if player_data.get("human", False) else "Bot"
            player_risk = player_data.get("type", "N/A")
            # Convertir el perfil de riesgo a texto
            if player_risk == 50:
                risk_profile = "Atrevido"
            elif player_risk == 40:
                risk_profile = "Normal"
            elif player_risk == 30:
                risk_profile = "Prudente"
            else:
                risk_profile = "N/A"
            print(player_id.ljust(18) + player_name.ljust(18) + player_type.ljust(18) + risk_profile.ljust(18))
        print()
        print("0) Salir")
        print()
        dni = input(
            "Introduzca el DNI del jugador que desea eliminar: "
        ).strip().upper()
        
        if dni == "0":
            break
        
        if dni in selected_players:
            player_name = Dt.context_game["players"].get(dni, {}).get("name", "Desconocido")
            
            confirm = input(f"¿Está seguro de que desea eliminar a {player_name}? (s/n): ").strip().lower()
            if confirm == "s":
                selected_players.remove(dni)
                print(f"Jugador {player_name} eliminado de la partida.")
                time.sleep(1)
            else:
                print("Eliminación cancelada.")
                time.sleep(1)
        else:
            print("DNI no válido. Inténtelo de nuevo.")
            time.sleep(1)

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
                player_human = "Humano"
            else:
                player_human = "Bot"
            if   Dt.context_game["players"][Dt.context_game["game"][i]]["type"] == 30:
                player_type = "Prudente"
            elif Dt.context_game["players"][Dt.context_game["game"][i]]["type"] == 40:
                player_type = "Moderado"
            elif Dt.context_game["players"][Dt.context_game["game"][i]]["type"] == 50:
                player_type = "Atrevido"
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
        print("=== Seleccionar Baraja de Cartas ===")

        # Mostrar la baraja seleccionada actualmente
        if "cards_deck" in Dt.context_game and Dt.context_game["cards_deck"]:
            if Dt.context_game["cards_deck"] == Dt.cartas_es:
                print("Baraja seleccionada actualmente: Baraja Española (40 cartas)")
            elif Dt.context_game["cards_deck"] == Dt.cartas_en:
                print("Baraja seleccionada actualmente: Baraja Inglesa (52 cartas)")
            elif Dt.context_game["cards_deck"] == Dt.cartas_al:
                print("Baraja seleccionada actualmente: Baraja Alemana (60 cartas)")
        print()
        # Mostrar las opciones de barajas disponibles
        print("Seleccione la baraja de cartas para la partida:")
        print("1) Baraja Española (40 cartas)")
        print("2) Baraja Inglesa (52 cartas)")
        print("3) Baraja Alemana (60 cartas)")
        print("4) Volver al Menú Anterior")

        # Solicitar al usuario que seleccione una opción
        option = Ut.getOpt(
            inputOptText="Seleccione una opción (1-4): ",
            rangeList=[1, 2, 3, 4]
        )

        # Asignar la baraja seleccionada a context_game["cards_deck"]
        if option == 1:
            Dt.context_game["cards_deck"] = Dt.cartas_es
            print("Baraja Española seleccionada.")
        elif option == 2:
            Dt.context_game["cards_deck"] = Dt.cartas_en
            print("Baraja Inglesa seleccionada.")
        elif option == 3:
            Dt.context_game["cards_deck"] = Dt.cartas_al
            print("Baraja Alemana seleccionada.")
        elif option == 4:
            return
        input("Presione Enter para continuar...")

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