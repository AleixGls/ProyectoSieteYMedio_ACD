import SC.Utilidad as Ut
import SC.Datos as Dt
import SC.Juego as Jg
import SC.Bbdd as Bd



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
    """
    Muestra el menú para añadir, eliminar o mostrar jugadores.
    """
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
            showPlayersGame()
        elif option == 4:
            break

def settings():
    """
    Muestra el menú de configuración del juego.
    """
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
        max_rounds = input("Introduzca el número máximo de rondas (por defecto 5): ").strip()
        
        if max_rounds.isdigit() and int(max_rounds) > 0:
            Dt.context_game["maxRounds"] = int(max_rounds)
            print(f"Número máximo de rondas establecido a {max_rounds}.")
            break
        else:
            print("Entrada no válida. Introduzca un número mayor que 0.")

def setPlayersGame():
    """
    Establece los jugadores que participarán en la partida.
    """
    Ut.clear_terminal()
    print("=== Establecer Jugadores de la Partida ===")
    # Aquí se implementaría la lógica para seleccionar jugadores de la base de datos.
    print("Funcionalidad en desarrollo...")

def showPlayersGame():
    """
    Muestra los jugadores actuales en la partida.
    """
    Ut.clear_terminal()
    print("=== Jugadores en la Partida ===")
    # Aquí se implementaría la lógica para mostrar los jugadores.
    print("Funcionalidad en desarrollo...")

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
    savePlayer(dni, name, risk, human)
    
    print(f"Jugador '{name}' creado con éxito. DNI: {dni}")
    input("Presione Enter para continuar...")