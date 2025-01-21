import SC.Menu
import SC.Datos
import SC.Bbdd


if __name__ == "__main__":
    SC.Bbdd.card_database()
    SC.Datos.context_game["cards_deck"] = SC.Datos.cartas_es
    SC.Menu.main_menu()