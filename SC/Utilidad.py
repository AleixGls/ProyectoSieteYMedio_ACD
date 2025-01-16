import os
import random



def clear_terminal():
    # Limpia la terminal

    os.system('cls' if os.name == 'nt' else 'clear')

def getOpt(textOpts="", inputOptText="", rangeList=[], exceptions=[]):
    # Gestionar menús y obtener una opción válida del usuario.
    # Parámetros:
    # - textOpts: Texto que muestra las opciones disponibles.
    # - inputOptText: Texto que se muestra para solicitar la entrada del usuario.
    # - rangeList: Lista de opciones válidas (por ejemplo, [1, 2, 3]).
    # - exceptions: Lista de excepciones adicionales (por ejemplo, ["salir"])
    # Retorna:
    # - La opción seleccionada por el usuario.

    while True:
        print(textOpts)
        user_input = input(inputOptText).strip().lower()
        
        if user_input.isdigit():
            user_input = int(user_input)
            if user_input in rangeList:
                return user_input
        
        if user_input in exceptions:
            return user_input

        print("Opción no válida. Inténtelo de nuevo.")

def logToFile(text):
    #Guarda un texto en logfileSevenAndHalf.txt.

    f = open("logfileSevenAndHalf.txt", "a")
    f.write(text)
    f.close()

def newRandomDNI():
    # Genera un DNI aleatorio en formato español (8 números + 1 letra).

    num = random.randint(10000000, 99999999)
    letters = 'TRWAGMYFPDXBNJZSQVHLCKE'
    letter = letters[num % 23]
    dni = f"{num}{letter}"
    return dni