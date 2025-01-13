import random

def newRandomDNI():
    num = random.randint(10000000, 99999999)
    letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
    letra = letras[num % 23]
    dni = f"{num}{letra}"
    return dni

def logToFile(text):
    f = open("logfileSevenAndHalf.txt", "a")
    f.write(text)
    f.close()