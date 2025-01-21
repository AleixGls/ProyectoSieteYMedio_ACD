import SC.Menu
import SC.Datos
import SC.Utilidad as Ut



if __name__ == "__main__":
    SC.Datos.context_game["cards_deck"] = SC.Datos.cartas_es
    SC.Menu.main_menu()