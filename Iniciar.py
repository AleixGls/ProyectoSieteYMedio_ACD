from SC.Menu import main_menu
import SC.Datos
import SC.Utilidad as Ut



if __name__ == "__main__":
    SC.Datos.context_game["cards_deck"] = SC.Datos.cartas_es
    main_menu()